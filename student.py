import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from datetime import datetime

STUDENT_FILE = "students.csv"
ATTENDANCE_FILE = "attendance.csv"

# Create CSV files if not exist
def initialize_files():
    if not os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Roll", "Name"])

    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Roll", "Name", "Status"])

initialize_files()

# ------------------- MAIN WINDOW -------------------
root = tk.Tk()
root.title("Student Attendance Management System")
root.geometry("900x500")
root.configure(bg="#f0f0f0")

# ------------------- FRAMES -------------------
side_frame = tk.Frame(root, width=200, bg="#2c3e50")
side_frame.pack(side="left", fill="y")

main_frame = tk.Frame(root, bg="white")
main_frame.pack(side="right", expand=True, fill="both")

# ------------------- FUNCTIONS -------------------

def clear_main():
    for widget in main_frame.winfo_children():
        widget.destroy()

# ---------- Add Student ----------
def add_student_screen():
    clear_main()

    tk.Label(main_frame, text="Add Student", font=("Arial", 18)).pack(pady=20)

    tk.Label(main_frame, text="Roll No:").pack()
    roll_entry = tk.Entry(main_frame)
    roll_entry.pack()

    tk.Label(main_frame, text="Name:").pack()
    name_entry = tk.Entry(main_frame)
    name_entry.pack()

    def save_student():
        roll = roll_entry.get()
        name = name_entry.get()

        if roll == "" or name == "":
            messagebox.showerror("Error", "All fields required!")
            return

        with open(STUDENT_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([roll, name])

        messagebox.showinfo("Success", "Student Added Successfully!")
        roll_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)

    tk.Button(main_frame, text="Save", bg="green", fg="white",
              command=save_student).pack(pady=10)

# ---------- Mark Attendance ----------
def mark_attendance_screen():
    clear_main()

    tk.Label(main_frame, text="Mark Attendance",
             font=("Arial", 18)).pack(pady=20)

    tree = ttk.Treeview(main_frame, columns=("Roll", "Name", "Status"),
                        show="headings")

    tree.heading("Roll", text="Roll")
    tree.heading("Name", text="Name")
    tree.heading("Status", text="Status")

    tree.pack(expand=True, fill="both")

    students = []
    with open(STUDENT_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            students.append(row)

    for student in students:
        tree.insert("", "end", values=(student[0], student[1], "Present"))

    def save_attendance():
        date = datetime.now().strftime("%Y-%m-%d")

        with open(ATTENDANCE_FILE, "a", newline="") as f:
            writer = csv.writer(f)

            for item in tree.get_children():
                roll, name, status = tree.item(item)["values"]
                writer.writerow([date, roll, name, status])

        messagebox.showinfo("Success", "Attendance Saved!")

    def toggle_status(event):
        selected = tree.focus()
        values = tree.item(selected, "values")

        if values:
            new_status = "Absent" if values[2] == "Present" else "Present"
            tree.item(selected, values=(values[0], values[1], new_status))

    tree.bind("<Double-1>", toggle_status)

    tk.Button(main_frame, text="Save Attendance",
              bg="blue", fg="white",
              command=save_attendance).pack(pady=10)

# ---------- View Attendance ----------
def view_attendance_screen():
    clear_main()

    tk.Label(main_frame, text="Attendance Records",
             font=("Arial", 18)).pack(pady=20)

    tree = ttk.Treeview(main_frame,
                        columns=("Date", "Roll", "Name", "Status"),
                        show="headings")

    tree.heading("Date", text="Date")
    tree.heading("Roll", text="Roll")
    tree.heading("Name", text="Name")
    tree.heading("Status", text="Status")

    tree.pack(expand=True, fill="both")

    with open(ATTENDANCE_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            tree.insert("", "end", values=row)

# ------------------- SIDE MENU -------------------

tk.Label(side_frame, text="MENU",
         bg="#2c3e50", fg="white",
         font=("Arial", 16)).pack(pady=20)

tk.Button(side_frame, text="Add Student",
          width=20, command=add_student_screen).pack(pady=10)

tk.Button(side_frame, text="Mark Attendance",
          width=20, command=mark_attendance_screen).pack(pady=10)

tk.Button(side_frame, text="View Attendance",
          width=20, command=view_attendance_screen).pack(pady=10)

tk.Button(side_frame, text="Exit",
          width=20, command=root.quit).pack(pady=10)

# Start with Add Student screen
add_student_screen()

root.mainloop()