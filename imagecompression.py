
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

path = None


def analyze():
    image = Image.open(path).convert("L")
    a = np.array(image)

    U, S, VT = np.linalg.svd(a, full_matrices=False)

    first_8 = []

    for k in range(10, 50, 5):
        summ = np.zeros_like(a, dtype=float)

        for j in range(k):
            summ += S[j] * np.outer(U[:, j], VT[j, :])

        additions = k * a.shape[0] * a.shape[1]

        first_8.append((k, summ, additions))

    analyticwindow = tk.Toplevel(root)
    analyticwindow.title("Image Compression using SVD")
    analyticwindow.geometry("1400x850")

    analyticwindow.grid_columnconfigure(0, weight=1)
    analyticwindow.grid_columnconfigure(1, weight=3)
    analyticwindow.grid_rowconfigure(0, weight=1)

    # Original image: left frame
    left_frame = tk.Frame(analyticwindow, bg="#836161")
    left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(
        left_frame, text="Original Image",
        fg="white", bg="#202020"
    ).pack(fill="x")

    fig = Figure(figsize=(5, 5))
    ax = fig.add_subplot(111)
    ax.imshow(a, cmap="gray")
    ax.axis("off")

    canvas = FigureCanvasTkAgg(fig, master=left_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Compressed images: right frame
    right_frame = tk.Frame(analyticwindow, bg="#dea6a6")
    right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    tk.Label(
        right_frame, text="Compressed Images",
        bg="#dea6a6", font=("Arial", 14, "bold")
    ).grid(row=0, column=0, columnspan=4, pady=5)

    for col in range(4):
        right_frame.grid_columnconfigure(col, weight=1)

    for idx, (k, arr, additions) in enumerate(first_8):
        row = (idx // 4) * 2 + 1
        col = idx % 4

        fig = Figure(figsize=(2.5, 2), dpi=80)
        ax = fig.add_subplot(111)
        ax.imshow(arr, cmap="gray", vmin=0, vmax=255)
        ax.axis("off")
        fig.tight_layout(pad=0)

        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(
            row=row, column=col, padx=5, pady=2, sticky="nsew"
        )

        tk.Label(
            right_frame,
            text=f"k = {k}\nAdditions: {additions:,}",
            bg="#dea6a6",
            font=("Arial", 9)
        ).grid(row=row + 1, column=col, pady=(0, 8))


def select_file():
    global path

    path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )

    if path:
        lab1.config(text="File selected successfully", fg="green")
        lab2.config(text=f"File: {path}")
        analyze()


root = tk.Tk()
root.geometry("650x200")
root.title("Image Compression using SVD")

tk.Button(
    root, text="Select File", padx=10, pady=6,
    command=select_file
).grid(row=0, column=0)

lab1 = tk.Label(root, text="No file selected", fg="red")
lab1.grid(row=1, column=0)

lab2 = tk.Label(root, text="", fg="grey", wraplength=600)
lab2.grid(row=2, column=0)

root.mainloop()
