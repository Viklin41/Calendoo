from datetime import datetime
import pytz

class Task:
    def __init__(self, name: str, deadline: str = None, priority: str = "low", notes: str = "", todolist: str = "General", time_zone: str = "UTC"):
        self.name = name
        self.deadline = self.parse_deadline(deadline)
        self.priority = self.set_priority(priority)
        self.todolist = self.parse_todolist(todolist)
        self.notes = notes
        self.completed = False
        self.time_zone = time_zone

    def set_priority(self, priority: str) -> str:
        """Sets the task priority, defaults to 'low' if unspecified or invalid."""
        valid_priorities = ['low', 'medium', 'high']
        return priority.lower() if priority in valid_priorities else "low"

    def parse_deadline(self, deadline_input: str) -> datetime:
        """Converts deadline input to a datetime object, with timezone awareness."""
        if not deadline_input:
            return None
        try:
            return datetime.strptime(deadline_input, '%Y-%m-%d %H:%M').replace(tzinfo=pytz.timezone(self.time_zone))
        except ValueError:
            raise ValueError("Invalid date format. Use 'YYYY-MM-DD HH:MM'.")

    def parse_todolist(self, todolist: str):
        """Checks if a todolist exists; if not, creates a new 'General' list."""
        # Assuming a TodolistManager class or a similar mechanism exists to track lists
        if todolist:  # Check for an existing list by name; return 'General' if not found
            return todolist
        return "General"

    def mark_completed(self):
        """Marks the task as completed."""
        self.completed = True

    def __str__(self):
        """String representation for CLI display."""
        deadline_str = self.deadline.strftime('%Y-%m-%d %H:%M') if self.deadline else "No deadline"
        status = "Completed" if self.completed else "Incomplete"
        return f"[{status}] Task: {self.name} | Priority: {self.priority} | Deadline: {deadline_str} | Notes: {self.notes}"

    # Potentially useful serialization methods
    def to_tuple(self):
        """Convert task attributes to a tuple for database insertion or serialization."""
        deadline_str = self.deadline.strftime('%Y-%m-%d %H:%M') if self.deadline else None
        return (self.name, deadline_str, self.priority, self.todolist, self.notes)

    @staticmethod
    def from_row(row):
        """Create a Task object from a database row or similar iterable."""
        return Task(
            name=row[0],
            deadline=row[1],
            priority=row[2],
            todolist=row[3],
            notes=row[4]
        )
