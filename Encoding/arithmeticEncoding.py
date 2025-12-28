import math
from collections import Counter
from decimal import Decimal, getcontext

# Thiết lập độ chính xác cao cho thư viện Decimal
# Arithmetic coding tạo ra các khoảng số cực nhỏ, float thông thường sẽ bị underflow (về 0)
getcontext().prec = 100  # Tăng lên nếu chuỗi văn bản rất dài

class ArithmeticEncoding:
    def __init__(self, text):
        self.text = text
        self.length = len(text)
        self.frequencies = Counter(text)
        self.probabilities = self._calculate_probabilities()
        self.ranges = self._calculate_ranges()

    def _calculate_probabilities(self):
        """Tính xác suất xuất hiện của từng ký tự"""
        probs = {}
        for char, count in self.frequencies.items():
            probs[char] = Decimal(count) / Decimal(self.length)
        return probs

    def _calculate_ranges(self):
        """
        Xác định khoảng [low, high) cho từng ký tự.
        Ví dụ: a: [0, 0.5), b: [0.5, 0.8), ...
        """
        ranges = {}
        current_low = Decimal(0)
        # Sắp xếp keys để đảm bảo thứ tự khoảng nhất quán
        for char in sorted(self.probabilities.keys()):
            prob = self.probabilities[char]
            ranges[char] = (current_low, current_low + prob)
            current_low += prob
        return ranges

    def calculate_entropy(self):
        """
        Tính Entropy (H) của nguồn tin theo công thức Shannon:
        H = - sum(p(x) * log2(p(x)))
        """
        entropy = Decimal(0)
        for prob in self.probabilities.values():
            if prob > 0:
                # Sử dụng logarit cơ số 2
                entropy -= prob * (prob.ln() / Decimal(2).ln())
        return float(entropy)

    def encode(self):
        """
        Thực hiện mã hóa để tìm khoảng cuối cùng.
        Trả về: (low, high, interval_width)
        """
        low = Decimal(0)
        high = Decimal(1)
        
        for char in self.text:
            # Độ rộng khoảng hiện tại
            current_range = high - low
            
            # Lấy khoảng con của ký tự hiện tại
            char_low, char_high = self.ranges[char]
            
            # Cập nhật high trước (dựa trên low cũ)
            high = low + current_range * char_high
            # Cập nhật low sau
            low = low + current_range * char_low
            
        interval_width = high - low
        return low, high, interval_width
     
    def decode(self, encoded_value, length):
        """
        Giải mã từ một giá trị số thực về chuỗi văn bản.
        
        Args:
            encoded_value (Decimal): Một giá trị nằm trong khoảng [low, high) cuối cùng.
            length (int): Số lượng ký tự cần giải mã.
        """
        decoded_text = []
        # Thêm một lượng cực nhỏ epsilon để bù trừ sai số làm tròn (precision drift)
        # khi encoded_value nằm sát biên dưới (low).
        # Với prec=100, 1e-50 đủ nhỏ để không ảnh hưởng dữ liệu ngắn/trung bình
        # nhưng đủ lớn để tránh lỗi "hụt" biên.
        current_value = encoded_value + Decimal('1e-80')

        for _ in range(length):
            # Tìm ký tự mà current_value rơi vào khoảng của nó
            for char, (low_range, high_range) in self.ranges.items():
                if low_range <= current_value < high_range:
                    decoded_text.append(char)
                    
                    # Cập nhật giá trị để giải mã ký tự tiếp theo
                    # Công thức: v_new = (v_old - low_i) / (high_i - low_i)
                    range_width = high_range - low_range
                    current_value = (current_value - low_range) / range_width
                    break
                    
        return "".join(decoded_text)

    def calculate_total_length_formula(self, p_s):
        """
        Tính tổng độ dài bit (L_total) dựa trên công thức bạn cung cấp:
        L_total = ceil( -log2(P(S)) ) + 1
        
        Args:
            p_s (Decimal): Độ rộng của khoảng số thực cuối cùng (Interval Width)
        """
        if p_s <= 0:
            return 0
            
        # Tính -log2(P(S))
        # Vì Decimal không có log2 trực tiếp, ta dùng ln(x)/ln(2)
        log2_val = p_s.ln() / Decimal(2).ln()
        neg_log2 = -log2_val
        
        # Hàm trần (Ceiling)
        ceil_val = math.ceil(neg_log2)
        
        # Cộng thêm hằng số an toàn +1 như trong công thức
        l_total = ceil_val + 1
        
        return l_total

    def calculate_average_length(self, l_total):
        """
        Tính độ dài từ mã trung bình (bits per symbol):
        L_avg = L_total / Tổng số ký tự
        """
        if self.length == 0: return 0
        return l_total / self.length

    def display(self):
        print(f"Độ dài chuỗi: {len(self.text)} ký tự")
        
        entropy = self.calculate_entropy()
        print(f"Entropy: {entropy:.6f} bits/kh")

        low, high, p_s = self.encode()
        print(f"Low  : {low}")
        print(f"High : {high}")
        print(f"P(S) (Độ rộng): {p_s}")
        
        l_total = self.calculate_total_length_formula(p_s)
        print(f"L_total = {l_total} bits (Tổng số bit cần để lưu cả chuỗi)")

        l_avg = self.calculate_average_length(l_total)
        print(f"Độ dài trung bình của từ mã: L_avg = {l_total} / {len(self.text)} = {l_avg:.6f} bits/kh")

        decoder = self.decode(low, len(self.text))
        print(f"Giải mã: {decoder}")