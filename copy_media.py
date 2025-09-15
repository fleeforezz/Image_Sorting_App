import sys, os
import shutil
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

extensions = ('.mp4', '.mov', '.heic', '.avi', '.jpg', '.jpeg', '.png')

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class CopyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Copier")
        self.source_dir = ttk.StringVar()
        self.dest_dir = ttk.StringVar()
        self.progress_var = ttk.DoubleVar()
        self.status_text = ttk.StringVar(value="Select source and destination folders.")

        frame = ttk.Frame(root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Source folder:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.source_dir, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Browse", bootstyle=INFO, command=self.browse_source).grid(row=0, column=2)

        ttk.Label(frame, text="Destination folder:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.dest_dir, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(frame, text="Browse", bootstyle=INFO, command=self.browse_dest).grid(row=1, column=2)

        self.progress = ttk.Progressbar(frame, orient="horizontal",
                                        length=400, mode="determinate",
                                        variable=self.progress_var, bootstyle=SUCCESS)
        self.progress.grid(row=2, column=0, columnspan=3, pady=10)

        ttk.Label(frame, textvariable=self.status_text, wraplength=400).grid(row=3, column=0, columnspan=3, sticky="w")

        ttk.Button(frame, text="Start Copy", bootstyle=SUCCESS, command=self.start_copy).grid(row=4, column=0, columnspan=3, pady=5)

    def browse_source(self):
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            self.source_dir.set(folder)

    def browse_dest(self):
        folder = filedialog.askdirectory(title="Select Destination Folder")
        if folder:
            self.dest_dir.set(folder)

    def start_copy(self):
        src = self.source_dir.get().strip()
        dst = self.dest_dir.get().strip()

        if not os.path.isdir(src):
            messagebox.showerror("Error", "Source folder is invalid.")
            return

        if not dst:
            messagebox.showerror("Error", "Please select a destination folder.")
            return

        if not os.path.exists(dst):
            os.makedirs(dst, exist_ok=True)

        # find all files to copy
        files_to_copy = []
        for root, dirs, files in os.walk(src):
            for file in files:
                if file.lower().endswith(extensions):
                    files_to_copy.append(os.path.join(root, file))

        if not files_to_copy:
            messagebox.showinfo("Info", "No media files found to copy.")
            return

        self.progress_var.set(0)
        self.progress.configure(maximum=len(files_to_copy))
        self.status_text.set(f"Found {len(files_to_copy)} files. Copying...")

        # copy loop
        for idx, src_path in enumerate(files_to_copy, 1):
            file_name = os.path.basename(src_path)
            dest_path = os.path.join(dst, file_name)

            # avoid overwriting
            if os.path.exists(dest_path):
                name, ext = os.path.splitext(file_name)
                counter = 1
                new_name = f"{name}_{counter}{ext}"
                new_dest_path = os.path.join(dst, new_name)
                while os.path.exists(new_dest_path):
                    counter += 1
                    new_name = f"{name}_{counter}{ext}"
                    new_dest_path = os.path.join(dst, new_name)
                dest_path = new_dest_path

            shutil.copy2(src_path, dest_path)

            # update progress bar & status
            self.progress_var.set(idx)
            self.status_text.set(f"Copying {idx}/{len(files_to_copy)}: {file_name}")
            self.root.update_idletasks()

        self.status_text.set(f"Done! Copied {len(files_to_copy)} files to {dst}")
        messagebox.showinfo("Done", f"Copied {len(files_to_copy)} files to:\n{dst}")

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")  # "darkly", "superhero" also nice
    icon_path = resource_path(os.path.join("assets", "photo.ico"))
    root.iconbitmap(icon_path)
    app = CopyApp(root)
    root.mainloop()
