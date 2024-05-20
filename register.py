import subprocess
from customtkinter import *
from setting import *
import tkinter.messagebox as mbox
import mysql.connector

# Kết nối MySQL
host = 'localhost'
user = 'root'
password = ''  # Mặc định là trống nếu bạn không thiết lập mật khẩu cho MySQL trong XAMPP
database = 'to_do_list'  # Thay bằng tên cơ sở dữ liệu của bạn

try:
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
except mysql.connector.Error as err:
    mbox.showinfo("Thông báo", f"Kết nối cơ sở dữ liệu thất bại: {err}")
    exit()

# App
app = CTk()
app.geometry(geometry_main)
app.title("Trang Đăng Kí")

# Setting theme
theme_setting = theme_dark
def theme():
    global theme_setting
    if btn_theme.cget("text") == "Light":
        app._set_appearance_mode("Light")  # Đúng chế độ giao diện cho 'Light'
        btn_theme.configure(text="Dark")
        theme_setting = theme_light
    else:
        app._set_appearance_mode("Dark")  # Đúng chế độ giao diện cho 'Dark'
        btn_theme.configure(text="Light")
        theme_setting = theme_dark
    # Cập nhật giao diện dựa trên cài đặt chủ đề mới
    btn_theme.configure(bg_color=theme_setting['bg_color'], corner_radius=theme_setting['corner_radius'])
    frame.configure(corner_radius=theme_setting["corner_radius"], bg_color=theme_setting["bg_color"], fg_color=theme_setting["fg_color"])
    h1_label.configure(text_color=theme_setting["text_color"])

# Tạo nút chuyển đổi chủ đề
btn_theme = CTkButton(
    master=app, text="Light", font=("Arial", 18),
    corner_radius=theme_setting["corner_radius"], bg_color=theme_setting['bg_color'],
    command=theme
)
btn_theme.place(relx=0.9, rely=0.9, anchor="center")

# Tạo một khung để chứa các widget khác
frame = CTkFrame(master=app, width=400, height=500, corner_radius=20, bg_color=theme_setting["bg_color"], fg_color=theme_setting["fg_color"])
frame.place(relx=0.5, rely=0.5, anchor="center")

# Thêm một nhãn vào khung
h1_label = CTkLabel(master=frame, text="Đăng Kí", font=("Arial", 30), text_color=theme_setting["text_color"])
h1_label.place(relx=0.5, rely=0.2, anchor="center")

# Thêm các widget khác vào khung nếu cần
entry_username = CTkEntry(master=frame, width=250, placeholder_text="Username")
entry_username.place(relx=0.5, rely=0.45, anchor="center")

entry_password = CTkEntry(master=frame, width=250, placeholder_text="Password", show="*")
entry_password.place(relx=0.5, rely=0.6, anchor="center")

def register_clicked():
    # Lấy thông tin từ các ô nhập liệu
    username = entry_username.get()
    password = entry_password.get()

    # Kiểm tra độ dài của tên đăng nhập và mật khẩu
    if len(username) < 8 or len(password) < 8:
        mbox.showinfo("Thông báo", "Tên đăng nhập và mật khẩu phải có ít nhất 8 kí tự.")
    else:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM account WHERE account = %s"
            cursor.execute(query, (username,))
            account = cursor.fetchone()

            if account:
                mbox.showinfo("Thông báo", "Tài khoản đã tồn tại trong hệ thống!")
            else:
                # Tài khoản không tồn tại, tạo mới
                query = "INSERT INTO account (account, password) VALUES (%s, MD5(%s))"
                cursor.execute(query, (username, password))
                conn.commit()
                mbox.showinfo("Thông báo", "Tài khoản đã được tạo mới thành công!")

        except mysql.connector.Error as err:
            mbox.showinfo("Thông báo", "Đăng kí thất bại. Vui lòng thử lại sau.")
            print("Lỗi:", err)
        finally:
            cursor.close()

btn_login = CTkButton(master=frame, text="Đăng Kí", font=("Arial", 20), height=30, command=register_clicked)
btn_login.place(relx=0.5, rely=0.8, anchor="center")

def register():
    app.destroy()
    subprocess.run(["python", "login.py"])

btn_register = CTkButton(master=frame, text="Đăng Nhập", font=("Arial", 15), command=register)
btn_register.place(relx=0.5, rely=0.89, anchor="center")

app.mainloop()
