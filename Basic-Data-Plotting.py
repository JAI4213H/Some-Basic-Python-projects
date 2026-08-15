
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

submittedcolumns = []

data = pd.read_csv("house_prediction_dataset.csv")
df = pd.DataFrame(data=data)

def submitstuff():

    submittedcolumns.clear()

    submittedcolumns.append(column1.get())
    submittedcolumns.append(column2.get())

    print("Both the features are:  ", submittedcolumns)
    makegraph(graph_frame)
    graph_frame.grid()


def makegraph(frame):

    if len(submittedcolumns) == 2:

        x = df[submittedcolumns[0]]
        y = df[submittedcolumns[1]]
        figure = plt.Figure(figsize=(5, 4))
        ax = figure.add_subplot(111)
        type_graph = getattr(ax , column3.get())
        
        type_graph(x, y)

        ax.set_xlabel(submittedcolumns[0])
        ax.set_ylabel(submittedcolumns[1])
        canvas = FigureCanvasTkAgg(figure, master=frame)

        canvas.draw()

        canvas.get_tk_widget().pack(fill="both",expand=True)


root = tk.Tk()
root.geometry("800x500")
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

text1 = tk.Label(root, text="Enter the column names")
label1 = tk.Label(root, text="Column 1")
column1 = tk.Entry(root)
label2 = tk.Label(root, text="Column 2")
column2 = tk.Entry(root)
label3 = tk.Label(root, text="Type of Graph")
column3 = tk.Entry(root)
text1.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

label1.grid(row=1, column=0, padx=10, pady=3)
column1.grid(row=1, column=1, padx=10, pady=3)
label2.grid(row=2, column=0, padx=10, pady=3)
column2.grid(row=2, column=1, padx=10, pady=3)

label3.grid(row=3, column=0, padx=10, pady=3)
column3.grid(row=3, column=1, padx=10, pady=3)

submit_button = tk.Button(
    root,
    text="Submit",
    command=submitstuff
)

submit_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=20
)

graph_frame = tk.Frame(root)

graph_frame.grid( column=2,row=0,rowspan=4,sticky="nsew"
)
graph_frame.grid_remove()








root.mainloop()
