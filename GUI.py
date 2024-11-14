import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from Classes import Task
from Database import DatabaseManager



class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        
        # Initialize Database Manager
        self.db_manager = DatabaseManager()
        
        # Set up main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=20, padx=20)
        
        # Widgets for Task Entry
        tk.Label(self.main_frame, text="Task Name:").grid(row=0, column=0, sticky="e")
        self.name_entry = tk.Entry(self.main_frame)
        self.name_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.main_frame, text="Deadline (YYYY-MM-DD HH:MM):").grid(row=1, column=0, sticky="e")
        self.deadline_entry = tk.Entry(self.main_frame)
        self.deadline_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.main_frame, text="Priority:").grid(row=2, column=0, sticky="e")
        self.priority_entry = tk.Entry(self.main_frame)
        self.priority_entry.grid(row=2, column=1, pady=5)

        tk.Label(self.main_frame, text="To-Do List:").grid(row=3, column=0, sticky="e")
        self.todolist_entry = tk.Entry(self.main_frame)
        self.todolist_entry.grid(row=3, column=1, pady=5)

        tk.Label(self.main_frame, text="Notes:").grid(row=4, column=0, sticky="e")
        self.notes_entry = tk.Entry(self.main_frame)
        self.notes_entry.grid(row=4, column=1, pady=5)

        tk.Label(self.main_frame, text="Time Zone:").grid(row=5, column=0, sticky="e")
        self.timezone_entry = tk.Entry(self.main_frame)
        self.timezone_entry.grid(row=5, column=1, pady=5)

        # Buttons for CRUD operations
        tk.Button(self.main_frame, text="Add Task", command=self.add_task).grid(row=6, column=0, pady=10)
        tk.Button(self.main_frame, text="View All Tasks", command=self.view_tasks).grid(row=6, column=1, pady=10)
        tk.Button(self.main_frame, text="Delete Task", command=self.delete_task).grid(row=7, column=0, pady=10)
        tk.Button(self.main_frame, text="Update Task", command=self.update_task).grid(row=7, column=1, pady=10)

        # Treeview to display tasks
        self.task_list = ttk.Treeview(self.main_frame, columns=("Name", "Deadline", "Priority", "Todolist", "Notes", "Completed", "Timezone"), show="headings")
        self.task_list.heading("Name", text="Name")
        self.task_list.heading("Deadline", text="Deadline")
        self.task_list.heading("Priority", text="Priority")
        self.task_list.heading("Todolist", text="To-Do List")
        self.task_list.heading("Notes", text="Notes")
        self.task_list.heading("Completed", text="Completed")
        self.task_list.heading("Timezone", text="Timezone")
        self.task_list.grid(row=8, column=0, columnspan=2, pady=20)
        
        # Populate initial task list
        self.view_tasks()

    def add_task(self):
        """Add a new task to the database."""
        name = self.name_entry.get()
        deadline = self.deadline_entry.get()
        priority = self.priority_entry.get()
        todolist = self.todolist_entry.get()
        notes = self.notes_entry.get()
        timezone = self.timezone_entry.get()
        
        # Create task object
        try:
            task = Task(name=name, deadline=deadline, priority=priority, notes=notes, todolist=todolist, time_zone=timezone)
            self.db_manager.add_task(task)
            messagebox.showinfo("Success", "Task added successfully!")
            self.view_tasks()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def view_tasks(self):
        """Display all tasks from the database."""
        for row in self.task_list.get_children():
            self.task_list.delete(row)
        
        tasks = self.db_manager.get_all_tasks()
        for task in tasks:
            self.task_list.insert("", "end", values=(task.name, 
                                                     task.deadline.strftime('%Y-%m-%d %H:%M') if task.deadline else "No deadline", 
                                                     task.priority, 
                                                     task.todolist, 
                                                     task.notes, 
                                                     "Yes" if task.completed else "No", 
                                                     task.time_zone))

    def delete_task(self):
        """Delete the selected task."""
        selected_item = self.task_list.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to delete.")
            return
        task_name = self.task_list.item(selected_item)["values"][0]
        self.db_manager.delete_task(task_name)
        messagebox.showinfo("Success", f"Task '{task_name}' deleted.")
        self.view_tasks()

    def update_task(self):
        """Update an existing task."""
        selected_item = self.task_list.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to update.")
            return
        task_name = self.task_list.item(selected_item)["values"][0]
        
        # Fetch new data from entry fields
        deadline = self.deadline_entry.get()
        priority = self.priority_entry.get()
        todolist = self.todolist_entry.get()
        notes = self.notes_entry.get()
        timezone = self.timezone_entry.get()
        
        # Update task object and database
        task = self.db_manager.get_task(task_name)
        if task:
            task.deadline = task.parse_deadline(deadline)
            task.priority = task.set_priority(priority)
            task.todolist = todolist
            task.notes = notes
            task.time_zone = timezone
            self.db_manager.update_task(task)
            messagebox.showinfo("Success", f"Task '{task_name}' updated.")
            self.view_tasks()
        else:
            messagebox.showerror("Error", f"Task '{task_name}' not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
