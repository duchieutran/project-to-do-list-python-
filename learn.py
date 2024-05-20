task_table = customtkinter.CTkLabel(master=tab_menu.tab("     Danh sách công việc     "), text="Danh sách công việc")
task_table.pack(padx=20, pady=20)

def load_tasks():
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
        cursor.execute("SELECT task_title, task_content, start_time, end_time , status FROM task_list WHERE creator_name = %s", (username,))
        list_data = cursor.fetchall()

        # Đóng kết nối cơ sở dữ liệu
        conn.close()

        # Hiển thị danh sách công việc
        task_table = ttk.Treeview(master=tab_menu.tab("     Danh sách công việc     "))
        task_table.pack(padx=2, pady=2)

        # Xóa dữ liệu cũ trong bảng
        task_table.config(text="Danh sách công việc\n")

        task_table["columns"] = ("Title", "Content", "Date", "Time", "Status")
        task_table.column("#0", width=0, stretch="no")
        task_table.column("Title", width=150)
        task_table.column("Content", width=200)
        task_table.column("Date", width=100)
        task_table.column("Time", width=100)
        task_table.column("Status", width=100)

        task_table.heading("#0", text="", anchor="w")
        task_table.heading("Title", text="Title", anchor="w")
        task_table.heading("Content", text="Content", anchor="w")
        task_table.heading("Date", text="Date", anchor="w")
        task_table.heading("Time", text="Time", anchor="w")
        task_table.heading("Status", text="Status", anchor="w")

        for task in list_data:
            task_title = task[0]
            task_content = task[1]
            task_date = task[2]
            task_time = task[3]
            task_status = task[4]

            task_table.insert("", "end", text="", values=(task_title, task_content, task_date, task_time, task_status))

    except mysql.connector.Error as err:
        mbox.showerror("Lỗi", f"Lỗi khi tải danh sách công việc: {err}")

# Tạo nút để tải danh sách công việc
load_button = customtkinter.CTkButton(master=tab_menu.tab("     Danh sách công việc     "), text="Tải danh sách công việc", command=load_tasks)
load_button.pack(pady=10)