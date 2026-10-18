from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

path = None

def analyze():
    root.withdraw()
    analyticwindow = tk.Toplevel(root)
    analyticwindow.title("Analytic Window")
    analyticwindow.geometry("1920x1080")
    analyticwindow.grid_rowconfigure(0,weight=1)
    analyticwindow.grid_columnconfigure(0,weight=1)
    analyticwindow.grid_columnconfigure(1,weight=3)
    if path is not None:
        image = Image.open(f"{path}").convert("L")
        a = np.array(image)
        U, S, VT = np.linalg.svd(a,full_matrices=False)
        first_8 = []
        for i in range(10,50,5):
            summ = np.zeros_like(a,dtype=float)
            for j in range(i):
                summ += S[j]*np.outer(U[:,j],VT[j,:])
            first_8.append(summ)
    
    left_frame = tk.Frame(analyticwindow,bg = "#836161")
    left_frame.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
    tk.Label(
        left_frame,text="Original Image",fg="white",bg="#202020"
    ).pack(padx=10)
    siz = Figure(figsize=(5,4),dpi=1000)
    ax = siz.add_subplot(111)
    
    
        
        
    
   



def select_file():
    global path
    try:
        path = filedialog.askopenfilename(filetypes=[("JPEG IMAGES","*.jpg")])
        lab1.config(text="File Found Sucessfully",foreground="green")
        lab2.config(text=f"File:  {path}")
        print(path)
        time.sleep(0.1)
        analyze()
        
        
    except:
        print("An error occured. Try again")

root = tk.Tk()
root.geometry("600x300")
root.title("Image Compression using SVD")
bun1 = tk.Button(root,text="Select File",padx=10,pady=6,command=select_file)
bun1.grid(row=1,column=0)
lab1 = tk.Label(root,text="No file Selected",foreground="red")
lab1.grid(row=2,column=0)
lab2 = tk.Label(root,text=f".",foreground="grey")
lab2.grid(row= 1,column=0)

root.mainloop()
