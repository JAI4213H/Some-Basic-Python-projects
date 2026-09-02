import tkinter as tk
from tkinter import ttk
import time
import numpy



dimension = None
def next_step():
    nxt = tk.Tk()
    
    total=[]
    for i in range(dimension):
        row=[]
        for j in range(dimension):
            
            element = ttk.Entry(nxt,width=3,font=("Arial", 14),justify="center")
            element.grid(row=i,column=j,ipadx=10,ipady=10,padx=2,pady=2)
            row.append(element)
        total.append(row)
        print(total)
            
            
    nxt.mainloop()
        
    
    
    
    
root = tk.Tk()
root.geometry("300x180")

def root_submit():
    global dimension
    try:
        dimension = int(entry.get())
        sucesslabel = ttk.Label(root,text="Proceding to Next step in 2 seconds",foreground="green")
        sucesslabel.pack(padx=5,pady=1)
        root.after(2000,next_step)
        
    except:
        warninglabel = ttk.Label(root,text="Enter an Integer please!!",foreground="red")
        warninglabel.pack(padx=5,pady=1)
        root.after(2000, warninglabel.destroy)
        
label1 = tk.Label(root,text="Dimension Of square matrix")
label1.pack(padx=5,pady=1)
entry = ttk.Entry(root)
entry.pack(padx=5,pady=2,ipadx=20)
button = ttk.Button(root,command=root_submit)
button.pack(padx=5,pady=2,ipadx=20)
root.mainloop()
