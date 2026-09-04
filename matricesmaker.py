import tkinter as tk
from tkinter import ttk
import time
import numpy as np

total = [] 
values = [] ## All the values of the matrix will be stored in this 2D array
def matrix_info():
    global values
    arr = np.array(values)
    det = np.linalg.det(arr)
    rank = np.linalg.matrix_rank(arr)
    mean = np.mean(arr)
    eigen_values,eigen_vectors = np.linalg.eig(arr)
    info_values = {
        "det": det,
        "rank": rank,
        "mean": mean,
        "eigen_values": eigen_values,
        "eigen_vectors": eigen_vectors
    }
    info = tk.Tk()
    info.geometry("400x300")
    for i in info_values:
        a = ttk.Label(info,text=f"{i} : {info_values[i]}")
        a.pack(padx=10,pady=3)
    info.mainloop()
   



def getvalues(nxt): # TO get the values of elements which we entered in element BOX
    global values #To store the values in it
    try:
        values = []
        
        for i in total:
            row_value = []  ##To get row values which later will be stored in values
            for j in i:
                row_value.append(int(j.get()))
            values.append(row_value)
        
        print(np.array(values))
    except:
        a = ttk.Label(nxt,foreground="red",text="Something Went wrong")
        a.pack()
                

dimension = None #To store the dimention of the Matrtix

def next_step():  #Function to make a group of entries which will mimic matrix elements
    global total
    nxt = tk.Tk()
    
    matrix_frame = ttk.Frame(nxt)
    matrix_frame.pack()
    
    total=[]
    for i in range(dimension):
        row=[]
        for j in range(dimension):
            
            element = tk.Entry(matrix_frame,width=3,font=("Arial", 14),justify="center",bg="black",fg='white')
            element.grid(row=i,column=j,ipadx=10,ipady=10,padx=2,pady=2)
            row.append(element)
        total.append(row)
    def submit_functions(nxt):
        getvalues(nxt)
        matrix_info()
        
        
    sumbit_button = ttk.Button(nxt,text="Submit to perform Operations",command=lambda: submit_functions(nxt=nxt))
    sumbit_button.pack(ipadx=20,ipady=5)
            
            
    nxt.mainloop()
        
    
    
###FIRST INTERFACE -- JUST A BASIC INTERFACE NO FURTHER DEVELOPMENT NEEDED HERE!!!!!!!!!!!!!!!!!!!!!!###############   
root = tk.Tk()  #First Interface
root.geometry("300x180")

def root_submit():
    global dimension
    try:
        dimension = int(entry.get())
        sucesslabel = ttk.Label(root,text="Proceding to Next step in 20 miniseconds",foreground="green")
        sucesslabel.pack(padx=5,pady=1)
        root.after(200,next_step)
        
        
    except:
        warninglabel = ttk.Label(root,text="Enter an Integer please!!",foreground="red")
        warninglabel.pack(padx=5,pady=1)
        root.after(2000, warninglabel.destroy)
        
label1 = tk.Label(root,text="Dimension Of square matrix")
label1.pack(padx=5,pady=1)
entry = ttk.Entry(root)
entry.pack(padx=5,pady=2,ipadx=20)
button = ttk.Button(root,command=root_submit,text="SUBMIT")
button.pack(padx=5,pady=2,ipadx=20)
root.mainloop()
