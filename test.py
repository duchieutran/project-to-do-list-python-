import customtkinter
from tkinter import ttk

# Create the main window
root = customtkinter.CTk()

# Create a style
style = ttk.Style()

# Configure the Treeview heading style
style.configure("Treeview.Heading", font=("Arial", 15, "bold"))

# Create a Treeview widget
tree = ttk.Treeview(root)

# Define the columns
tree["columns"] = ("Title", "Content", "Creator", "Start Time", "End Time")

# Format the columns
tree.column("#0", width=0, stretch=customtkinter.NO)
tree.column("Title", width=150, anchor="w")
tree.column("Content", width=300, anchor="w")
tree.column("Creator", width=100, anchor="w")
tree.column("Start Time", width=150, anchor="w")
tree.column("End Time", width=150, anchor="w")

# Create the column headings
tree.heading("#0", text="", anchor="w")
tree.heading("Title", text="Title", anchor="w")
tree.heading("Content", text="Content", anchor="w")
tree.heading("Creator", text="Creator", anchor="w")
tree.heading("Start Time", text="Start Time", anchor="w")
tree.heading("End Time", text="End Time", anchor="w")

# Insert data into the table
tree.insert("", customtkinter.END, values=("Project A", "Develop new feature", "Alice", "2024-01-01 09:00", "2024-01-01 17:00"))
tree.insert("", customtkinter.END, values=("Project B", "Bug fixes", "Bob", "2024-01-02 10:00", "2024-01-02 18:00"))
tree.insert("", customtkinter.END, values=("Project C", "Code review", "Charlie", "2024-01-03 11:00", "2024-01-03 15:00"))

# Pack the Treeview widget
tree.pack(expand=True, fill='both', padx=10, pady=10)

# Start the main loop
root.mainloop()
