import sqlite3
import calendar
import argparse
from datetime import datetime
current_date=datetime.now()

class Task():
    def __init__(self,name:str,deadline:str=None, priority:str=None,notes:str="", todolist:str="General"):
        self.name=name
        self.deadline = self.parse_deadline(deadline)
        valid_priorities=['low','medium','high']
        #Aggiungere attributo fuso orario
        self.priority = self.set_priority(priority)
        self.todolist=todolist
        self.notes=notes
        self.completed = False

    def parse_todolist(self, todolist:str):
        """1. Se esiste la todolist aggiunge la task alla todolist 2. se no la aggiunge alla todolist General"""
        #TBC DA FARE

    #Nella GUI non ti chiede la priority, ma te la da come opzionale nel widget
    def set_priority(self, priority: str) -> str:
        """Sets task priority only if it’s valid, otherwise asks for a valid priority repeatedly."""
        while priority not in self.valid_priorities:
            print(f"Invalid priority '{priority}'. Please enter a valid priority.")
            priority = input("Enter task priority (low, medium, high) or leave blank for 'low': ").lower().strip() or None #TBC se il None così va abene
        return priority

    #Nella GUI non ti chiede la deadline, ma te la da come opzionale nel widget
    def parse_deadline(self, deadline_input: str) -> datetime:
        """Parses the deadline input string to a datetime object, prompting repeatedly until valid."""
        while True:
            if not deadline_input:
                return None
            try:
                return datetime.strptime(deadline_input, '%Y-%m-%d %H:%M')
            except ValueError:
                print("Invalid date format. Please enter the deadline in the format YYYY-MM-DD HH:MM.")
                deadline_input = input("Enter a valid task deadline (YYYY-MM-DD HH:MM) or leave blank for no deadline: ")

     def mark_completed(self):
        """Marks the task as completed."""
        self.completed = True

    #AGGIORNARE __str___
    def __str__(self):
        status = "Completed" if self.completed else "Incomplete"
        deadline_str = self.deadline.strftime('%Y-%m-%d %H:%M') if self.deadline else "No deadline"
        return (f"Task: {self.title}\n  Status: {status}\n  Deadline: {deadline_str}\n"
                f"  Priority: {self.priority}\n  Notes: {self.notes}")

    def represent(self):
        return (f'Name:{self.name}; Priority:{self.priority}; Deadline:{self.deadline}; To-Do list:{self.todolist}; Notes:{self.notes}')
    def to_tuple(self):
        return (self.name, self.deadline.strftime('%d-%m-%Y'), self.priority, self.todolist, self.notes) #tbc RESIDUO DI JSON

    @staticmethod
    def from_row(row):
        return Task(
            name=row[0],
            deadline=row[1],
            priority=row[2],
            todolist=row[3],
            notes=row[4]
        )



#########################################################################################

class ToDoList():
    def __init__(self,name):
        self.name=name
        self.todo_list={}

#METODI E ATTRIBUTI PER UNA TODOLIST
#1 Si crei un databes o la todilist venga aggiunta a un database madre
#2 add/remove task

class ListToDos():
#METODI E ATTRIBUTI PER UNA TODOLIST

# Today view
# View per scadenza
# VIew per priorità
































        self.db_name='todolist.db'
    def create_table(self):
        """Create tasks table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                name TEXT PRIMARY KEY,
                deadline TEXT,
                priority TEXT,
                category TEXT,
                notes TEXT
            )
            ''')
            conn.commit()

    def add_task(self,task):
        """Add a task to the database and load it into memory."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT OR REPLACE INTO tasks (name, deadline, priority, category, notes)
            VALUES (?, ?, ?, ?, ?)
            ''', task.to_tuple())
            conn.commit()
        self.todo_list[task.name]=task
    def rem_task(self,task):
        """Remove a task from the database and memory."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE name = ?', (task.name,))
            conn.commit()
        del self.todo_list[task.name]
    def get_todo(self):
        return[task.represent() for task in self.todo_list.values()]
    def filter_by_category(self,category):
        return [task.represent() for task in self.todo_list.values() if task.category == category]
    def filter_by_deadline(self,deadline):
        formatted_deadline=datetime.strptime(deadline,'%d-%m-%Y')
        return[task.represent() for task in self.todo_list.values() if task.deadline==formatted_deadline]
    def order_by_deadline(self):
        sorted_todo_list_byd = sorted(self.todo_list.values(), key=lambda task: task.deadline)
        return[task.represent() for task in sorted_todo_list_byd]
    def filter_by_priority(self,priority):
        return[task.represent() for task in self.todo_list.values() if task.priority==priority]
    def order_by_priority(self):
        priority_order = {
        'high': 0,
        'medium': 1,
        'low': 2
    }
        sorted_todo_list_byp = sorted(self.todo_list.values(), key=lambda task: priority_order.get(task.priority, 3))
        return[task.represent() for task in sorted_todo_list_byp]
    def load_tasks(self):
        """Load tasks from the database into memory."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks')
            rows = cursor.fetchall()
            for row in rows:
                task = Task.from_row(row)
                self.todo_list[task.name] = task
    def show_calendar(self,year,month=current_date.month):
        cal=calendar.TextCalendar(calendar.SUNDAY)
        cal_str=cal.formatmonth(year,month)
        print(cal_str)
        found_tasks=False
        for task in self.todo_list.values():
            if task.deadline.month==month and task.deadline.year==year:
                day=task.deadline.day
                found_tasks=True
                print(f'Task "{task.name}" on {day}-{month}-{year}: {task.represent()}')
        if found_tasks==False:
            raise ValueError(f'No tasks found for {month} {year}')
