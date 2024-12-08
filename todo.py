# Import necessary libraries
import os
import tkinter as tk
from tkinter import messagebox


# Function to load tasks from a file
def load_tasks():
    """
    Loads tasks from a file named 'tasks.txt'. If the file doesn't exist, it creates one.
    Each line in the file represents a task in the format: task|priority|completed.
    Returns a list of tasks with their details.
    """
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as file:
            pass  # Create the file if it doesn't exist
    with open("tasks.txt", "r") as file:
        tasks = []
        for line in file.readlines():
            # Parse the task details from each line
            task_info = line.strip().split("|")
            if len(task_info) == 3:  # Ensure the data has the expected structure
                tasks.append({"task": task_info[0], "priority": task_info[1], "completed": task_info[2]})
        return tasks


# Function to save tasks to the file
def save_tasks(tasks):
    """
    Saves the current list of tasks into 'tasks.txt' in the format: task|priority|completed
    Each task is written on a new line in the file.
    """
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(f"{task['task']}|{task['priority']}|{task['completed']}\n")


# Main GUI Application Class
class TodoApp:
    def __init__(self, root):
        """
        Initializes the GUI window, sets up the widgets, and loads tasks from the file.
        """
        self.root = root
        self.root.title("To-Do App")
        self.root.geometry("600x700")
        
        # Load tasks from the file
        self.tasks = load_tasks()
        self.filtered_tasks = self.tasks  # Use this for filtered view logic

        # Title Label
        self.label_title = tk.Label(root, text="To-Do List with Priorities", font=("Arial", 20))
        self.label_title.pack(pady=10)

        # Listbox widget to display tasks
        self.listbox_tasks = tk.Listbox(
            root, height=15, width=50, selectmode=tk.SINGLE, font=("Arial", 12)
        )
        self.listbox_tasks.pack(pady=5)
        self.refresh_task_list()  # Populate the listbox with tasks

        # Input field for entering a new task
        self.label_task_entry = tk.Label(root, text="Enter Task Description:", font=("Arial", 12))
        self.label_task_entry.pack()
        self.entry_task = tk.Entry(root, font=("Arial", 12))
        self.entry_task.pack(pady=5)

        # Dropdown menu to select priority
        self.label_priority = tk.Label(root, text="Select Priority:", font=("Arial", 12))
        self.label_priority.pack()
        self.priority_var = tk.StringVar(value="Low")
        self.dropdown_priority = tk.OptionMenu(
            root, self.priority_var, "Low", "Medium", "High"
        )
        self.dropdown_priority.pack(pady=5)

        # Buttons for application functionalities
        self.button_add = tk.Button(
            root, text="Add Task", command=self.add_task, font=("Arial", 10)
        )
        self.button_add.pack(pady=5)

        self.button_mark_completed = tk.Button(
            root, text="Mark as Completed", command=self.mark_completed, font=("Arial", 10)
        )
        self.button_mark_completed.pack(pady=5)

        self.button_delete = tk.Button(
            root, text="Delete Task", command=self.delete_task, font=("Arial", 10)
        )
        self.button_delete.pack(pady=5)

        self.button_sort = tk.Button(
            root, text="Sort by Priority", command=self.sort_tasks, font=("Arial", 10)
        )
        self.button_sort.pack(pady=5)

        self.button_exit = tk.Button(
            root, text="Exit", command=self.exit_app, font=("Arial", 10)
        )
        self.button_exit.pack(pady=5)

    # Function to refresh the Listbox display
    def refresh_task_list(self):
        """
        Clears and repopulates the Listbox with the tasks sorted by priority for better visibility.
        """
        self.listbox_tasks.delete(0, tk.END)
        # Sort tasks by priority for better visibility
        self.filtered_tasks.sort(key=lambda x: {"Low": 3, "Medium": 2, "High": 1}[x["priority"]])
        for task in self.filtered_tasks:
            self.listbox_tasks.insert(tk.END, f"{task['task']} - Priority: {task['priority']}")

    # Function to add a new task to the task list
    def add_task(self):
        """
        Adds a new task with the selected priority to the task list and saves it.
        """
        task_desc = self.entry_task.get().strip()
        priority = self.priority_var.get()
        if task_desc:
            new_task = {"task": task_desc, "priority": priority, "completed": "No"}
            self.tasks.append(new_task)
            save_tasks(self.tasks)
            self.filtered_tasks = self.tasks
            self.refresh_task_list()
            self.entry_task.delete(0, tk.END)
            messagebox.showinfo("Success", f"Task '{task_desc}' added successfully with priority '{priority}'!")
        else:
            messagebox.showerror("Error", "Task description cannot be empty.")

    # Function to mark a task as completed
    def mark_completed(self):
        """
        Marks the selected task as completed and updates the task list.
        """
        try:
            selected_task_index = self.listbox_tasks.curselection()[0]
            task_to_mark = self.filtered_tasks[selected_task_index]
            task_to_mark["completed"] = "Yes"
            save_tasks(self.tasks)
            self.filtered_tasks = self.tasks
            self.refresh_task_list()
            messagebox.showinfo("Task Completed", f"Task '{task_to_mark['task']}' marked as completed.")
        except IndexError:
            messagebox.showerror("Error", "Please select a task to mark as completed.")

    # Function to delete a task
    def delete_task(self):
        """
        Deletes the selected task from the list and saves changes to the file.
        """
        try:
            selected_task_index = self.listbox_tasks.curselection()[0]
            task_to_delete = self.filtered_tasks[selected_task_index]
            self.tasks.remove(task_to_delete)
            save_tasks(self.tasks)
            self.filtered_tasks = self.tasks
            self.refresh_task_list()
            messagebox.showinfo("Deleted", f"Task '{task_to_delete['task']}' deleted.")
        except IndexError:
            messagebox.showerror("Error", "Please select a task to delete.")

    # Function to sort tasks by priority
    def sort_tasks(self):
        """
        Sorts tasks by priority and refreshes the Listbox display.
        """
        self.filtered_tasks.sort(key=lambda x: {"Low": 3, "Medium": 2, "High": 1}[x["priority"]])
        self.refresh_task_list()
        messagebox.showinfo("Sorted", "Tasks sorted by priority.")

    # Function to exit the application
    def exit_app(self):
        """
        Saves tasks to the file and closes the application window.
        """
        save_tasks(self.tasks)
        self.root.destroy()


# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
