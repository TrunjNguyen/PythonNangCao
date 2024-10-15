import tkinter as tk
from tkinter import messagebox
import re  # Import để kiểm tra định dạng email

def validate_name(name):
    # Kiểm tra tên chỉ chứa chữ cái và 
    return name.isalpha() 

def validate_email(email):
    # Kiểm tra email chứa ký tự @ và phần chữ cái, số
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_age(age):
    # Kiểm tra tuổi chỉ chứa số
    return age.isdigit()

def submit_form():
    name = entry_name.get()
    email = entry_email.get()
    age = entry_age.get()
    workshops = []
    
    # Kiểm tra các lựa chọn tham gia workshop
    if var_workshop1.get() == 1:
        workshops.append("Workshop 1:'GOOGLE AI'")
    if var_workshop2.get() == 1:
        workshops.append("Workshop 2:'VIETNAM'S CREATIVITY DAWN'")
    if var_workshop3.get() == 1:
        workshops.append("Workshop 3:'CREATOR HACKING'")
    
    is_agree = var_agree.get()

    # Kiểm tra thông tin nhập
    if not validate_name(name):
        messagebox.showwarning("Lỗi", "Vui lòng nhập đúng Họ và tên")
        return
    if not validate_email(email):
        messagebox.showwarning("Lỗi", "Email không hợp lệ. Vui lòng nhập đúng định dạng email.")
        return
    if not validate_age(age):
        messagebox.showwarning("Lỗi", "Tuổi của bạn không đúng! Vui lòng nhập lại số tuổi")
        return
    if not is_agree:
        messagebox.showwarning("Lỗi", "Vui lòng xác nhận đồng ý với điều khoản.")
        return
    if not workshops:
        messagebox.showwarning("Lỗi", "Vui lòng chọn ít nhất một workshop.")
        return

    # Hiển thị thông báo đăng ký thành công
    messagebox.showinfo("Thông báo", f"Đăng ký thành công!\nHọ và tên: {name}\nEmail: {email}\nTuổi: {age}\nTham gia: {', '.join(workshops)}")

# Tạo cửa sổ chính
win = tk.Tk()
win.title("Đăng ký tham gia sự kiện")
win.geometry("450x400")
win.config(bg="#e6f7ff")  # Màu nền tổng thể của cửa sổ

# Tạo LabelFrame để chứa các thành phần đăng ký
frame = tk.LabelFrame(win, text="Thông tin đăng ký", padx=10, pady=10, bg="#ffffff", fg="#333", font=("Arial", 12, "bold"))
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Label và Entry cho tên
label_name = tk.Label(frame, text="Họ và tên:", bg="#ffffff", fg="#333333", font=("Arial", 10, "bold"))
label_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_name = tk.Entry(frame, bg="#f0f8ff", fg="#000", font=("Arial", 10))
entry_name.grid(row=0, column=1, padx=10, pady=5)

# Label và Entry cho email
label_email = tk.Label(frame, text="Email:", bg="#ffffff", fg="#333333", font=("Arial", 10, "bold"))
label_email.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_email = tk.Entry(frame, bg="#f0f8ff", fg="#000", font=("Arial", 10))
entry_email.grid(row=1, column=1, padx=10, pady=5)

# Label và Entry cho tuổi
label_age = tk.Label(frame, text="Tuổi:", bg="#ffffff", fg="#333333", font=("Arial", 10, "bold"))
label_age.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_age = tk.Entry(frame, bg="#f0f8ff", fg="#000", font=("Arial", 10))
entry_age.grid(row=2, column=1, padx=10, pady=5)

# Checkbutton để chọn workshop tham gia
var_workshop1 = tk.IntVar()
var_workshop2 = tk.IntVar()
var_workshop3 = tk.IntVar()

check_workshop1 = tk.Checkbutton(frame, text=" Workshop 1: 'GOOGLE AI", variable=var_workshop1, bg="#ffffff", fg="#333333", font=("Arial", 10))
check_workshop1.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=5)

check_workshop2 = tk.Checkbutton(frame, text="Workshop 2: 'VIETNAM'S CREATIVITY DAWN'", variable=var_workshop2, bg="#ffffff", fg="#333333", font=("Arial", 10))
check_workshop2.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=5)

check_workshop3 = tk.Checkbutton(frame, text="Workshop 3: 'CREATOR HACKING'", variable=var_workshop3, bg="#ffffff", fg="#333333", font=("Arial", 10))
check_workshop3.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=5)

# Checkbutton đồng ý điều khoản
var_agree = tk.IntVar()
check_agree = tk.Checkbutton(frame, text="Tôi đồng ý với các điều khoản", variable=var_agree, bg="#ffffff", fg="#333333", font=("Arial", 10, "italic"))
check_agree.grid(row=6, columnspan=2, pady=10)

# Button gửi đăng ký
btn_submit = tk.Button(win, text="Gửi đăng ký", command=submit_form, bg="#4CAF80", fg="#ffffff", font=("Arial", 12, ))
btn_submit.pack(pady=10)

# Chạy vòng lặp chính
win.mainloop()
