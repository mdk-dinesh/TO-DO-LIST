import argparse
from .model import TaskManager

def run_cli():
    manager = TaskManager()
    parser = argparse.ArgumentParser(description="To-Do List CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--desc", help="Task description", default="")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--all", action="store_true", help="Show all tasks including completed")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("--title", help="New title")
    update_parser.add_argument("--desc", help="New description")
    update_parser.add_argument("--status", choices=["pending", "completed"], help="New status")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("id", type=int, help="Task ID")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.command == "add":
        task = manager.add_task(args.title, args.desc)
        print(f"Task added: [{task.id}] {task.title}")

    elif args.command == "list":
        tasks = manager.list_tasks()
        if not tasks:
            print("No tasks found.")
        else:
            print(f"{'ID':<5} {'Status':<12} {'Title':<30} {'Description'}")
            print("-" * 60)
            for task in tasks:
                if not args.all and task.status == "completed":
                    continue
                print(f"{task.id:<5} {task.status:<12} {task.title:<30} {task.description}")

    elif args.command == "update":
        task = manager.update_task(args.id, title=args.title, description=args.desc, status=args.status)
        if task:
            print(f"Task updated: [{task.id}] {task.title}")
        else:
            print(f"Task with ID {args.id} not found.")

    elif args.command == "complete":
        task = manager.update_task(args.id, status="completed")
        if task:
            print(f"Task marked as completed: [{task.id}] {task.title}")
        else:
            print(f"Task with ID {args.id} not found.")

    elif args.command == "delete":
        if manager.delete_task(args.id):
            print(f"Task {args.id} deleted.")
        else:
            print(f"Task with ID {args.id} not found.")

    else:
        parser.print_help()
