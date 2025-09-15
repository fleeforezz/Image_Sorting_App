# import os
# import shutil
# from tqdm import tqdm  # pip install tqdm

# # Ask user for input folder and destination folder
# source = input("Enter the folder to scan (leave blank for current folder): ").strip()
# if not source:
#     source = os.getcwd()

# destination = input("Enter destination folder for copied files: ").strip()
# if not destination:
#     destination = os.path.join(os.getcwd(), 'photo')

# # Normalize paths
# source = os.path.abspath(source)
# destination = os.path.abspath(destination)
# os.makedirs(destination, exist_ok=True)

# # Extensions to match
# extensions = ('.mp4', '.mov', '.heic', '.avi', '.jpg', '.jpeg', '.png')

# # Collect files & sizes
# files_to_copy = []
# total_size = 0
# for root, dirs, files in os.walk(source):
#     for file in files:
#         if file.lower().endswith(extensions):
#             fpath = os.path.join(root, file)
#             files_to_copy.append(fpath)
#             total_size += os.path.getsize(fpath)

# # Progress bar in bytes, will show MB copied
# pbar = tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024,
#             desc=f"Copying {len(files_to_copy)} files")

# bytes_copied = 0

# for src_path in files_to_copy:
#     file = os.path.basename(src_path)
#     dest_path = os.path.join(destination, file)

#     # Handle duplicate names
#     if os.path.exists(dest_path):
#         name, ext = os.path.splitext(file)
#         counter = 1
#         new_name = f"{name}_{counter}{ext}"
#         new_dest_path = os.path.join(destination, new_name)
#         while os.path.exists(new_dest_path):
#             counter += 1
#             new_name = f"{name}_{counter}{ext}"
#             new_dest_path = os.path.join(destination, new_name)
#         dest_path = new_dest_path

#     # Copy file in chunks so we can update size progress
#     with open(src_path, 'rb') as fsrc, open(dest_path, 'wb') as fdst:
#         while True:
#             chunk = fsrc.read(1024 * 1024)  # 1 MB chunks
#             if not chunk:
#                 break
#             fdst.write(chunk)
#             bytes_copied += len(chunk)
#             pbar.update(len(chunk))

# pbar.close()
# print(f"\nDone! {len(files_to_copy)} files copied to {destination}")


import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

extensions = ('.mp4', '.mov', '.heic', '.avi', '.jpg', '.jpeg', '.png')

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
        # same copy logic as before
        messagebox.showinfo("Info", "Start copying here... implement your copy logic")

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")  # or "darkly", "superhero"
    app = CopyApp(root)
    root.mainloop()

