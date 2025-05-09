import tkinter as tk
from tkinter import messagebox, filedialog
import os
import tkinter.font as tkfont
import re

class PersistentNotesApp:
    def __init__(self, root):
        self.root = root
        root.title("Persistent Notes")
        root.geometry("600x400")

        # Custom font
        custom_font = tkfont.Font(family="Monospace", size=12)

        # Text area with custom font and wheat background
        self.text_area = tk.Text(root, wrap=tk.WORD, font=custom_font, bg='wheat')
        self.text_area.pack(expand=True, fill='both')

        # Menu
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_notes, accelerator="Ctrl+S")
        file_menu.add_command(label="Clear", command=self.clear_notes)

        # Bind events
        self.text_area.bind('<Return>', self.add_task_line)
        root.bind('<Control-s>', lambda event: self.save_notes())

        # Load existing notes
        self.notes_path = os.path.expanduser('~/.persistent_notes.txt')
        self.load_notes()

        # Save on close
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_next_task_number(self):
        content = self.text_area.get("1.0", tk.END)
        task_numbers = re.findall(r'^(\d+)\.\s', content, re.MULTILINE)
        return int(task_numbers[-1]) + 1 if task_numbers else 1

    def add_task_line(self, event):
        # Get the current line
        current_line = int(self.text_area.index(tk.INSERT).split('.')[0])
        
        # Check if the line is not empty
        line_content = self.text_area.get(f"{current_line}.0", f"{current_line}.end")
        
        if line_content.strip():
            # Get the next task number
            next_task_number = self.get_next_task_number()
            
            # Insert new task line with number
            separator = f"\n{next_task_number}. "
            self.text_area.insert(tk.INSERT, separator)
        
        return 'break'  # Prevent default return behavior

    def load_notes(self):
        try:
            with open(self.notes_path, 'r') as file:
                content = file.read()
                # If file is empty, start with first task line
                if not content.strip():
                    content = "1. "
                self.text_area.insert(tk.END, content)
        except FileNotFoundError:
            self.text_area.insert(tk.END, "1. ")

    def save_notes(self):
        try:
            with open(self.notes_path, 'w') as file:
                file.write(self.text_area.get("1.0", tk.END))
            messagebox.showinfo("Saved", "Notes saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save notes: {str(e)}")

    def clear_notes(self):
        if messagebox.askyesno("Clear Notes", "Are you sure you want to clear all notes?"):
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, "1. ")
            if os.path.exists(self.notes_path):
                os.remove(self.notes_path)

    def on_closing(self):
        self.save_notes()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = PersistentNotesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()