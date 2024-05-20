from customtkinter import *
from setting import *
import tkinter.messagebox as mbox
import mysql.connector
import subprocess
import os

os.environ["LOGGED_IN"] = "false"

# kết nối mysql
host = 'localhost'
user = 'root'
password = ''  # Mặc định là trống nếu bạn không thiết lập mật khẩu cho MySQL trong XAMPP
database = 'to_do_list'  # Thay tendb bằng tên cơ sở dữ liệu của bạn

conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# app
app = CTk()
app.geometry(geometry_main)
app.title("Trang Đăng Nhập")

#setting theme
theme_setting = theme_dark
def theme():
    global theme_setting
    if btn_theme.cget("text") == "Light":
        app._set_appearance_mode("Light")  # Correct appearance mode for 'Dark'
        btn_theme.configure(text="Dark")
        theme_setting = theme_light
    else:
        app._set_appearance_mode("Dark")  # Correct appearance mode for 'Light'
        btn_theme.configure(text="Light")
        theme_setting = theme_dark
    # Update button's appearance based on the new theme setting
    btn_theme.configure(bg_color=theme_setting['bg_color'], corner_radius=theme_setting['corner_radius'])
    frame.configure(corner_radius=theme_setting["corner_radius"], bg_color=theme_setting["bg_color"],fg_color=theme_setting["fg_color"])
    h1_label.configure(text_color = theme_setting["text_color"])

# Create the theme toggle button
btn_theme = CTkButton(
    master=app, text="Light", font=("Arial", 18),
    corner_radius=theme_setting["corner_radius"], bg_color=theme_setting['bg_color'],
    command=theme
)
btn_theme.place(relx=0.9, rely=0.9, anchor="center")

# Create a frame to contain other widgets
frame = CTkFrame(master=app, width=400, height=500, corner_radius=20, bg_color=theme_setting["bg_color"], fg_color=theme_setting["fg_color"])
frame.place(relx=0.5, rely=0.5, anchor="center")

# Add a label to the frame
h1_label = CTkLabel(master=frame, text="Đăng Nhập", font=("Arial", 30), text_color=theme_setting["text_color"])
h1_label.place(relx=0.5, rely=0.2, anchor="center")

# Add other widgets to the frame as needed
# For example, adding an entry field or another button
entry_username = CTkEntry(master=frame,width=250, placeholder_text="Username")
entry_username.place(relx=0.5, rely=0.45, anchor="center")

entry_password = CTkEntry(master=frame,width=250, placeholder_text="Password", show="*")
entry_password.place(relx=0.5, rely=0.6, anchor="center")

def login_clicked():
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

            
            # Tài khoản tồn tại, kiểm tra mật khẩu
            query = "SELECT * FROM account WHERE account = %s AND password = MD5(%s)"
            cursor.execute(query, (username, password))
            account = cursor.fetchone()

            if account:
                mbox.showinfo("Thông báo", "Đăng nhập thành công!")
                with open("log.txt", "w") as f:
                    f.write(username)
                os.environ["LOGGED_IN"] = "true"
                app.destroy()
                subprocess.run(["python", "main.py"])
            else:
                mbox.showinfo("Thông báo", "Mật khẩu không đúng.")
            # else:
            #     # Tài khoản không tồn tại, tạo mới
            #     query = "INSERT INTO account (account, password) VALUES (%s, MD5(%s))"
            #     cursor.execute(query, (username, password))
            #     conn.commit()  # Cần commit để lưu thay đổi vào cơ sở dữ liệu

            #     mbox.showinfo("Thông báo", "Tài khoản đã được tạo mới thành công!")

        except mysql.connector.Error as err:
            mbox.showinfo("Thông báo", "Đăng nhập thất bại. Vui lòng thử lại sau.")
            print("Lỗi:", err)
        finally:
            cursor.close()


btn_login = CTkButton(master=frame, text="Đăng Nhập",font=("Arial", 20), height=30, command=login_clicked)
btn_login.place(relx=0.5, rely=0.8, anchor="center")

def register():
    app.destroy()
    subprocess.run(["python", "register.py"])

btn_register = CTkButton(master=frame, text="Đăng Kí", font=("Arial", 15), command=register)
btn_register.place(relx=0.5, rely=0.89, anchor="center")


app.mainloop()
