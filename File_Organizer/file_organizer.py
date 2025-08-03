'''This script creat a gui with tkinter to organize files in a specified directory by their extensions.'''
'''The User has 3 options: '''
'''1. Inputfield = Directory '''
'''2. button = Organize'''
'''3. button = Exit '''

# Classes, functions, and imports


from tkinter import ttk
import tkinter as tk
import os
from tkinter import messagebox


class fileorganizer:
    def add_directory(self, directory):
        # Add a directory to the organizer
        if not os.path.exists(directory):
            return
        self.directory = directory

    def scan_directory(self, directory):
        # Scan the specified directory for files
        if not os.path.exists(directory):
            return []
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    def sort_files_by_extension(self, files):
        # Sort files by their extensions
        sorted_files = {
            'images': [],
            'documents': [],
            'audio': [],
            'video': [],
            'others': []
        }
        for file in files:
            ext = file.split('.')[-1].lower()
            if ext in ['jpg', 'jpeg', 'png', 'gif']:
                sorted_files['images'].append(file)
            elif ext in ['txt', 'docx', 'pdf']:
                sorted_files['documents'].append(file)
            elif ext in ['mp3', 'wav']:
                sorted_files['audio'].append(file)
            elif ext in ['mp4', 'avi']:
                sorted_files['video'].append(file)
            else:
                sorted_files['others'].append(file)
        return sorted_files

    def organize_files_on_click(self):
        # Organize files when the button is clicked
        directory = self.entry.get()
        if not directory:
            messagebox.showerror("Error", "Please enter a directory.")
            return
        if not os.path.exists(directory):
            messagebox.showerror(
                "Error", f"Directory '{directory}' does not exist.")
            return
        try:
            self.add_directory(directory)
            files = self.scan_directory(directory)
            if not files:
                messagebox.showinfo("Info", "No files found in the directory.")
                return
            sorted_files = self.sort_files_by_extension(files)

            directory_path = os.path.join(directory, "organized_files")
            os.makedirs(directory_path, exist_ok=True)
            for category, files in sorted_files.items():
                category_path = os.path.join(directory_path, category)
                os.makedirs(category_path, exist_ok=True)
                for file in files:
                    src = os.path.join(directory, file)
                    dst = os.path.join(category_path, file)
                    try:
                        os.rename(src, dst)
                    except Exception as e:
                        messagebox.showerror(
                            "Error", f"Could not move file '{file}': {e}")
            messagebox.showinfo("Success", "Files organized successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def quit_on_click(self):
        # Quit the application when the exit button is clicked
        self.root.quit()

    def gui_menu(self, organize_files_on_click=None, quit_on_click=None):
        # Create a GUI menu using tkinter with system-native appearance
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        window_width = 400
        window_height = 130
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Make window draggable
        def start_move(event):
            self._drag_start_x = event.x
            self._drag_start_y = event.y

        def do_move(event):
            x = self.root.winfo_x() + event.x - self._drag_start_x
            y = self.root.winfo_y() + event.y - self._drag_start_y
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.root.bind('<Button-1>', start_move)
        self.root.bind('<B1-Motion>', do_move)

        # Set ttk theme to system default
        style = ttk.Style(self.root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "xpnative" in style.theme_names():
            style.theme_use("xpnative")
        elif "clam" in style.theme_names():
            style.theme_use("clam")
        else:
            style.theme_use(style.theme_names()[0])

        # Create GUI elements
        self.label = ttk.Label(self.root, text="Enter Directory:")
        self.label.pack(anchor="w", padx=10, pady=(10, 0))

        self.entry = ttk.Entry(self.root)
        self.entry.pack(fill="x", padx=10, pady=(0, 10), ipady=4)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)

        self.organize_button = ttk.Button(
            button_frame, text="Organize", command=organize_files_on_click)
        self.organize_button.pack(
            side=tk.LEFT, padx=20, pady=5, ipadx=20, ipady=8)

        self.exit_button = ttk.Button(
            button_frame, text="Exit", command=quit_on_click)
        self.exit_button.pack(side=tk.LEFT, padx=20, pady=5, ipadx=20, ipady=8)

        self.root.mainloop()


# Main execution block to run the GUI

if __name__ == "__main__":
    organizer = fileorganizer()
    organizer.gui_menu(organize_files_on_click=organizer.organize_files_on_click,
                       quit_on_click=organizer.quit_on_click)
