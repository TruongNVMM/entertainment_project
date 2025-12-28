import math
from collections import Counter

class LZWEncoding:
    def __init__(self):
        """
        Khởi tạo class LZWEncoding.
        Kích thước từ điển gốc là 256 (cho bảng mã ASCII/Bytes 8-bit).
        """
        self.dictionary_size = 256

    def calculate_entropy(self, text: str) -> float:
        """
        Tính Entropy H(X) của nguồn tin (chuỗi văn bản).
        Công thức: H(X) = - sum(p(x) * log2(p(x)))
        """
        if not text:
            return 0.0
        
        # Đếm tần suất xuất hiện của từng ký tự
        frequencies = Counter(text)
        total_chars = len(text)
        
        entropy = 0.0
        for count in frequencies.values():
            p_x = count / total_chars
            entropy += -p_x * math.log2(p_x)
            
        return entropy

    def encode(self, text: str):
        """
        Mã hóa chuỗi văn bản sử dụng thuật toán LZW.
        Input: Chuỗi tiếng Việt (Unicode).
        Output: Danh sách các mã số (integers) và tổng số bit đã sử dụng.
        """
        # Chuyển đổi chuỗi sang bytes (UTF-8) để xử lý tiếng Việt chính xác
        # LZW thường hoạt động trên luồng byte.
        uncompressed = text.encode('utf-8')
        
        # Khởi tạo từ điển với 256 ký tự ASCII đầu tiên
        dictionary = {bytes([i]): i for i in range(self.dictionary_size)}
        dict_size = self.dictionary_size
        
        w = bytes()
        compressed_result = []
        
        # Biến để tính toán tổng số bit thực tế
        total_bits_used = 0
        
        for byte_val in uncompressed:
            c = bytes([byte_val])
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                code = dictionary[w]
                compressed_result.append(code)
                
                # Tính số bit cần thiết để biểu diễn mã này tại thời điểm hiện tại
                # Số bit = ceil(log2(dict_size)) vì từ điển đang lớn dần
                bits_for_this_code = math.ceil(math.log2(dict_size)) if dict_size > 1 else 8
                total_bits_used += max(8, bits_for_this_code) 
                
                # Thêm chuỗi mới vào từ điển
                dictionary[wc] = dict_size
                dict_size += 1
                w = c
        
        if w:
            code = dictionary[w]
            compressed_result.append(code)
            bits_for_this_code = math.ceil(math.log2(dict_size)) if dict_size > 1 else 8
            total_bits_used += max(8, bits_for_this_code)

        return compressed_result, total_bits_used

    def decode(self, compressed_codes: list) -> str:
        """
        Giải mã danh sách code trở lại thành chuỗi ban đầu.
        """
        if not compressed_codes:
            return ""

        # Khởi tạo lại từ điển giải mã
        dictionary = {i: bytes([i]) for i in range(self.dictionary_size)}
        dict_size = self.dictionary_size
        
        # Xử lý mã đầu tiên
        w = dictionary[compressed_codes[0]]
        result = bytearray(w)
        
        for k in compressed_codes[1:]:
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = w + w[:1] # Trường hợp đặc biệt: cScSc
            else:
                raise ValueError(f"Mã nén không hợp lệ: {k}")
            
            result.extend(entry)
            
            # Cập nhật từ điển
            dictionary[dict_size] = w + entry[:1]
            dict_size += 1
            
            w = entry
            
        return result.decode('utf-8')

    def calculate_average_code_length(self, text: str, total_bits: int) -> float:
        """
        Tính độ dài từ mã trung bình (L_avg).
        L_avg = Tổng số bit sau nén / Tổng số ký tự nguồn
        """
        if not text:
            return 0.0
        return total_bits / len(text)
    
    def display(self, text: str): 
        print(f"Độ dài chuỗi: {len(text)} kí tự")

        entropy = self.calculate_entropy(text)
        print(f"Entropy: {entropy} bits/kh")

        compressed_codes, total_bits = self.encode(text)
        print(f"Mã nén (dạng số): {compressed_codes}")
        print(f"Số lượng mã output: {len(compressed_codes)}")
        print(f"Tổng số bit sau nén: {total_bits} bits")

        l_avg = self.calculate_average_code_length(text, total_bits)
        print(f"Độ dài mã trung bình (L_avg): {l_avg:.4f} bits/kh")

        decoded_text = self.decode(compressed_codes)
        print(f"Giải mã: \"{decoded_text}\"")