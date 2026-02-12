import tkinter as tk
from tkinter import messagebox, simpledialog
from .model import TaskManager
import random

class TodoApp:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("600x500") # Slightly larger for spacing
        self.root.resizable(False, False) # Keep it fixed for simple animation logic

        # Colors - Cream Theme
        self.bg_base = "#FFFDD0" # Cream
        self.bg_dark = "#F5F5DC" # Beige
        self.fg_color = "#4E342E" # Dark Brown text (warm contrast)
        self.btn_bg = "#FFE0B2"   # Light Orange/Peach
        self.btn_hover = "#FFCC80" # Darker Orange/Peach
        self.accent = "#EF6C00"   # Deep Orange accent

        # 1. Background Canvas
        self.canvas = tk.Canvas(self.root, bg=self.bg_base, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 2. Floating Objects (Bubbles)
        self.shapes = []
        for _ in range(10):
            x = random.randint(0, 600)
            y = random.randint(0, 500)
            size = random.randint(20, 80)
            # Create semi-transparent-looking circles (using stipple or just colors)
            # Tkinter transparency is hard, so we use different shades of gray/black
            color = random.choice(["#000000", "#1a1a1a", "#333333"])
            obj = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            dx = random.choice([-1, 1]) * random.uniform(0.5, 2)
            dy = random.choice([-1, 1]) * random.uniform(0.5, 2)
            self.shapes.append({'id': obj, 'dx': dx, 'dy': dy, 'width': 600, 'height': 500})

        # 3. Main Container Frame (Centered)
        # We make this frame semi-transparent or solid white with opacity?
        # Solid white is safest for readability against moving background.
        self.container = tk.Frame(self.canvas, bg="white", padx=20, pady=20, relief=tk.RAISED, borderwidth=1)
        self.canvas.create_window(300, 250, window=self.container, width=500, height=400)

        # Move logic into container
        self.setup_ui_in_container()
        
        # Start animation
        self.animate_shapes()

    def setup_ui_in_container(self):
        # Header
        tk.Label(self.container, text="✨ My Tasks ✨", font=("Segoe UI", 20, "bold"), bg="white", fg=self.fg_color).pack(pady=(0, 15))

        # Task List
        self.list_frame = tk.Frame(self.container, bg="white")
        self.list_frame.pack(fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(
            self.list_frame,
            font=("Segoe UI", 12),
            bg="#FAFAFA",
            fg="#333",
            selectbackground=self.accent,
            selectforeground="white",
            highlightthickness=0,
            borderwidth=0,
            activestyle="none"
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.task_listbox.bind('<Double-1>', self.view_task_details)

        scrollbar = tk.Scrollbar(self.list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Buttons
        self.button_frame = tk.Frame(self.container, bg="white")
        self.button_frame.pack(pady=20)

        self.create_button("➕ Add", self.add_task).pack(side=tk.LEFT, padx=5)
        self.create_button("✅ Done", self.complete_task).pack(side=tk.LEFT, padx=5)
        self.create_button("🗑️ Del", self.delete_task).pack(side=tk.LEFT, padx=5)
        
        self.refresh_list()

    def create_button(self, text, command):
        btn = tk.Button(
            self.button_frame, 
            text=text, 
            command=command, 
            bg=self.btn_bg, 
            fg=self.fg_color, 
            activebackground=self.btn_hover, 
            activeforeground="white", 
            relief=tk.FLAT, 
            padx=12, 
            pady=5,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=self.btn_hover, fg="white"))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.btn_bg, fg=self.fg_color))
        return btn

    def animate_shapes(self):
        w, h = 600, 500
        for shape in self.shapes:
            self.canvas.move(shape['id'], shape['dx'], shape['dy'])
            pos = self.canvas.coords(shape['id'])
            # Bounce logic
            if pos[0] <= 0 or pos[2] >= w:
                shape['dx'] *= -1
            if pos[1] <= 0 or pos[3] >= h:
                shape['dy'] *= -1
        
        self.root.after(30, self.animate_shapes)

    def refresh_list(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.manager.list_tasks()
        for task in tasks:
            icon = "✓" if task.status == "completed" else "○"
            text = f" {icon}  {task.title}   #{task.id}"
            self.task_listbox.insert(tk.END, text)
            if task.status == "completed":
                self.task_listbox.itemconfig(tk.END, {'fg': '#AAA'})

    def add_task(self):
        title = simpledialog.askstring("Add Task", "Enter task title:")
        if title:
            desc = simpledialog.askstring("Add Task", "Enter description (optional):")
            self.manager.add_task(title, desc if desc else "")
            self.refresh_list()

    def complete_task(self):
        task_id = self.get_selected_task_id()
        if task_id:
            self.manager.update_task(task_id, status="completed")
            self.refresh_list()
        else:
            messagebox.showwarning("Warning", "Please select a task first.")

    def delete_task(self):
        task_id = self.get_selected_task_id()
        if task_id:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
                self.manager.delete_task(task_id)
                self.refresh_list()
        else:
            messagebox.showwarning("Warning", "Please select a task first.")

    def get_selected_task_id(self):
        try:
            selection = self.task_listbox.curselection()
            if not selection:
                return None
            idx = selection[0]
            task_str = self.task_listbox.get(idx)
            parts = task_str.split("#")
            if len(parts) > 1:
                return int(parts[-1])
            return None
        except Exception:
            return None

    def view_task_details(self, event=None):
        task_id = self.get_selected_task_id()
        if task_id:
            task = self.manager.get_task(task_id)
            if task:
                TaskDetailWindow(self.root, task)

class TaskDetailWindow:
    def __init__(self, parent, task):
        self.window = tk.Toplevel(parent)
        self.window.title("Task Details")
        self.window.geometry("400x400")
        self.window.resizable(False, False)
        
        # Colors: Pink and Blue mix
        self.bg_color = "#F8BBD0" # Pink
        self.fg_color = "#880E4F" # Dark Pink/Red
        self.window.configure(bg=self.bg_color)
        
        # Canvas for animation
        self.canvas = tk.Canvas(self.window, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Floating shapes (Blue bubbles)
        self.shapes = []
        for _ in range(8):
            x = random.randint(0, 400)
            y = random.randint(0, 400)
            size = random.randint(15, 50)
            color = random.choice(["#E3F2FD", "#BBDEFB", "#90CAF9"]) # Blue shades
            obj = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
            dy = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
            self.shapes.append({'id': obj, 'dx': dx, 'dy': dy, 'width': 400, 'height': 400})
            
        # Content Frame
        self.container = tk.Frame(self.canvas, bg="white", padx=20, pady=20, relief=tk.RAISED, borderwidth=1)
        self.canvas.create_window(200, 200, window=self.container, width=320, height=300)
        
        # Details
        status_icon = "✅" if task.status == "completed" else "⏳"
        
        tk.Label(self.container, text="📝 Task Details", font=("Segoe UI", 16, "bold"), bg="white", fg="#AD1457").pack(pady=(0, 10))
        
        tk.Label(self.container, text="Title:", font=("Segoe UI", 10, "bold"), bg="white", fg="gray").pack(anchor="w")
        tk.Label(self.container, text=task.title, font=("Segoe UI", 12), bg="white", fg="#333").pack(anchor="w", pady=(0, 10))
        
        tk.Label(self.container, text="Description:", font=("Segoe UI", 10, "bold"), bg="white", fg="gray").pack(anchor="w")
        tk.Label(self.container, text=task.description, font=("Segoe UI", 11), bg="white", fg="#555", wraplength=280, justify="left").pack(anchor="w", pady=(0, 10))
        
        tk.Label(self.container, text="Status:", font=("Segoe UI", 10, "bold"), bg="white", fg="gray").pack(anchor="w")
        tk.Label(self.container, text=f"{status_icon} {task.status.capitalize()}", font=("Segoe UI", 11), bg="white", fg="#333").pack(anchor="w", pady=(0, 10))
        
        tk.Label(self.container, text="Created:", font=("Segoe UI", 10, "bold"), bg="white", fg="gray").pack(anchor="w")
        tk.Label(self.container, text=task.created_at, font=("Segoe UI", 9), bg="white", fg="#777").pack(anchor="w")
        
        self.animate_shapes()
        
    def animate_shapes(self):
        w, h = 400, 400
        # Check if window still exists
        if not self.window.winfo_exists():
            return
            
        for shape in self.shapes:
            self.canvas.move(shape['id'], shape['dx'], shape['dy'])
            pos = self.canvas.coords(shape['id'])
            if pos[0] <= 0 or pos[2] >= w:
                shape['dx'] *= -1
            if pos[1] <= 0 or pos[3] >= h:
                shape['dy'] *= -1
        
        self.window.after(30, self.animate_shapes)

def run_gui():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
