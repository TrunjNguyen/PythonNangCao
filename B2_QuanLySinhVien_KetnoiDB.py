import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import Error

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng Nhập")
        self.root.geometry("300x150")

        # Tạo các biến
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Frame đăng nhập
        login_frame = ttk.LabelFrame(root, text="Đăng nhập", padding=10)
        login_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Username
        ttk.Label(login_frame, text="Tên đăng nhập:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(login_frame, textvariable=self.username_var).grid(row=0, column=1, padx=5, pady=5)

        # Password
        ttk.Label(login_frame, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(login_frame, textvariable=self.password_var, show="*").grid(row=1, column=1, padx=5, pady=5)

        # Nút đăng nhập
        ttk.Button(login_frame, text="Đăng nhập", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        # Kiểm tra thông tin đăng nhập (ví dụ đơn giản)
        if username == "Thanhtrung" and password == "123456":
            self.root.destroy()  # Đóng cửa sổ đăng nhập
            main_window = tk.Tk()  # Mở cửa sổ chính
            QuanLySinhVien(main_window)
        else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

class QuanLySinhVien:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản Lý Sinh Viên")
        self.root.geometry("800x600")

        # Kết nối database
        try:
            self.conn = psycopg2.connect(
                database="TestDB",
                user="postgres",
                password="123456",
                host="localhost",
                port="5432"
            )
            self.cursor = self.conn.cursor()
            
            # Tạo bảng nếu chưa tồn tại
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS sinh_vien (
                    ma_sv VARCHAR(20) PRIMARY KEY,
                    ho_ten VARCHAR(50) NOT NULL
                )
            """)
            self.conn.commit()
        except Error as e:
            messagebox.showerror("Lỗi", f"Lỗi kết nối database: {e}")

        # Tạo các biến
        self.ma_sv_var = tk.StringVar()
        self.ho_ten_var = tk.StringVar()

        # Frame nhập liệu
        input_frame = ttk.LabelFrame(root, text="Thông tin sinh viên", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Mã sinh viên
        ttk.Label(input_frame, text="Mã sinh viên:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.ma_sv_var).grid(row=0, column=1, padx=5, pady=5)

        # Họ tên
        ttk.Label(input_frame, text="Họ tên:").grid(row=0, column=2, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.ho_ten_var).grid(row=0, column=3, padx=5, pady=5)

        # Frame nút chức năng
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        # Các nút chức năng
        ttk.Button(button_frame, text="Thêm", command=self.them_sinh_vien).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Sửa", command=self.sua_sinh_vien).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.xoa_sinh_vien).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Đăng xuất", command=self.dang_xuat).grid(row=0, column=3, padx=5)

        # Treeview hiển thị danh sách
        self.tree = ttk.Treeview(root, columns=("Mã SV", "Họ tên"), show="headings")
        self.tree.heading("Mã SV", text="Mã SV")
        self.tree.heading("Họ tên", text="Họ tên")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Binding sự kiện chọn item
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Load dữ liệu
        self.load_data()

    def dang_xuat(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            self.root.destroy()
            login_window = tk.Tk()
            LoginWindow(login_window)

    # [Các phương thức khác giữ nguyên như cũ]
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            self.cursor.execute("SELECT * FROM sinh_vien")
            rows = self.cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
        except Error as e:
            messagebox.showerror("Lỗi", f"Lỗi load dữ liệu: {e}")

    def them_sinh_vien(self):
        ma_sv = self.ma_sv_var.get()
        ho_ten = self.ho_ten_var.get()

        if not ma_sv or not ho_ten:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            self.cursor.execute("INSERT INTO sinh_vien (ma_sv, ho_ten) VALUES (%s, %s)", (ma_sv, ho_ten))
            self.conn.commit()
            messagebox.showinfo("Thành công", "Thêm sinh viên thành công!")
            self.clear_entries()
            self.load_data()
        except Error as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi thêm sinh viên: {e}")

    def sua_sinh_vien(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên cần sửa!")
            return

        ma_sv = self.ma_sv_var.get()
        ho_ten = self.ho_ten_var.get()

        if not ma_sv or not ho_ten:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            self.cursor.execute("UPDATE sinh_vien SET ho_ten = %s WHERE ma_sv = %s", (ho_ten, ma_sv))
            self.conn.commit()
            messagebox.showinfo("Thành công", "Cập nhật sinh viên thành công!")
            self.clear_entries()
            self.load_data()
        except Error as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi cập nhật sinh viên: {e}")

    def xoa_sinh_vien(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên cần xóa!")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa sinh viên này?"):
            ma_sv = self.tree.item(selected_item)['values'][0]
            try:
                self.cursor.execute("DELETE FROM sinh_vien WHERE ma_sv = %s", (ma_sv,))
                self.conn.commit()
                messagebox.showinfo("Thành công", "Xóa sinh viên thành công!")
                self.clear_entries()
                self.load_data()
            except Error as e:
                self.conn.rollback()
                messagebox.showerror("Lỗi", f"Lỗi xóa sinh viên: {e}")

    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            self.ma_sv_var.set(values[0])
            self.ho_ten_var.set(values[1])

    def clear_entries(self):
        self.ma_sv_var.set("")
        self.ho_ten_var.set("")

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()