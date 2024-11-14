import sqlite3
from task import Task  # Import the Task class from your file
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="tasks.db"):
        """Initialize the database connection and create tasks table if it doesn't exist."""
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self):
        """Create the tasks table in the database if it doesn't already exist."""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    name TEXT PRIMARY KEY,
                    deadline TEXT,
                    priority TEXT,
                    todolist TEXT,
                    notes TEXT,
                    completed INTEGER,
                    time_zone TEXT
                )
            """)

    def add_task(self, task: Task):
        """Add a new task to the database."""
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO tasks (name, deadline, priority, todolist, notes, completed, time_zone)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, task.to_tuple() + (1 if task.completed else 0, task.time_zone))

    def get_task(self, name: str) -> Task:
        """Retrieve a task by name."""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE name = ?", (name,))
        row = cur.fetchone()
        return Task.from_row(row) if row else None

    def get_all_tasks(self):
        """Retrieve all tasks from the database."""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks")
        rows = cur.fetchall()
        return [Task.from_row(row) for row in rows]

    def delete_task(self, name: str):
        """Delete a task from the database by name."""
        with self.conn:
            self.conn.execute("DELETE FROM tasks WHERE name = ?", (name,))

    def update_task(self, task: Task):
        """Update an existing task's details in the database."""
        with self.conn:
            self.conn.execute("""
                UPDATE tasks
                SET deadline = ?, priority = ?, todolist = ?, notes = ?, completed = ?, time_zone = ?
                WHERE name = ?
            """, (task.deadline.strftime('%Y-%m-%d %H:%M') if task.deadline else None,
                  task.priority, task.todolist, task.notes, 1 if task.completed else 0, task.time_zone, task.name))

    def close(self):
        """Close the database connection."""
        self.conn.close()