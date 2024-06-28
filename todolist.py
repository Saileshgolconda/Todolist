import json
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# File to store tasks
TASKS_FILE = "tasks.json"

# Function to load tasks from a file
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save tasks to a file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

# Function to update the task list display
def update_task_list(filter_status="All"):
    task_list.delete(*task_list.get_children())
    for index, task in enumerate(tasks, start=1):
        status = "Done" if task["completed"] else "Pending"
        if filter_status == "All" or (filter_status == "Pending" and not task["completed"]) or (filter_status == "Completed" and task["completed"]):
            task_list.insert("", "end", iid=index, values=(index, task["title"], status))

# Function to add a new task
def add_task():
    title = simpledialog.askstring("Add Task", "Enter task title:")
    if title:
        tasks.append({"title": title, "completed": False})
        save_tasks(tasks)
        update_task_list(filter_var.get())

# Function to remove a task
def remove_task():
    selected_task = task_list.selection()
    if selected_task:
        task_index = int(task_list.item(selected_task)["values"][0]) - 1
        tasks.pop(task_index)
        save_tasks(tasks)
        update_task_list(filter_var.get())
    else:
        messagebox.showwarning("Remove Task", "Please select a task to remove.")

# Function to mark a task as completed
def complete_task():
    selected_task = task_list.selection()
    if selected_task:
        task_index = int(task_list.item(selected_task)["values"][0]) - 1
        tasks[task_index]["completed"] = True
        save_tasks(tasks)
        update_task_list(filter_var.get())
    else:
        messagebox.showwarning("Complete Task", "Please select a task to mark as completed.")

# Function to edit a task
def edit_task():
    selected_task = task_list.selection()
    if selected_task:
        task_index = int(task_list.item(selected_task)["values"][0]) - 1
        new_title = simpledialog.askstring("Edit Task", "Enter new task title:", initialvalue=tasks[task_index]["title"])
        if new_title:
            tasks[task_index]["title"] = new_title
            save_tasks(tasks)
            update_task_list(filter_var.get())
    else:
        messagebox.showwarning("Edit Task", "Please select a task to edit.")

# Main window setup
root = tk.Tk()
root.title("Enhanced To-Do List")
root.geometry("500x400")
root.resizable(False, False)

# Task list display with Treeview
columns = ("#", "Title", "Status")
task_list = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    task_list.heading(col, text=col)
    task_list.column(col, width=150)
task_list.pack(pady=10)

# Button frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Buttons
add_button = tk.Button(button_frame, text="Add Task", font=("Arial", 12), command=add_task, bg="#4CAF50", fg="white")
add_button.grid(row=0, column=0, padx=5)

remove_button = tk.Button(button_frame, text="Remove Task", font=("Arial", 12), command=remove_task, bg="#F44336", fg="white")
remove_button.grid(row=0, column=1, padx=5)

complete_button = tk.Button(button_frame, text="Complete Task", font=("Arial", 12), command=complete_task, bg="#2196F3", fg="white")
complete_button.grid(row=0, column=2, padx=5)

edit_button = tk.Button(button_frame, text="Edit Task", font=("Arial", 12), command=edit_task, bg="#FFC107", fg="black")
edit_button.grid(row=0, column=3, padx=5)

# Filter frame
filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)

filter_label = tk.Label(filter_frame, text="Filter tasks by status:", font=("Arial", 12))
filter_label.grid(row=0, column=0, padx=5)

filter_var = tk.StringVar(value="All")
filter_all = tk.Radiobutton(filter_frame, text="All", variable=filter_var, value="All", command=lambda: update_task_list(filter_var.get()))
filter_all.grid(row=0, column=1, padx=5)

filter_pending = tk.Radiobutton(filter_frame, text="Pending", variable=filter_var, value="Pending", command=lambda: update_task_list(filter_var.get()))
filter_pending.grid(row=0, column=2, padx=5)

filter_completed = tk.Radiobutton(filter_frame, text="Completed", variable=filter_var, value="Completed", command=lambda: update_task_list(filter_var.get()))
filter_completed.grid(row=0, column=3, padx=5)

# Load tasks and update display
tasks = load_tasks()
update_task_list()

root.mainloop()
