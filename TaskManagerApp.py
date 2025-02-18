import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import json
import os

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Task Manager")
        self.root.geometry("500x400")

        # Task list
        self.tasks = []

        # Load tasks from file if it exists
        self.load_tasks()

        # GUI Components
        self.create_widgets()

    def create_widgets(self):
        # Task Entry Frame
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Task Description:").grid(row=0, column=0, padx=5)
        self.task_entry = tk.Entry(entry_frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=5)

        tk.Label(entry_frame, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5)
        self.due_date_entry = tk.Entry(entry_frame, width=30)
        self.due_date_entry.grid(row=1, column=1, padx=5)

        add_button = tk.Button(entry_frame, text="Add Task", command=self.add_task)
        add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Task List Frame
        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=10)

        self.task_listbox = ttk.Treeview(list_frame, columns=("Description", "Due Date", "Status"), show="headings")
        self.task_listbox.heading("Description", text="Description")
        self.task_listbox.heading("Due Date", text="Due Date")
        self.task_listbox.heading("Status", text="Status")
        self.task_listbox.pack()

        # Buttons Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        complete_button = tk.Button(button_frame, text="Mark as Complete", command=self.mark_complete)
        complete_button.pack(side=tk.LEFT, padx=5)

        sort_button = tk.Button(button_frame, text="Sort by Due Date", command=self.sort_tasks)
        sort_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="Delete Task", command=self.delete_task)
        delete_button.pack(side=tk.LEFT, padx=5)

        # Load tasks into the listbox
        self.update_task_listbox()

    def add_task(self):
        description = self.task_entry.get().strip()
        due_date = self.due_date_entry.get().strip()

        if not description or not due_date:
            messagebox.showwarning("Input Error", "Please fill in both task description and due date.")
            return

        try:
            # Validate date format
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Date Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        # Add task to the list
        self.tasks.append({
            "description": description,
            "due_date": due_date,
            "status": "Pending"
        })

        # Clear input fields
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)

        # Update the task listbox
        self.update_task_listbox()

        # Save tasks to file
        self.save_tasks()

    def mark_complete(self):
        selected_task = self.task_listbox.selection()
        if not selected_task:
            messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")
            return

        # Get the selected task index
        task_index = self.task_listbox.index(selected_task)
        self.tasks[task_index]["status"] = "Completed"

        # Update the task listbox
        self.update_task_listbox()

        # Save tasks to file
        self.save_tasks()

    def delete_task(self):
        selected_task = self.task_listbox.selection()
        if not selected_task:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return

        # Get the selected task index
        task_index = self.task_listbox.index(selected_task)
        del self.tasks[task_index]

        # Update the task listbox
        self.update_task_listbox()

        # Save tasks to file
        self.save_tasks()

    def sort_tasks(self):
        # Sort tasks by due date
        self.tasks.sort(key=lambda x: x["due_date"])

        # Update the task listbox
        self.update_task_listbox()

    def update_task_listbox(self):
        # Clear the listbox
        for row in self.task_listbox.get_children():
            self.task_listbox.delete(row)

        # Add tasks to the listbox
        for task in self.tasks:
            self.task_listbox.insert("", tk.END, values=(task["description"], task["due_date"], task["status"]))

    def save_tasks(self):
        # Save tasks to a JSON file
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        # Load tasks from a JSON file if it exists
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)

# Main application loop
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()