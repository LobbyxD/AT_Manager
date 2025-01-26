import tkinter as tk
from tkinter import messagebox, ttk, Tk
import os
import json
import datetime
#FEATURENEEDED Adding new line to bottom instead to top
#FEATURENEEDED Window border is white, I prefer making it black or changing according to dark mode.
#FEATURENEEDED Screen size adjustable instead of fixed.
#FEATURENEEDED cell text over wrap instead of cutting.
#FEATURENEEDED cell/row clipboard copy.
#FEATURENEEDED row clipboard copy, and pastable in Add Task / Edit Task with ease.
#FEATURENEEDED Save last viewed filter, it existed on "QA" then when re-open it will stay on "QA"
#FEATURENEEDED somehow make it a standalone program that doesn't require installations beside itself.

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        # Light/Dark mode flag
        self.dark_mode = False

        # Task data
        self.tasks = []

        # Filter tasks data
        self.filterTasks = []

        # Task ID counter
        self.task_id_counter = 1

        # Create UI components
        self.create_widgets()

        # Load tasks and mode preference after the UI is ready
        self.load_tasks()
        self.load_mode_preference()
        


    def create_widgets(self):
        print('create_widgets')
        # Header frame
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(fill="x")

        # Add Task button
        self.add_button = tk.Button(self.header_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side="left", padx=5)

        # Edit Task button
        self.edit_button = tk.Button(self.header_frame, text="Edit Task", command=self.edit_task, state="disabled")
        self.edit_button.pack(side="left", padx=5)

        # Delete Task button
        self.delete_button = tk.Button(self.header_frame, text="Delete Task", command=self.delete_task, state="disabled")
        self.delete_button.pack(side="left", padx=5)

        #BUG filter bar bg is white in dark mode
        # Filter status label and combobox
        self.status_label = tk.Label(self.header_frame, text="Filter Status:")
        self.status_label.pack(side="left", padx=5)

        self.status_filter = tk.StringVar(value="All")
        self.status_dropdown = tk.OptionMenu(self.header_frame, self.status_filter, "All", "Dev", "Self QA", "QA", "Released")
        self.status_dropdown.pack(side="left", padx=5)
        self.status_filter.trace_add("write", self.filter_tasks)

        #FEATURENEEDED Hover text after 0.3s saying "Toggle Theme"
        # Dark mode toggle button
        self.mode_button = tk.Button(self.header_frame, text="🌞", command=self.toggle_dark_mode, relief="flat")
        self.mode_button.pack(side="right")

        # Table frame
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill="both", expand=True)

        # Table headers
        #BUG Headers do not listen to theme.
        #BUG Dates accepet letter, invalid date and not formatted correctly 
        #BUG Characterization Link cells should appear with text "Link" (while url is hidden, visable only in editing.) and have a clicky mouse icon while hovering.
        self.headers = ["Jira Key", "Task Name", "Status", "Description", "Dev Date", "QA Date", "Released Date", "Aldon Task", "Characterization Link"]
        self.table = []

        # Display the table headers
        for col, header in enumerate(self.headers):
            label = tk.Label(self.table_frame, text=header, relief="solid", width=20)
            label.grid(row=0, column=col)

        # Task list display (grid of labels)
        self.update_task_display()

    def add_task(self):
        print('add_task')
        self.open_task_form()

    def edit_task(self):
        print('edit_task')
        selected_task = self.get_selected_task()
        if selected_task:
            self.open_task_form(selected_task)


    #BUG Do not allow to click outside of this window. only this window is focused.
    def open_task_form(self, task=None):
        print('open_task_form')
        # Create a new window for adding/editing a task
        if self.dark_mode:
            theme_bg_color = "#333"
            theme_fg_color = "white"
            theme_bg_color_lighten = "#474747"
            btn_bg = "#555"
            table_bg = "#555"
            table_fg = "white"
        else:
            theme_bg_color = "white"
            theme_fg_color = "black"
            btn_bg = "lightgray"
            table_bg = "white"
            table_fg = "black"

        form_window = tk.Toplevel(self.root)
        form_window.title("Task Form")
    
        # Apply theme to form window
        self.apply_theme_to_form(form_window)

        # Fields for the form
        task_details = task if task else {
            "Jira Key": "",
            "Task Name": "",
            "Status": "Dev",
            "Description": "",
            "Dev Date": str(datetime.date.today()),
            "QA Date": "",
            "Released Date": "",
            "Aldon Task": "",
            "Characterization Link": ""
        }

        task_jira_enty_label = tk.Label(form_window, text="Jira Key:")
        task_jira_enty_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        task_jira_enty_label.config(bg= theme_bg_color, fg= theme_fg_color)
        task_jira_entry = tk.Entry(form_window)
        task_jira_entry.insert(0, task_details["Jira Key"])
        task_jira_entry.grid(row=0, column=1, padx=10, pady=5)
        task_jira_entry.config(bg=theme_bg_color, fg=theme_fg_color)

        task_name_entry_label = tk.Label(form_window, text="Task Name:")
        task_name_entry_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        task_name_entry_label.config(bg= theme_bg_color, fg= theme_fg_color)
        task_name_entry = tk.Entry(form_window)
        task_name_entry.insert(0, task_details["Task Name"])
        task_name_entry.grid(row=1, column=1, padx=10, pady=5)
        task_name_entry.config(bg=theme_bg_color, fg=theme_fg_color)

        # Status dropdown
        Status_entry_label = tk.Label(form_window, text="Status:")
        Status_entry_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        Status_entry_label.config(bg= theme_bg_color, fg= theme_fg_color)
        #Dropdown

        status_var = tk.StringVar(value=task_details["Status"] if task_details["Status"] else "Dev")
        status_options = ["Dev", "Self QA", "QA", "Released"]
        status_combobox = ttk.Combobox(form_window, textvariable=status_var, values=status_options, state="readonly")
        status_combobox.grid(row=2, column=1, padx=10, pady=5)

        # Customize the combobox
        # status_combobox.config(
        #     background=theme_bg_color,
        #     foreground=theme_fg_color,
        #     font=("Helvetica", 10),  # Customize font if needed
        # )
        win = Tk()
        win.geometry("700x350")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground= theme_bg_color, background= theme_bg_color, foreground=theme_fg_color)
        win.option_add("*TCombobox*Listbox*Background", 'black')
        win.option_add('*TCombobox*Listbox*Foreground', 'white')

        label = ttk.Label(win, text="Status:", font=('Ariel 11'))
        label.pack(pady=30)
        cb= ttk.Combobox(win, width=25, values=status_options)
        cb.pack()
        win.mainloop()
        # Optional: Set a width for the combobox to match the layout
        status_combobox.config(width=15, style="")  # Adjust this value based on your needs

        description_entry_label = tk.Label(form_window, text="Description:")
        description_entry_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        description_entry_label.config(bg= theme_bg_color, fg= theme_fg_color)
        description_entry = tk.Entry(form_window)
        description_entry.insert(0, task_details["Description"])
        description_entry.grid(row=3, column=1, padx=10, pady=5)
        description_entry.config(bg=theme_bg_color, fg=theme_fg_color)

        dev_date_entry_label = tk.Label(form_window, text="Dev Date:")
        dev_date_entry_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        dev_date_entry_label.config(bg= theme_bg_color, fg= theme_fg_color)
        dev_date_entry = tk.Entry(form_window)
        dev_date_entry.insert(0, task_details["Dev Date"])
        dev_date_entry.grid(row=4, column=1, padx=10, pady=5)
        dev_date_entry.config(bg=theme_bg_color, fg=theme_fg_color)

        qa_date_entry_label = tk.Label(form_window, text="QA Date:")
        qa_date_entry_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)   
        qa_date_entry_label.config(bg= theme_bg_color, fg= theme_fg_color)
        qa_date_entry = tk.Entry(form_window)
        qa_date_entry.insert(0, task_details["QA Date"])
        qa_date_entry.grid(row=5, column=1, padx=10, pady=5)
        qa_date_entry.config(bg=theme_bg_color, fg=theme_fg_color)

        released_date_entry_label = tk.Label(form_window, text="Released Date:")
        released_date_entry_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)
        released_date_entry_label.config(bg= theme_bg_color, fg= theme_fg_color) 
        released_date_entry = tk.Entry(form_window)
        released_date_entry.insert(0, task_details["Released Date"])
        released_date_entry.grid(row=6, column=1, padx=10, pady=5)
        released_date_entry.config(bg=theme_bg_color, fg=theme_fg_color)

        aldon_task_entry_label = tk.Label(form_window, text="Aldon Task:")
        aldon_task_entry_label.grid(row=7, column=0, sticky="w", padx=10, pady=5)
        aldon_task_entry_label.config(bg= theme_bg_color, fg= theme_fg_color) 
        aldon_task_entry = tk.Entry(form_window)
        aldon_task_entry.insert(0, task_details["Aldon Task"])
        aldon_task_entry.grid(row=7, column=1, padx=10, pady=5)
        aldon_task_entry.config(bg=theme_bg_color, fg=theme_fg_color)

        char_link_entry_label = tk.Label(form_window, text="Characterization Link:")
        char_link_entry_label.grid(row=8, column=0, sticky="w", padx=10, pady=5)
        char_link_entry_label.config(bg= theme_bg_color, fg= theme_fg_color) 
        char_link_entry = tk.Entry(form_window)
        char_link_entry.insert(0, task_details["Characterization Link"])
        char_link_entry.grid(row=8, column=1, padx=10, pady=5)
        char_link_entry.config(bg=theme_bg_color, fg=theme_fg_color)

        def save_task():
            new_task = {
                "Jira Key": task_jira_entry.get(),
                "Task Name": task_name_entry.get(),
                "Status": status_var.get(),
                "Description": description_entry.get(),
                "Dev Date": dev_date_entry.get(),
                "QA Date": qa_date_entry.get(),
                "Released Date": released_date_entry.get(),
                "Aldon Task": aldon_task_entry.get(),
                "Characterization Link": char_link_entry.get(),
            }

            if task:  # Editing an existing task
                task.update(new_task)
            else:  # Adding a new task
                self.tasks.append(new_task)

            form_window.destroy()  # Close the form window
            self.update_task_display()
            self.save_tasks()  # Save after adding or editing a task

        # Save Button
        save_button = tk.Button(form_window, text="Save Task", command=save_task)
        save_button.grid(row=9, column=0, columnspan=2, pady=10)

    def apply_theme_to_form(self, window):
        if self.dark_mode:
            window.config(bg="#333")
            for widget in window.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg="#333", fg="white")
                elif isinstance(widget, tk.Entry) or isinstance(widget, tk.Button) or isinstance(widget, tk.OptionMenu):
                    widget.config(bg="#555", fg="white")
        else:
            window.config(bg="white")
            for widget in window.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg="white", fg="black")
                elif isinstance(widget, tk.Entry) or isinstance(widget, tk.Button) or isinstance(widget, tk.OptionMenu):
                    widget.config(bg="lightgray", fg="black")


    def delete_task(self):
        print('delete_task')
        selected_task = self.get_selected_task()
        if selected_task:
            if messagebox.askyesno("Delete Task", f"Are you sure you want to delete {selected_task['Jira Key']}?"):
                self.tasks.remove(selected_task)
                self.update_task_display()
                self.save_tasks()  # Save after deleting a task

    def update_task_display(self):
        print('update_task_display')
        # Clear existing task display
        for widget in self.table:
            widget.destroy()
        self.table.clear()

        # Display task rows
        for row_idx, task in enumerate(self.tasks, start=1):
            for col_idx, header in enumerate(self.headers):
                cell_value = task.get(header, "")
                label = tk.Label(self.table_frame, text=cell_value, relief="solid", width=20, height=2)
                label.grid(row=row_idx, column=col_idx)

                # Status coloring
                if header == "Status":
                    self.color_status(label, task['Status'])

                # Make Characterization Link clickable
                if header == "Characterization Link" and cell_value:
                    label.bind("<Button-1>", lambda event, link=cell_value: self.open_url(link))

                # Row selection
                label.bind("<Button-1>", lambda event, task=task: self.select_task(event, task))

                self.table.append(label)
        self.filterTasks = self.tasks
        

    def select_task(self, event, task):
        print('select_task')
        # Update task selection state
        self.selected_task = task
        self.edit_button.config(state="normal")
        self.delete_button.config(state="normal")

    #BUG selected task is not highlights visually
    def get_selected_task(self):
        print('get_selected_task')
        return getattr(self, "selected_task", None)

    def color_status(self, label, status):
        print('color_status')
        # Color map for status
        color_map = {
            "Dev": "red",
            "Self QA": "orange",
            "QA": "yellow",
            "Released": "green"
        }

        # Apply status color without overriding text color in dark mode
        label.config(fg=color_map.get(status, "black"))

    #BUG does not open / not clickable
    def open_url(self, url):
        print('open_url')
        os.system(f"start {url}")

    def toggle_dark_mode(self):
        print('toggle_dark_mode')
        self.dark_mode = not self.dark_mode
        
        
          # Save the mode preference when toggled

        # lst = []
        # for row_idx, task in enumerate(self.tasks, start=1):
        #     for col_idx, header in enumerate(self.headers):
        #         cell_value = task.get(header, "")
        #         label = tk.Label(self.table_frame, text=cell_value, relief="solid", width=20, height=2)
        #         label.grid(row=row_idx, column=col_idx)

        #         # Status coloring
        #         if header == "Status":
        #             lst.append((label, task['Status']))
        #             print(label, task['Status'])
        #             #self.color_status(label, task['Status'])

        self.apply_theme()
        self.save_mode_preference()
        # for row_idx, task in enumerate(self.tasks, start=1):
        #     for col_idx, header in enumerate(self.headers):
        #         cell_value = task.get(header, "")
        #         label = tk.Label(self.table_frame, text=cell_value, relief="solid", width=20, height=2)
        #         label.grid(row=row_idx, column=col_idx)

        #         # Status coloring
        #         if header == "Status":
        #             if self.dark_mode:
        #                 label.config(fg="red", background='white')
        #             else:
        #                 label.config(fg="red", background='black')
        # for l in lst:
        #   self.color_status(l[0], l[1])
  
    def apply_theme(self, filtered = False):
        print('apply_theme')
        if filtered:
            tasks = self.filterTasks
        else:
            tasks = self.tasks

        if self.dark_mode:
            theme_bg_color = "#333"
            theme_fg_color = "white"
            btn_bg = "#555"
            table_bg = "#555"
            table_fg = "white"
        else:
            theme_bg_color = "white"
            theme_fg_color = "black"
            btn_bg = "lightgray"
            table_bg = "white"
            table_fg = "black"

        self.root.config(bg=theme_bg_color)
        self.header_frame.config(bg=theme_bg_color)
        self.table_frame.config(bg=theme_bg_color)
        self.mode_button.config(bg=btn_bg, fg=theme_fg_color)
        self.add_button.config(bg=btn_bg, fg=theme_fg_color)
        self.edit_button.config(bg=btn_bg, fg=theme_fg_color)
        self.delete_button.config(bg=btn_bg, fg=theme_fg_color)
        self.status_label.config(bg=theme_bg_color, fg=theme_fg_color)
        #Status cell color
        counter = 0
        color_map = {
                    "Dev": "red",
                    "Self QA": "orange",
                    "QA": "yellow",
                    "Released": "green"
                    }
        
        for i in range(len(self.table)):
                if i % len(self.headers) == 2:
                    print(color_map[tasks[counter]["Status"]])
                    label = self.table[i]  
                # if counter < len(self.filterTasks):  # Prevent out-of-range access
                    label.config(bg=theme_bg_color, fg=color_map.get(tasks[counter]["Status"], table_fg))
                    counter += 1
                else:
                    label = self.table[i]  
                    label.config(bg=theme_bg_color, fg=table_fg) 

    def save_tasks(self):
        print('save_tasks')
        # Save tasks to a file
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)
        self.apply_theme()

    def load_tasks(self):
        print('load_tasks')
        # Load tasks from a file if it exists
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
                self.update_task_display()  # Ensure tasks are displayed on load

    def save_mode_preference(self):
        print('save_mode_preference')
        # Save the mode preference to a file
        with open("mode_preference.json", "w") as file:
            json.dump({"dark_mode": self.dark_mode}, file)

    def load_mode_preference(self):
        print('load_mode_preference')
        # Load the mode preference from a file
        if os.path.exists("mode_preference.json"):
            with open("mode_preference.json", "r") as file:
                data = json.load(file)
                self.dark_mode = data.get("dark_mode", False)
                self.apply_theme()  # Apply the mode when loaded

    def filter_tasks(self, *args):
        print('filter_tasks')
        selected_status = self.status_filter.get()

        # Filter tasks based on the selected status
        if selected_status == "All":
            filtered_tasks = self.tasks
        else:
            filtered_tasks = [task for task in self.tasks if task["Status"] == selected_status]

        # Update display with filtered tasks
        self.filterTasks = filtered_tasks
        self.update_task_display(filtered_tasks)
        self.apply_theme(filtered= True)
    
    def update_task_display(self, filtered_tasks=None):
        print('update_task_display')
        if filtered_tasks is None:
            filtered_tasks = self.tasks  # Default to all tasks if no filter is applied

        # Clear existing task display
        for widget in self.table:
            widget.destroy()
        self.table.clear()

        # Display task rows
        for row_idx, task in enumerate(filtered_tasks, start=1):
            for col_idx, header in enumerate(self.headers):
                cell_value = task.get(header, "")
                label = tk.Label(self.table_frame, text=cell_value, relief="solid", width=20, height=2)
                label.grid(row=row_idx, column=col_idx)

                # Make Characterization Link clickable
                if header == "Characterization Link" and cell_value:
                    label.bind("<Button-1>", lambda event, link=cell_value: self.open_url(link))

                # Row selection
                label.bind("<Button-1>", lambda event, task=task: self.select_task(event, task))

                self.table.append(label)



# Create the main window
root = tk.Tk()

app = TaskManagerApp(root)
root.mainloop()

