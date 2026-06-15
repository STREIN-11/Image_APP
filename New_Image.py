import praw
import sys
import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from urllib.request import urlopen
from urllib.error import HTTPError

SCRIPT = "p1CoZQuBy9eP4e8YH0dM5Q"
SECRET = "6YHiBWbUWEIJMvYt91vuDjOOsCOUOA"
def download(storage_directory, subreddit_name, sort_type, num_images, log):
    try:
        os.makedirs(storage_directory, exist_ok=True)
        os.chdir(storage_directory)
        for f in os.listdir(storage_directory):
            os.remove(f)
        log("Cleared directory. Connecting to Reddit...\n")

        reddit = praw.Reddit(
            client_id=SCRIPT,
            client_secret=SECRET,
            user_agent="Image_Py",
        )
        subreddit = reddit.subreddit(subreddit_name)
        feed = {
            "hot": subreddit.hot,
            "new": subreddit.new,
            "top": subreddit.top,
            "rising": subreddit.rising,
        }[sort_type]

        images = [s.url for s in feed(limit=num_images)]
        log(f"Found {len(images)} posts. Downloading...\n")

        for i, image in enumerate(images):
            log(f"Downloading {i+1}/{len(images)}: {image}\n")
            try:
                imgdata = urlopen(image).read()
                ext = image.split('.')[-1][:4]
                fname = f"image{i+1}.{ext}"
                with open(fname, "wb") as f:
                    f.write(imgdata)
                if os.stat(fname).st_size < 200000:
                    os.remove(fname)
            except HTTPError:
                log(f"  HTTP Error for {image}\n")
            except (FileNotFoundError, OSError):
                log(f"  Invalid link: {image}\n")

        log("Done!\n")
    except Exception as e:
        log(f"Error: {e}\n")


def build_ui():
    root = tk.Tk()
    root.title("Reddit Image Downloader")
    root.resizable(False, False)

    # Set custom icon - change path to your .ico or .png file
    icon_path = r"C:\Users\subha\OneDrive\Desktop\Image\HAVI.ico"
    if os.path.exists(icon_path):
        if icon_path.endswith(".ico"):
            root.iconbitmap(icon_path)
        else:
            img = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, img)

    pad = {"padx": 10, "pady": 5}

    # Directory row
    tk.Label(root, text="Storage Directory:").grid(row=0, column=0, sticky="w", **pad)
    dir_var = tk.StringVar(value=r"C:\FUN ZONE\IMAGES\WallPaperr")
    tk.Entry(root, textvariable=dir_var, width=40).grid(row=0, column=1, **pad)
    tk.Button(root, text="Browse", command=lambda: dir_var.set(
        filedialog.askdirectory() or dir_var.get()
    )).grid(row=0, column=2, **pad)

    # Subreddit row
    tk.Label(root, text="Subreddit:").grid(row=1, column=0, sticky="w", **pad)
    sub_var = tk.StringVar(value="wallpaper")
    tk.Entry(root, textvariable=sub_var, width=40).grid(row=1, column=1, **pad)

    # Number of images row
    tk.Label(root, text="Number of Images:").grid(row=2, column=0, sticky="w", **pad)
    num_var = tk.IntVar(value=100)
    tk.Spinbox(root, from_=1, to=1000, textvariable=num_var, width=38).grid(row=2, column=1, **pad)

    # Sort type row
    tk.Label(root, text="Sort Type:").grid(row=3, column=0, sticky="w", **pad)
    sort_var = tk.StringVar(value="hot")
    ttk.Combobox(root, textvariable=sort_var, values=["hot", "new", "top", "rising"],
                 state="readonly", width=37).grid(row=3, column=1, **pad)

    # Log area
    log_box = scrolledtext.ScrolledText(root, width=60, height=15, state="disabled")
    log_box.grid(row=4, column=0, columnspan=3, **pad)

    def log(msg):
        log_box.config(state="normal")
        log_box.insert(tk.END, msg)
        log_box.see(tk.END)
        log_box.config(state="disabled")

    def start():
        btn.config(state="disabled")
        log_box.config(state="normal")
        log_box.delete("1.0", tk.END)
        log_box.config(state="disabled")
        threading.Thread(
            target=lambda: [
                download(dir_var.get(), sub_var.get(), sort_var.get(), num_var.get(), log),
                btn.config(state="normal"),
            ],
            daemon=True,
        ).start()

    btn = tk.Button(root, text="Start Download", command=start, bg="#4CAF50", fg="white", width=20)
    btn.grid(row=5, column=1, pady=10)

    root.mainloop()


if __name__ == "__main__":
    build_ui()