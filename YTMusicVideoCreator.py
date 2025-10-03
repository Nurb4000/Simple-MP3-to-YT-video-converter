import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def select_mp3():
    file_path = filedialog.askopenfilename(
        title="Select MP3 File",
        filetypes=[("MP3 files", "*.mp3")]
    )
    if file_path:
        mp3_entry.delete(0, tk.END)
        mp3_entry.insert(0, file_path)

def select_image():
    file_path = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=[("Image files", "*.jpg *.jpeg")]
    )
    if file_path:
        image_entry.delete(0, tk.END)
        image_entry.insert(0, file_path)

def run_conversion():
    mp3_file = mp3_entry.get()
    image_file = image_entry.get()
    
    if not mp3_file or not image_file:
        messagebox.showerror("Error", "Please select both MP3 and Image files")
        return
    
    if not os.path.exists(mp3_file):
        messagebox.showerror("Error", "MP3 file does not exist")
        return
    
    if not os.path.exists(image_file):
        messagebox.showerror("Error", "Image file does not exist")
        return
    
    # Get directory and base name
    mp3_dir = os.path.dirname(mp3_file)
    base_name = os.path.splitext(os.path.basename(mp3_file))[0]
    output_file = os.path.join(mp3_dir, f"{base_name}.mp4")
    
    # Build ffmpeg command
    cmd = [
        "ffmpeg",
        "-loop", "1",
        "-i", image_file,
        "-i", mp3_file,
        "-c:v", "libx264",
        "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
        "-shortest",
        output_file
    ]
    
    try:
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        messagebox.showinfo("Success", f"Video created successfully!\n\n{output_file}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Conversion failed:\n{e.stderr}")
    except FileNotFoundError:
        messagebox.showerror("Error", "FFmpeg not found. Please install FFmpeg and add it to your PATH.")

# Create main window
root = tk.Tk()
root.title("MP3 to MP4 Converter")
root.geometry("500x250")

# Create and pack widgets
tk.Label(root, text="MP3 File:").pack(pady=5)
mp3_frame = tk.Frame(root)
mp3_frame.pack(pady=5)
mp3_entry = tk.Entry(mp3_frame, width=50)
mp3_entry.pack(side=tk.LEFT, padx=5)
tk.Button(mp3_frame, text="Browse", command=select_mp3).pack(side=tk.LEFT)

tk.Label(root, text="Image File:").pack(pady=5)
image_frame = tk.Frame(root)
image_frame.pack(pady=5)
image_entry = tk.Entry(image_frame, width=50)
image_entry.pack(side=tk.LEFT, padx=5)
tk.Button(image_frame, text="Browse", command=select_image).pack(side=tk.LEFT)

tk.Button(root, text="Convert to MP4", command=run_conversion, bg="lightblue", height=2, width=20).pack(pady=20)

# Start the GUI event loop
root.mainloop()