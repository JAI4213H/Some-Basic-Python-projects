import mysql.connector as sql
import tkinter as tk
from tkinter import ttk


connect = sql.connect(host = "localhost",username="root",password='',database="world") #Used Xampp for SQL server
cursor = connect.cursor()
#QURIES Required ----------------------------
query = "INSERT INTO userdata (username,password) VALUES (%s,%s)"
check_query = "SELECT username FROM userdata WHERE username = %s"
login_query = "SELECT username FROM userdata WHERE username = %s AND password = %s"
#----------------------------------
option_window = tk.Tk()
option_window.geometry("400x180")
option_window.columnconfigure(1,weight=1)


#WINDOW FOR CREARING ACCOUNT
def CreateAcountWindow():
    
    def sumbit():
        username = username_entry.get()
        password = pass_entry.get()
        values = [username,password]
        cursor.execute(check_query,(username,))
        check_result  = cursor.fetchone() #Fetch One DataLine if found then it wont return NONE
        
        
        if check_result is not None:
            confirmLable.config(text="USERNAME ALREADY EXIST!!!!!!!",foreground="red")
            return
        try:          
            cursor.execute(query,values)
            connect.commit()
            confirmLable.config(text="Your Account has been sucessfully created!",foreground="green")
        except Exception as e:
            print("Somehting Went Wrong!!!",e)

        
    option_window.withdraw() # To Not destroy the window (we cant use .destroy)
    create_window = tk.Toplevel(option_window)
    create_window.columnconfigure(0,weight=1)
    create_window.columnconfigure(1,weight=2)
    create_window.geometry("400x200")
    
    lable1 = ttk.Label(create_window,text="Username:")
    lable2 = ttk.Label(create_window,text="Password")
    username_entry = ttk.Entry(create_window)
    pass_entry = ttk.Entry(create_window)
    sumbit_butn = ttk.Button(create_window,text="Submit",command=sumbit)
    confirmLable = ttk.Label(create_window,text="")
    
    username_entry.focus()
    
    confirmLable.grid(row=4,column=1)
    lable1.grid(row=1,column=0,ipadx=20,ipady=5)
    lable2.grid(row=2,column=0,ipadx=20,ipady=5)
    username_entry.grid(row=1,column=1)
    pass_entry.grid(row=2,column=1)
    sumbit_butn.grid(row=3,column=1)


#LOGIN WINDOW
def LoginWindow():
    
    def login():
        username = username_entry.get()
        password = pass_entry.get()
        values = (username,password)
        
        try:
            cursor.execute(login_query,values)
            login_result = cursor.fetchone()
            
            if login_result is not None:
                confirmLable.config(text="Login Successful!",foreground="green")
            else:
                confirmLable.config(text="INVALID USERNAME OR PASSWORD!!!!!!!",foreground="red")
        except Exception as e:
            print("Something Went Wrong!!!",e)
    
    
    option_window.withdraw()
    login_window = tk.Toplevel(option_window)
    login_window.columnconfigure(0,weight=1)
    login_window.columnconfigure(1,weight=2)
    login_window.geometry("400x200")
    
    lable1 = ttk.Label(login_window,text="Username:")
    lable2 = ttk.Label(login_window,text="Password")
    username_entry = ttk.Entry(login_window)
    pass_entry = ttk.Entry(login_window,show="*")
    login_butn = ttk.Button(login_window,text="Login",command=login)
    confirmLable = ttk.Label(login_window,text="")
    
    username_entry.focus()
    
    confirmLable.grid(row=4,column=1)
    lable1.grid(row=1,column=0,ipadx=20,ipady=5)
    lable2.grid(row=2,column=0,ipadx=20,ipady=5)
    username_entry.grid(row=1,column=1)
    pass_entry.grid(row=2,column=1)
    login_butn.grid(row=3,column=1)


create_button = ttk.Button(option_window,text="Create Account",command=CreateAcountWindow)
login_button = ttk.Button(option_window,text="Login",command=LoginWindow)
create_button.grid(row=1,column=1,ipadx=30,ipady=15,padx=30,pady=4)
login_button.grid(row=2,column=1,ipadx=30,ipady=15,padx=10,pady=4)


option_window.mainloop()
