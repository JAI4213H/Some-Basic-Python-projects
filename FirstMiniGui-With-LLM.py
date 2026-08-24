import tkinter as tk
from tkinter import ttk
from ollama import chat

#FOR TESTING AND LEARNING PURPOSE ONLY!!!!

def getresult():
    response = chat(
        model='gemma2:2b',
        messages=[{'role': 'user', 'content': f'{text_storage.get()}'}],
        options= {
            'num_predict': 50
        })
    entry_lable.config(text=f"Result {response.message.content}")
    
    


root = tk.Tk()
root.geometry('800x800')
root.title('Entry Widget Demo')


    

name_lable = tk.Label(root,text="Enter Your Prompt ")
name_lable.pack()
text_storage = tk.StringVar()

text_entry = tk.Entry(root,textvariable=text_storage)

text_entry.pack(pady=200)

final = tk.Button(root,text="Submit",command=getresult)

final.pack()

entry_lable = tk.Label(root,text=f"You entered: Nothing till now ")




entry_lable.pack()


root.mainloop()

#THINGS I MADE WRONG : 1. Used lable to display the output.  2. must have used Text or Scrollable Text
# 3. SHould have used Grid instead of putting things randomly
# 4. NO output optimizaion for the ollame gemma2:2b model.


