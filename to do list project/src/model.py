import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class Task:
    def __init__(self, title: str, description: str = "", status: str = "pending", created_at: str = None, id: int = None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at if created_at else datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Task':
        return Task(
            id=data.get("id"),
            title=data.get("title"),
            description=data.get("description", ""),
            status=data.get("status", "pending"),
            created_at=data.get("created_at")
        )

class TaskManager:
    def __init__(self, storage_file: str = "data/tasks.json"):
        self.storage_file = storage_file
        self.tasks: List[Task] = []
        self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.storage_file):
            return
        
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(t) for t in data]
        except (json.JSONDecodeError, IOError):
            self.tasks = []

    def save_tasks(self):
        data = [t.to_dict() for t in self.tasks]
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=4)

    def add_task(self, title: str, description: str = "") -> Task:
        new_id = 1 if not self.tasks else max(t.id for t in self.tasks) + 1
        task = Task(title=title, description=description, id=new_id)
        self.tasks.append(task)
        self.save_tasks()
        return task

    def update_task(self, task_id: int, title: str = None, description: str = None, status: str = None) -> Optional[Task]:
        task = self.get_task(task_id)
        if task:
            if title is not None: task.title = title
            if description is not None: task.description = description
            if status is not None: task.status = status
            self.save_tasks()
        return task

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False

    def get_task(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def list_tasks(self) -> List[Task]:
        return self.tasks
