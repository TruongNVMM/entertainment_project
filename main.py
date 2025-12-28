from Encoding.huffmanEncoding import HuffmanEncoding
from Encoding.arithmeticEncoding import ArithmeticEncoding
from Encoding.lzpEncoding import LZWEncoding
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class CompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BTL - LÝ THUYẾT THÔNG TIN")
        self.root.geometry("650x450")
        
        # Style configuration
        style = ttk.Style()
        style.configure("Bold.TLabel", font=("Arial", 10, "bold"))
        style.configure("Result.TLabel", font=("Consolas", 11), foreground="blue")
        style.configure("Conclusion.TLabel", font=("Arial", 10, "italic"), foreground="#D32F2F") # Màu đỏ đậm cho kết luận

        # --- 1. Khu vực nhập liệu ---
        input_frame = ttk.LabelFrame(root, text="Nhập đoạn văn bản cần mã hóa", padding=(10, 5))
        input_frame.pack(fill="x", padx=10, pady=3)
        
        self.txt_input = scrolledtext.ScrolledText(input_frame, height=5, font=("Arial", 10))
        self.txt_input.pack(fill="x", expand=True)
        self.txt_input.insert(tk.END, "Nhập từ mã") # Default text

        # --- 2. Khu vực chọn thuật toán ---
        control_frame = ttk.Frame(root, padding=(10, 5))
        control_frame.pack(fill="x", padx=10)

        ttk.Label(control_frame, text="Chọn thuật toán:", font=("Arial", 10, "bold")).pack(side="left", padx=(0, 10))
        
        self.algo_var = tk.StringVar(value="huffman")
        
        rb_huffman = ttk.Radiobutton(control_frame, text="Mã Huffman", variable=self.algo_var, value="huffman")
        rb_lzp = ttk.Radiobutton(control_frame, text="Mã LZW (LZP)", variable=self.algo_var, value="lzw")
        rb_arith = ttk.Radiobutton(control_frame, text="Mã Arithmetic", variable=self.algo_var, value="arithmetic")
        
        rb_huffman.pack(side="left", padx=10)
        rb_lzp.pack(side="left", padx=10)
        rb_arith.pack(side="left", padx=10)

        btn_process = ttk.Button(control_frame, text="THỰC HIỆN MÃ HÓA", command=self.process_text)
        btn_process.pack(side="right", padx=10)

        # --- 3. Khu vực hiển thị kết quả (Dashboard) ---
        result_frame = ttk.LabelFrame(root, text="Kết quả Thống kê và Kết luận", padding=(10, 10))
        result_frame.pack(fill="x", padx=10, pady=10)
        
        # Grid layout for results
        # Row 0: Original Length & Entropy
        ttk.Label(result_frame, text="Độ dài chuỗi gốc:", style="Bold.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.lbl_len_orig = ttk.Label(result_frame, text="0 ký tự", style="Result.TLabel")
        self.lbl_len_orig.grid(row=0, column=1, sticky="w", padx=20)

        ttk.Label(result_frame, text="Entropy:", style="Bold.TLabel").grid(row=0, column=2, sticky="w", pady=5)
        self.lbl_entropy = ttk.Label(result_frame, text="0.0000 bits/kh", style="Result.TLabel")
        self.lbl_entropy.grid(row=0, column=3, sticky="w", padx=20)

        # Row 1: Average Code Length & Info
        ttk.Label(result_frame, text="Độ dài TB từ mã:", style="Bold.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.lbl_avg_len = ttk.Label(result_frame, text="0.0000 bits/kh", style="Result.TLabel")
        self.lbl_avg_len.grid(row=1, column=1, sticky="w", padx=20)

        ttk.Label(result_frame, text="Tổng số bit nén:", style="Bold.TLabel").grid(row=1, column=2, sticky="w", pady=5)
        self.lbl_total_bits = ttk.Label(result_frame, text="0 bits", style="Result.TLabel")
        self.lbl_total_bits.grid(row=1, column=3, sticky="w", padx=20)

        # Row 2
        ttk.Label(result_frame, text="Kết luận:", style="Bold.TLabel").grid(row=2, column=0, sticky="nw", pady=15)
        self.lbl_conclusion = ttk.Label(result_frame, text="Chưa có dữ liệu.", style="Conclusion.TLabel", wraplength=450)
        self.lbl_conclusion.grid(row=2, column=1, columnspan=2, sticky="w", padx=20, pady=15)

        self.btn_visualize = ttk.Button(result_frame, text="Xem Biểu đồ", command=self.show_chart, state='disabled')
        self.btn_visualize.grid(row=2, column=3, sticky="e", padx=20, pady=15)
        
        # Data storage for visualization
        self.entropy_val = 0.0
        self.avg_len_val = 0.0
        self.algo_name = ""
        
        # --- 4. Khu vực giải mã ---
        decode_frame = ttk.LabelFrame(root, text="Kết quả giải mã", padding=(10, 5))
        decode_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.txt_output = scrolledtext.ScrolledText(decode_frame, height=3, state='disabled', font=("Arial", 10), background="#f0f0f0")
        self.txt_output.pack(fill="both", expand=True)

    def process_text(self):
        text = self.txt_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập văn bản trước khi mã hóa!")
            return

        algo = self.algo_var.get()
        
        try:
            length_orig = len(text)
            entropy = 0.0
            avg_len = 0.0
            decoded_text = ""

            if algo == "huffman":
                huff = HuffmanEncoding()
                encoded_str = huff.encode(text)
                entropy = huff.calculate_entropy(text)
                avg_len = huff.average_code_length()
                total_bits_encoded = len(encoded_str)
                decoded_text = huff.decode(encoded_str)

            elif algo == "lzw":
                lzw = LZWEncoding()
                entropy = lzw.calculate_entropy(text)
                codes, total_bits_encoded = lzw.encode(text)
                avg_len = lzw.calculate_average_code_length(text, total_bits_encoded)
                decoded_text = lzw.decode(codes)

            elif algo == "arithmetic":
                arith = ArithmeticEncoding(text)
                entropy = arith.calculate_entropy()
                low, high, p_s = arith.encode()
                total_bits_encoded = arith.calculate_total_length_formula(p_s)
                avg_len = arith.calculate_average_length(total_bits_encoded)
                decoded_text = arith.decode(low, len(text))

            # Update UI
            self.lbl_len_orig.config(text=f"{length_orig} ký tự")
            self.lbl_entropy.config(text=f"{entropy:.4f} bits/kh")
            self.lbl_avg_len.config(text=f"{avg_len:.4f} bits/kh")
            self.lbl_total_bits.config(text=f"{total_bits_encoded} bits")
            
            conclusion_msg = ""
            epsilon = 0.000001 # Sai số cho phép khi so sánh số thực
            
            if avg_len >= entropy - epsilon:
                diff = avg_len - entropy
                if diff < 0.1:
                    conclusion_msg = (f"Độ dài mã trung binh ({avg_len:.2f}) ≈ Entropy ({entropy:.2f}).")
                    self.lbl_conclusion.config(foreground="green")
                else:
                    conclusion_msg = (f"Độ dài mã trung bình ({avg_len:.2f}) > Entropy ({entropy:.2f}).")
                    self.lbl_conclusion.config(foreground="blue")
            else:
                conclusion_msg = (f"L_avg ({avg_len:.2f}) < Entropy ({entropy:.2f}).")
                self.lbl_conclusion.config(foreground="red")
            
            self.lbl_conclusion.config(text=conclusion_msg)

            # Store for visualization
            self.entropy_val = entropy
            self.avg_len_val = avg_len
            self.algo_name = self.algo_var.get()
            self.btn_visualize.config(state='normal')

            # Show decoded text
            self.txt_output.config(state='normal')
            self.txt_output.delete("1.0", tk.END)
            self.txt_output.insert(tk.END, decoded_text)
            self.txt_output.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra trong quá trình tính toán:\n{str(e)}")

    def show_chart(self):
        if self.entropy_val == 0 and self.avg_len_val == 0:
            return

        # Create new window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Trực quan hóa Kết quả")
        chart_window.geometry("600x500")

        # Prepare data
        labels = ['Entropy', 'Avg Code Length']
        values = [self.entropy_val, self.avg_len_val]
        colors = ['#1f77b4', '#ff7f0e']

        # Create Plot
        fig, ax = plt.subplots(figsize=(6, 5))
        bars = ax.bar(labels, values, color=colors, width=0.5)

        # Labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

        ax.set_ylabel('Bits per symbol')
        algo_display = "Huffman" if self.algo_name == "huffman" else ("LZW" if self.algo_name == "lzw" else "Arithmetic")
        ax.set_title(f'So sánh Entropy vs Avg Code Length ({algo_display})')
        
        # Add Entropy reference line
        ax.axhline(y=self.entropy_val, color='r', linestyle='--', alpha=0.5, label='Entropy Limit')
        ax.legend()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



if __name__ == "__main__":
    root = tk.Tk()
    app = CompressionApp(root)
    root.mainloop()