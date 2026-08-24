import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk



data_location = None
df = None
numeric_list = None
if data_location == None:

    def temp_submissions():
        global data_location,df,numeric_list

        data_location = data_loc.get()
        
        try: 
            data = pd.read_csv(f"{data_location}")
            df = pd.DataFrame(data=data)
            numeric_list = list(df.select_dtypes(include=[float,int]).columns)
            temp_submission.destroy()

        except FileNotFoundError:
            print("Your input of filename isnt correct")
        
    

    temp_submission = tk.Toplevel(root)

    tk.Label(
        temp_submission,
        text="Enter name of the dataset or its location"
    ).pack(padx=10,pady=2)

    data_loc = tk.Entry(temp_submission)
    data_loc.pack(side=tk.LEFT,padx=10,pady=3)

    tk.Button(
        temp_submission,
        text="Submit",
        command=temp_submissions
    ).pack()



def submitstuff():

    

    

    print(
        "Both the features are:  ",
        storing_string_for_column1.get(),
        storing_string_for_column2.get()
    )

    makegraph(graph_frame)
    graph_frame.grid()


def makegraph(frame):

    

    x = df[storing_string_for_column1.get()]
    y = df[storing_string_for_column2.get()]
    
    for i in frame.winfo_children():
        i.destroy()

    figure = plt.Figure(figsize=(5, 4))
    ax = figure.add_subplot(111)

    type_graph = getattr(
        ax,
        storing_string_for_column3.get()
    )
    type_graph(x, y)

    ax.set_xlabel(storing_string_for_column1.get())
    ax.set_ylabel(storing_string_for_column2.get())
    canvas = FigureCanvasTkAgg(
        figure,
        master=frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )
root = tk.Tk()
root.geometry("800x500")

root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

## textVARIABLESSS----------
storing_string_for_column3 = tk.StringVar()
storing_string_for_column2 = tk.StringVar()
storing_string_for_column1 = tk.StringVar()
#---------------------------------


#texts
text1 = tk.Label(
    root,
    text="Enter the column names"
)

label1 = tk.Label(
    root,
    text="Column 1"
)

label2 = tk.Label(
    root,
    text="Column 2"
)

label3 = tk.Label(
    root,
    text="Type of Graph"
)
#-------------------------------------------
column1 = ttk.Combobox(
    root,
    textvariable=storing_string_for_column1
)

column2 = ttk.Combobox(
    root,
    textvariable=storing_string_for_column2
)

column3 = ttk.Combobox(
    root,
    textvariable=storing_string_for_column3
)


list_of_plots = ['scatter','bar','plot']


column1['state'] = 'readonly'
column1['values'] = numeric_list
column2['state'] = 'readonly'
column2['values'] = numeric_list
column3['state'] = 'readonly'
column3['values'] = list_of_plots

text1.grid(
    row=0,
    column=0,
    columnspan=2,
    padx=10,
    pady=5
)
label1.grid(
    row=1,
    column=0,
    padx=10,
    pady=3)
column1.grid(
    row=1,
    column=1,
    padx=10,
    pady=3)
label2.grid(
    row=2,
    column=0,
    padx=10,
    pady=3)

column2.grid(
    row=2,
    column=1,
    padx=10,
    pady=3)

label3.grid(
    row=3,
    column=0,
    padx=10,
    pady=3)

column3.grid(
    row=3,
    column=1,
    padx=10,
    pady=3)

submit_button = tk.Button(
    root,
    text="Submit",
    command=submitstuff)

submit_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=20)


graph_frame = tk.Frame(root)

graph_frame.grid(
    column=2,
    row=0,
    rowspan=4,
    sticky="nsew"
)

graph_frame.grid_remove()


root.mainloop()
