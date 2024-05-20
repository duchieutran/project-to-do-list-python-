import os
import sys
import subprocess
import tkinter.messagebox as mbox
import customtkinter
from setting import *
from PIL import Image
from tkinter import ttk


import mysql.connector

# def check_login_status():
#     # Kiểm tra trạng thái đăng nhập
#     if os.environ.get("LOGGED_IN") != "true":
#         mbox.showinfo("Thông báo", "Bạn chưa đăng nhập tài khoản!")
#         sys.exit()

# check_login_status()

with open("log.txt", "r") as f:
    username = f.read().strip()

try:
    # Kết nối tới cơ sở dữ liệu MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Thay thế bằng tên đăng nhập MySQL của bạn
        password="",  # Thay thế bằng mật khẩu MySQL của bạn
        database="to_do_list"
    )

    cursor = conn.cursor()

    # Truy vấn dữ liệu
    cursor.execute("SELECT id, created_at, status, role FROM account WHERE account = %s", (username,))
    user_data = cursor.fetchone()

    # Đóng kết nối cơ sở dữ liệu
    conn.close()

except mysql.connector.Error as err:
    mbox.showerror("Lỗi", f"Không thể kết nối tới cơ sở dữ liệu: {err}")
    sys.exit()

id_name = user_data[0]
date_create = user_data[1]
status = user_data[2]
role = user_data[3]

app = CTk()
app.geometry(geometry_main)
app.title("Trang Chủ")

# Hiển thị thông tin người dùng trong tab hồ sơ
info_username = CTkLabel(master=app, text=f"Xin chào, {username}", font=("Arial", 14))
info_username.place(relx=0.95, rely=0.05, anchor="ne")

tab_menu = customtkinter.CTkTabview(app, width=1200, height=680)
tab_menu.pack(padx=30, pady=100)

tab_menu.add("     Thêm công việc     ")
tab_menu.add("     Danh sách công việc     ")
tab_menu.add("     Học tiếng Anh     ")
tab_menu.add("     Hồ sơ     ")

tab_menu.set("     Hồ sơ     ")

avt_img = customtkinter.CTkImage(light_image=Image.open("D:/_chuyenmon/Python/project_1/img/icon.png"),
                                 dark_image=Image.open("D:/_chuyenmon/Python/project_1/img/icon.png"),
                                 size=(50, 50))
image_label_avt = customtkinter.CTkLabel(master=tab_menu.tab("     Hồ sơ     "),
                                         image=avt_img, text="")
image_label_avt.pack(padx=20, pady=20)

info_id = customtkinter.CTkLabel(master=tab_menu.tab("     Hồ sơ     "),
                                   text=f"Mã người dùng : #{id_name}", font=("Arial", 16), text_color="blue")
info_id.pack(padx=20, pady=3)

info_name = customtkinter.CTkLabel(master=tab_menu.tab("     Hồ sơ     "),
                                   text=f"Tài khoản : {username}", font=("Arial", 20), text_color="red")
info_name.pack(padx=20, pady=5)

info_date_create = customtkinter.CTkLabel(master=tab_menu.tab("     Hồ sơ     "),
                                         text=f"Ngày tạo : {date_create}", font=("Arial", 16), text_color="blue")
info_date_create.pack(padx=20, pady=3)

if status == "active":
    info_status = customtkinter.CTkLabel(master=tab_menu.tab("     Hồ sơ     "),
                                        text="Trạng thái: Hoạt động", font=("Arial", 16), text_color="green")
else:
    info_status = customtkinter.CTkLabel(master=tab_menu.tab("     Hồ sơ     "),
                                        text="Trạng thái: Không hoạt động", font=("Arial", 16), text_color="red")

info_status.pack(padx=20, pady=3)

if role == "admin":
    info_role = customtkinter.CTkLabel(master=tab_menu.tab("     Hồ sơ     "),
                                      text="Vai trò: Quản trị viên", 
                                      font=("Arial", 16), 
                                      text_color="green")
else:
    info_role = customtkinter.CTkLabel(master=tab_menu.tab("     Hồ sơ     "),
                                      text="Vai trò: Người dùng", font=("Arial", 16), text_color="blue")
info_role.pack(padx=20, pady=3)

button_frame = CTkFrame(master=tab_menu.tab("     Hồ sơ     "))
button_frame.pack(padx=20, pady=10)


if role == "admin":
    admin_button = customtkinter.CTkButton(master=button_frame, text="Trang Admin")
    admin_button.pack(side="left", padx=5)

def delete_account():
    # Hiển thị popup xác nhận xóa tài khoản
    confirm = mbox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa tài khoản không?")
    if confirm:
        try:
            # Kết nối tới cơ sở dữ liệu MySQL
            conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Thay thế bằng tên đăng nhập MySQL của bạn
                password="",  # Thay thế bằng mật khẩu MySQL của bạn
                database="to_do_list"
            )

            cursor = conn.cursor()

            # Xóa tài khoản từ cơ sở dữ liệu
            cursor.execute("DELETE FROM account WHERE account = %s", (username,))
            conn.commit()

            # Đóng kết nối cơ sở dữ liệu
            conn.close()

            mbox.showinfo("Thông báo", "Xóa tài khoản thành công!")
            app.destroy()
            subprocess.run(["python", "login.py"])
            os.environ["LOGGED_IN"] = "false"

        except mysql.connector.Error as err:
            mbox.showerror("Lỗi", f"Lỗi khi xóa tài khoản: {err}")

delete_button = customtkinter.CTkButton(master=button_frame, text="Xóa tài khoản", command=delete_account)
delete_button.pack(side="left", padx=5)

def logout():
    app.destroy()
    subprocess.run(["python", "login.py"])
    os.environ["LOGGED_IN"] = "false"

logout_button = customtkinter.CTkButton(master=button_frame, text="Đăng xuất", command=logout)
logout_button.pack(side="left", padx=5)

def toggle_appearance_mode():
    if toggle_button.cget("text") == "Sáng":
        customtkinter.set_appearance_mode("light")
        toggle_button.configure(text="Tối")
    else:
        customtkinter.set_appearance_mode("dark")
        toggle_button.configure(text="Sáng")

toggle_button = customtkinter.CTkButton(master=app, text="Sáng", command=toggle_appearance_mode)
toggle_button.place(relx=0.05, rely=0.05)


# --------------------- Tạo công việc ---------------------
# trong danh sách công việc , tôi muốn tạo 1 from để nhập công việc mới, sau đó lưu vào cơ sỏ dữ liệu với bảng tast_list gồm các thông tin là: task_title, task_content, task_date, task_time, task_status
def save_task():
    title = task_title_entry.get()
    content = task_content_entry.get()
    start_date = task_start_date_entry.get()  # Change variable name to start_date
    end_date = task_end_date_entry.get()  # Add end_date variable

    try:
        # Kết nối tới cơ sở dữ liệu MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Thay thế bằng tên đăng nhập MySQL của bạn
            password="",  # Thay thế bằng mật khẩu MySQL của bạn
            database="to_do_list"
        )

        cursor = conn.cursor()

        # Thêm công việc vào bảng task_list
        cursor.execute("INSERT INTO task_list (task_title, task_content,creator_name, start_time, end_time) VALUES (%s, %s, %s, %s, %s)",
                       (title, content, username, start_date, end_date))
        conn.commit()

        # Đóng kết nối cơ sở dữ liệu
        conn.close()

        mbox.showinfo("Thông báo", "Thêm công việc thành công!")

        # Clear the input fields
        task_title_entry.delete(0, "end")
        task_content_entry.delete(0, "end")
        task_start_date_entry.delete(0, "end")  # Change variable name to task_start_date_entry
        task_end_date_entry.delete(0, "end")  # Add task_end_date_entry

    except mysql.connector.Error as err:
        mbox.showerror("Lỗi", f"Lỗi khi thêm công việc: {err}")

# Tạo form để nhập công việc mới
task_form_frame = CTkFrame(master=tab_menu.tab("     Thêm công việc     "))
task_form_frame.pack(padx=20, pady=20)

task_title_label = customtkinter.CTkLabel(master=task_form_frame, text="Tiêu đề công việc:")
task_title_label.pack()

task_title_entry = customtkinter.CTkEntry(master=task_form_frame, width=300)  # Increase the width of the entry
task_title_entry.pack(pady=5)

task_content_label = customtkinter.CTkLabel(master=task_form_frame, text="Nội dung công việc:")
task_content_label.pack()

task_content_entry = customtkinter.CTkEntry(master=task_form_frame, width=300)  # Increase the width of the entry
task_content_entry.pack(pady=5)

task_start_date_label = customtkinter.CTkLabel(master=task_form_frame, text="Ngày bắt đầu (YYYY-MM-DD):")  # Change label text
task_start_date_label.pack()

task_start_date_entry = customtkinter.CTkEntry(master=task_form_frame, width=300)  # Increase the width of the entry
task_start_date_entry.pack(pady=5)

task_end_date_label = customtkinter.CTkLabel(master=task_form_frame, text="Ngày kết thúc (YYYY-MM-DD):")  # Add new label
task_end_date_label.pack()

task_end_date_entry = customtkinter.CTkEntry(master=task_form_frame, width=300)  # Increase the width of the entry
task_end_date_entry.pack(pady=5)

save_button = customtkinter.CTkButton(master=task_form_frame, text="Lưu công việc", command=save_task)
save_button.pack(pady=10)


# --------------------- Danh sách công việc ---------------------
# hiển thị danh sách công việc từ bảng task_list

# chưa build xong


app.mainloop()
 