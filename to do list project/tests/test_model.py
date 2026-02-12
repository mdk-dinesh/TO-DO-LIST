import unittest
import os
import shutil
import json
from src.model import Task, TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        # Use a temporary directory for tests
        self.test_dir = "tests/data"
        os.makedirs(self.test_dir, exist_ok=True)
        self.storage_file = os.path.join(self.test_dir, "tasks.json")
        self.manager = TaskManager(self.storage_file)

    def tearDown(self):
        # Clean up
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_add_task(self):
        task = self.manager.add_task("Test Task", "Description")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(len(self.manager.list_tasks()), 1)

    def test_update_task(self):
        task = self.manager.add_task("Old Title")
        updated = self.manager.update_task(task.id, title="New Title", status="completed")
        self.assertEqual(updated.title, "New Title")
        self.assertEqual(updated.status, "completed")

    def test_delete_task(self):
        task = self.manager.add_task("To Delete")
        self.manager.delete_task(task.id)
        self.assertEqual(len(self.manager.list_tasks()), 0)

    def test_persistence(self):
        self.manager.add_task("Persistent Task")
        # Create a new manager instance to check if it loads from file
        new_manager = TaskManager(self.storage_file)
        self.assertEqual(len(new_manager.list_tasks()), 1)
        self.assertEqual(new_manager.list_tasks()[0].title, "Persistent Task")

if __name__ == '__main__':
    unittest.main()
