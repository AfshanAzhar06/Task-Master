import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *

class AnotherWindow(tk.Toplevel):
    def __init__(self, master, tree):
        super().__init__(master)
        self.title("Enter Task...")
        self.tree = tree

        # Set background color
        self.configure(bg='white')

        # Create entry fields
        placeholder_text = "Enter your to-do here..."
        self.entry_task = tk.Entry(self, width=40, bd=2, relief=tk.SOLID, fg="gray")
        self.entry_task.place(x=50, y=70, width=300, height=40)
        self.entry_task.insert(0, placeholder_text)
        self.entry_task.bind("<FocusIn>", self.clear_placeholder)
        self.entry_task.bind("<FocusOut>", self.restore_placeholder)

        self.priority_var = tk.BooleanVar()
        self.priority_checkbox = tk.Checkbutton(self, text="Priority", variable=self.priority_var)
        self.priority_checkbox.place(x=160, y=140)

        # Create buttons
        self.button_add_task = tk.Button(self, text='Add Task', font="arial 9 bold", command=self.add_task, bg='#318CE7', fg='white', bd=5, highlightbackground='#888888')
        self.button_add_task.place(x=80, y=220)

        button_add_subtask = tk.Button(self, text='Add Subtask', font="arial 9 bold", command=self.add_subtask, bg='#318CE7', fg='white', bd=5, highlightbackground='#888888')
        button_add_subtask.place(x=240, y=220)

        # Set default window size
        self.geometry('400x400')
        self.resizable(False, False)

    def clear_placeholder(self, event):
        current_text = self.entry_task.get()
        placeholder_text = "Enter your to-do here..."
        if current_text == placeholder_text:
            self.entry_task.delete(0, "end")
            self.entry_task.config(fg="black") # Change the text color to black

    def restore_placeholder(self, event):
        current_text = self.entry_task.get()
        placeholder_text = "Enter your to-do here..."
        if current_text == "":
            self.entry_task.insert(0, placeholder_text)
            self.entry_task.config(fg="gray")  # Change the text color back to gray

    def add_task(self):
        task_name = self.entry_task.get()
        priority = self.priority_var.get()
        if not task_name or task_name == "Enter your to-do here...":
            messagebox.showwarning("Empty Task", "Please enter a task") 
        else:
            if priority:
                task_name = "* " + task_name  # Add '*' prefix for high-priority tasks
                self.tree.insert('', 0, text=task_name, values=('Not Completed',))
            else:
                self.tree.insert('', 'end', text=task_name, values=('Not Completed',))

            self.entry_task.delete(0, 'end')
        self.destroy()

    def add_subtask(self):
        selected_item = self.tree.selection()
        if selected_item:
            subtask_name = self.entry_task.get()
            if not subtask_name or subtask_name == "Enter your to-do here...":
                messagebox.showwarning("Empty Task", "Please enter a task") 
            else:
                self.tree.insert(selected_item, 'end', text=subtask_name, values=('Not Completed',))
            self.entry_task.delete(0, 'end')
        else:
            messagebox.showinfo("Error", "Please select a task.")
        self.destroy()
