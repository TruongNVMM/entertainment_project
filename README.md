# Ứng Dụng Minh Họa Thuật Toán Nén Dữ Liệu - Lý Thuyết Thông Tin

Chào mừng đến với ứng dụng **Minh Họa Thuật Toán Nén Dữ Liệu Dạng Văn Bản**. Đây là công cụ trực quan giúp người dùng hiểu rõ hơn về các khái niệm cốt lõi trong Lý thuyết Thông tin (Information Theory) như Entropy, độ dài mã trung bình, và hiệu quả của các thuật toán nén phổ biến.

Ứng dụng được xây dựng bằng **Python**, sử dụng giao diện đồ họa **Tkinter** và thư viện vẽ biểu đồ **Matplotlib**.

---
*Dự án Bài tập lớn môn Lý thuyết thông tin.*       
*Họ và Tên thành viên nhóm:*  
**Nguyễn Việt Trường 20234042**     
**Nguyễn Hoàng Anh 20233994**  
**Vũ Hoàng Hiệp 20234005**  
**Nguyễn Quốc Huy 20234013**

---

## 📋 Mục lục

1. [Yêu cầu hệ thống & Cài đặt](#1-yêu-cầu-hệ-thống--cài-đặt)
   - [Cài đặt Python](#cài-đặt-python)
   - [Cài đặt thư viện phụ thuộc](#cài-đặt-thư-viện-phụ-thuộc)
2. [Hướng dẫn sử dụng](#2-hướng-dẫn-sử-dụng)
3. [Tính năng nổi bật](#3-tính-năng-nổi-bật)

---

## 1. Yêu cầu hệ thống & Cài đặt

Trước khi chạy ứng dụng, bạn cần đảm bảo máy tính đã được cài đặt môi trường Python.

### Cài đặt Python

Nếu máy tính của bạn chưa có Python, hãy làm theo các bước sau:

1.  Truy cập trang chủ Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2.  Tải xuống phiên bản Python mới nhất (khuyến nghị **Python 3.8** trở lên).
3.  Chạy file cài đặt (`.exe`).
4.  **QUAN TRỌNG:** Ở màn hình cài đặt đầu tiên, hãy tích vào ô **"Add Python to PATH"** trước khi nhấn "Install Now". Điều này giúp bạn có thể chạy lệnh python từ bất kỳ đâu.

### Cài đặt thư viện phụ thuộc

Ứng dụng yêu cầu một số thư viện để xử lý tính toán và vẽ biểu đồ. Sau khi cài Python, hãy mở **Command Prompt (CMD)** hoặc **PowerShell** và chạy lệnh sau:

```bash
pip install matplotlib numpy
```

*(Lưu ý: `tkinter` là thư viện giao diện mặc định thường đi kèm với Python nên không cần cài đặt thêm).*

---

## 2. Hướng dẫn sử dụng

Sau khi cài đặt xong, bạn có thể khởi chạy ứng dụng bằng cách mở terminal tại thư mục dự án và chạy lệnh:

```bash
python main.py (sử dụng window) hoặc python3 main.py (sử dụng linux)  
```

Dưới đây là quy trình thao tác chuẩn để sử dụng phần mềm:

### Bước 1: Nhập dữ liệu đầu vào
Tại giao diện chính, bạn sẽ thấy khung **"Nhập đoạn văn bản cần mã hóa"**.
- Nhập chuỗi ký tự hoặc đoạn văn bản bất kỳ mà bạn muốn nén vào ô này.
- *Ví dụ: "Xin Chào ĐạI HọC bácH Khoa Hà nỘi"*

### Bước 2: Lựa chọn thuật toán
Tại khu vực **"Chọn thuật toán"**, hãy tích chọn một trong ba phương pháp nén:
- 🔘 **Mã Huffman**: Thuật toán nén không mất dữ liệu dựa trên tần suất ký tự.
- 🔘 **Mã LZW (LZP)**: Thuật toán nén dựa trên từ điển (thường dùng trong GIF, ZIP).
- 🔘 **Mã Arithmetic**: Mã hóa số học, biểu diễn cả chuỗi tin bằng một số thực duy nhất.

### Bước 3: Thực hiện mã hóa
Nhấn nút **"THỰC HIỆN MÃ HÓA"** ở góc phải.
- Chương trình sẽ tính toán Entropy, xây dựng mã, và giải mã lại để kiểm tra tính toàn vẹn.

### Bước 4: Xem kết quả thống kê
Quan sát khu vực **"Kết quả Thống kê và Kết luận"**:
- **Độ dài chuỗi gốc:** Số lượng ký tự ban đầu.
- **Entropy:** Giới hạn nén lý thuyết (bits/ký tự).
- **Độ dài TB từ mã:** Số bit trung bình thực tế tốn cho mỗi ký tự sau khi nén.
- **Kết luận:** Hệ thống sẽ tự động so sánh xem thuật toán nén có đạt hiệu quả tiệm cận với Entropy hay không.

### Bước 5: Trực quan hóa kết quả
Sau khi có kết quả tính toán, nút **"Xem Biểu đồ"** sẽ sáng lên (kích hoạt).
- Nhấn vào nút này để mở cửa sổ biểu đồ.
- Một biểu đồ cột sẽ hiện ra, so sánh trực quan giữa **Entropy (Lý thuyết)** và **Độ dài mã trung bình (Thực tế)**.
- Đây là minh chứng rõ ràng nhất cho hiệu quả của thuật toán nén: Cột "Avg Code Length" càng gần (hoặc bằng) cột "Entropy" thì nén càng tốt.

---

## 3. Tính năng nổi bật

*   **Đa thuật toán:** Hỗ trợ cả 3 thuật toán kinh điển Huffman, LZW, và Arithmetic.
*   **Giao diện trực quan:** Thiết kế hiện đại, dễ thao tác.
*   **So sánh thời gian thực:** Tính toán và hiển thị ngay lập tức các chỉ số quan trọng (Entropy vs Length).
*   **Data Visualization:** Tích hợp biểu đồ Matplotlib ngay trong ứng dụng để phục vụ báo cáo và nghiên cứu.
*   **Kiểm chứng giải mã:** Luôn hiển thị chuỗi sau khi giải mã để chứng minh thuật toán hoạt động chính xác (Lossless).


