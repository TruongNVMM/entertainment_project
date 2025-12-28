import heapq
from collections import Counter
import math

class HuffmanNode:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanEncoding:
    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}
        self.freq_table = {}

    def build_frequency_table(self, text: str) -> dict[str, int]:
        self.freq_table = Counter(text)
        return self.freq_table

    def build_huffman_tree(self, freq_table: dict[str, int]) -> HuffmanNode:
        priority_queue = [HuffmanNode(freq, char) for char, freq in freq_table.items()]
        heapq.heapify(priority_queue)

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            merged = HuffmanNode(left.freq + right.freq, None, left, right)
            heapq.heappush(priority_queue, merged)

        return priority_queue[0] if priority_queue else None

    def build_codes_helper(self, node: HuffmanNode, current_code: str):
        if node is None:
            return
        if node.char is not None:
            self.codes[node.char] = current_code
            self.reverse_codes[current_code] = node.char
            return
        self.build_codes_helper(node.left, current_code + "0")
        self.build_codes_helper(node.right, current_code + "1")

    def build_codes(self, tree_root: HuffmanNode):
        self.codes = {}
        self.reverse_codes = {}
        self.build_codes_helper(tree_root, "")

    def encode(self, text: str) -> str:
        self.build_frequency_table(text)
        tree_root = self.build_huffman_tree(self.freq_table)
        self.build_codes(tree_root)
        encoded_text = "".join(self.codes[ch] for ch in text)
        return encoded_text

    def decode(self, encoded_text: str) -> str:
        current_code = ""
        decoded_text = []
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded_text.append(self.reverse_codes[current_code])
                current_code = ""
        return "".join(decoded_text)

    def get_codes(self) -> dict[str, str]:
        return self.codes

    def average_code_length(self) -> float:
        """
        Tính độ dài trung bình mã Huffman:
        = sum(p_i * l_i) với p_i là xác suất, l_i là độ dài mã của ký tự i.
        """
        if not self.codes or not self.freq_table:
            return 0.0

        total_chars = sum(self.freq_table.values())
        avg_length = 0.0
        for ch, freq in self.freq_table.items():
            p_i = freq / total_chars
            l_i = len(self.codes.get(ch, ""))
            avg_length += p_i * l_i
        return avg_length
    
    def calculate_entropy(self, text):
        """Tính Entropy Shannon (H) của văn bản."""
        total_len = len(text)
        frequency = Counter(text)
        entropy = 0
        
        for char, count in frequency.most_common(5):
            prob = count / total_len
            entropy -= prob * math.log2(prob)
            
        # Tính tiếp entropy cho các ký tự còn lại (không in ra để gọn)
        for char, count in frequency.most_common()[5:]:
            prob = count / total_len
            entropy -= prob * math.log2(prob)
            
        return entropy
    
    def display(self, text: str): 
        print(f"Độ dài chuỗi: {len(text)} kí tự")

        entropy = self.calculate_entropy(text)
        print(f"Entropy: {entropy} bits/kh")

        encoder = self.encode(text)
        print(f"Mã hóa: {encoder}")

        average_length = self.average_code_length()
        print(f"Độ dài mã trung bình: {average_length}")

        decoder = self.decode(encoder)
        print(f"Giải mã: {decoder}")
