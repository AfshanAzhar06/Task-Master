import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from anotherWindow import AnotherWindow


window = tk.Tk()
window.title("Task Master")
window.geometry("400x680+400+10")
window.resizable(False, False)

# Create Functions
def open_another_window():
    anotherWindow = AnotherWindow(window,tree)

def delete_task():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)
    else:
        messagebox.showinfo("Error", "Please select a task.")

def mark_completed():
    selected_item = tree.selection()
    if selected_item:
        tree.set(selected_item, column='#1', value='Completed')
    else:
        messagebox.showinfo("Error", "Please select a task.")

def mark_not_completed():
    selected_item = tree.selection()
    if selected_item:
        tree.set(selected_item, column='#1', value='Not Completed')
    else:
        messagebox.showinfo("Error", "Please select a task.")

def save_tasks():
    tasks = []
    subtasks = {}

    # Traverse the tree to collect tasks and subtasks
    for item in tree.get_children():
        task = tree.item(item)["text"]
        tasks.append(task)

        children = tree.get_children(item)
        if children:
            subtasks[task] = [tree.item(child)["text"] for child in children]

    # Save tasks and subtasks to the file
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(task + "\n")
            if task in subtasks:
                for subtask in subtasks[task]:
                    file.write(f"- {subtask}\n")

def load_tasks():
    try:
        with open("tasks.txt", "r") as file:
            current_task = None
            for line in file:
                line = line.strip()
                if line.startswith("-"):
                    if current_task:
                        tree.insert(parent_task, 'end', text=line[2:], values=('Not Completed',))
                else:
                    current_task = line
                    parent_task = tree.insert('', 'end', text=line, values=('Not Completed',))
    except FileNotFoundError:
        pass

def on_closing():
    if messagebox.askyesno("Confirmation", "Do you want to save tasks before closing?"):
        save_tasks()
    window.destroy()



# icon
Image_icon = PhotoImage(file="task.png")
window.iconphoto(False, Image_icon)

# top bar
TopImage = PhotoImage(file="topbar.png")
Label(window, image=TopImage).pack()

dockImage = PhotoImage(file="dock.png")
Label(window, image=dockImage, bg="#32405b").place(x=30, y=25)

noteImage = PhotoImage(file="task.png")
Label(window, image=noteImage, bg="#32405b").place(x=340, y=25)

heading = Label(window, text="TASK MASTER", font="arial 20 bold", fg="white", bg="#32405b")
heading.place(x=100, y=20)



# create frame
frame = tk.Frame(window,bd=3,width=650,bg="#32405b")   
frame.pack(pady=(140,0))

# Create a scrollable frame
scrollable_frame = ttk.Frame(frame)
scrollable_frame.pack(fill='both', expand=True)

# Create a tree view
tree = ttk.Treeview(scrollable_frame,height=15)
tree.pack(side='left', fill='y')

# Add a scrollbar to the frame
scrollbar = ttk.Scrollbar(scrollable_frame, orient='vertical', command=tree.yview)
scrollbar.pack(side='right', fill='y')

# Configure the treeview to use the scrollbar
tree.configure(yscrollcommand=scrollbar.set)

# Add columns to the tree view
tree['columns'] = ('Status')
tree.column('#0', width=250)
tree.column('Status', width=131)
tree.heading('#0', text='Task')
tree.heading('Status', text='Status')

# Create buttons
add_button = Button(window, text="ADD", font="arial 20 bold", width=24, bg="#5a95ff", fg="#fff", bd=0, command=open_another_window)
add_button.place(x=0, y=150)

# delete button
Delete_icon = PhotoImage(file="delete.png")
delete_button = tk.Button(window, image=Delete_icon, bd=0, command=delete_task)
delete_button.pack(side=BOTTOM, pady=13)

# mark buttons

button_mark_completed = tk.Button(window, text='Mark Completed', font="arial 9 bold", command=mark_completed, bg='#318CE7', fg='white', bd=5, highlightbackground='#888888')
button_mark_completed.pack(side=tk.BOTTOM)
button_mark_completed.place(x=35, y=556)

button_mark_not_completed = tk.Button(window, text='Mark Not Completed', font="arial 9 bold", command=mark_not_completed, bg='#318CE7', fg='white',bd=5, highlightbackground='#888888')
button_mark_not_completed.pack(side=tk.BOTTOM)
button_mark_not_completed.place(x=250, y=556)

BUTTON = tk.Button(window, text=' BUTTON', font="arial 9 bold",  bg='#318CE7', fg='white', bd=5, highlightbackground='#888888')
BUTTON.pack(side=tk.BOTTOM)
BUTTON.place(x=150, y=556)

window.protocol("WM_DELETE_WINDOW", on_closing)
load_tasks()  # Load tasks from file
window.mainloop()
