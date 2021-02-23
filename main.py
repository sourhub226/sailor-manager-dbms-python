# MySQL Sailor Manager database implementation in python
# To create a simple database application for the following schema
# SAILOR(SID,SNAME,RATING,AGE)

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql  #module to connect python with mysql server

#Tkinter GUI initialization codes
root=Tk()
root.minsize(800,295)
root.title("Sailor Manager")
root.update()

#Global variables
sid_var=StringVar()
sname_var=StringVar()
rating_var=StringVar()
age_var=StringVar()

# Theme variables
bgcolor="#f6f6f6"

#Establish connection to mysql database named sailor_manager pre-defined using the following queries
# create database sailor_manager;
# use sailor_manager;
# create table sailor(sid int primary key,sname varchar(30) not null, rating int not null,age int not null);
def get_cursor():
    con=pymysql.connect(host="localhost",user="root",password="",database="sailor_manager")
    return con,con.cursor()

def get_input_data(self):
    current_row=database_table.focus()
    contents=database_table.item(current_row)
    row_data=contents['values']
    sid_var.set(row_data[0])
    sname_var.set(row_data[1])
    rating_var.set(row_data[2])
    age_var.set(row_data[3])

def clear_input():
    sid_var.set("")
    sname_var.set("")
    rating_var.set("")
    age_var.set("")

#Displays all data present in the database
def display_database():
    con,cur=get_cursor()
    query="select * from sailor;" #display query
    cur.execute(query)
    rows=cur.fetchall()
    print("Data fetched")
    database_table.delete(*database_table.get_children())
    for row in rows:
        database_table.insert("",END,values=row)
    con.commit()
    con.close()
    sid_entry.focus()

#Checks field inputs for null values or invalid datatypes and prompts an error message
def check_input():
    if sid_var.get() and sname_var.get() and rating_var.get() and age_var.get():
        if not sid_var.get().isdigit(): 
            messagebox.showerror(title="Value Error",message="Please enter an integer value for Sid.")
            sid_var.set("")
        elif not rating_var.get().isdigit(): 
            messagebox.showerror(title="Value Error",message="Please enter an integer value for Rating.")
            rating_var.set("")
        elif not age_var.get().isdigit(): 
            messagebox.showerror(title="Value Error",message="Please enter an integer value for Age.")
            age_var.set("")
        else:
            return True
    else:
        messagebox.showerror(title="Null Error",message="Please input all fields.")

#Insert data into the database
def add_data():
    if check_input():
        try:
            con,cur=get_cursor()
            query=f"insert into sailor values({sid_var.get()},'{sname_var.get()}',{rating_var.get()},{age_var.get()});" #insertion query
            cur.execute(query)
            con.commit()
            print("Data added successfully")
            con.close()
            display_database()
            clear_input() 
        except pymysql.Error as e:
            messagebox.showerror(title="SQL Error",message=e)

#Update data in the database
def update_data():
    if check_input():
        try:
            con,cur=get_cursor()
            query=f"update sailor set sname='{sname_var.get()}',rating={rating_var.get()},age={age_var.get()} where sid={sid_var.get()};" #update query
            cur.execute(query)
            con.commit()
            print("Data updated successfully")
            con.close()
            display_database()
            clear_input() 
        except pymysql.Error as e:
            messagebox.showerror(title="SQL Error",message=e)

#Delete data from the database
def delete_data():
    if sid_var.get():
        if not sid_var.get().isdigit(): 
            messagebox.showerror(title="Value Error",message="Please enter an integer value for Sid.")
            sid_var.set("")
        else:
            try:
                con,cur=get_cursor()
                query=f"delete from sailor where sid={sid_var.get()};" #deletion query
                cur.execute(query)
                con.commit()
                print("Data deleted successfully")
                con.close()
                display_database()
                clear_input() 
            except pymysql.Error as e:
                messagebox.showerror(title="SQL Error",message=e)
    else:
        messagebox.showerror(title="Null Error",message="Please input Sid to delete.")


#GUI related codes below
insert_frame=Frame(root,width=root.winfo_width()/3,bg=bgcolor)
display_frame=Frame(root,height=600,bg=bgcolor)

insert_frame.grid(row=0,column=0,sticky="nsew")
display_frame.grid(row=0,column=1,sticky="nsew")

sid_label=Label(insert_frame,text="Sid",font=("TkDefaultFont",10),bg=bgcolor)
sid_entry=ttk.Entry(insert_frame,textvariable=sid_var,width=28)
sname_label=Label(insert_frame,text="Sname",font=("TkDefaultFont", 10),bg=bgcolor)
sname_entry=ttk.Entry(insert_frame,textvariable=sname_var,width=28)
rating_label=Label(insert_frame,text="Rating",font=("TkDefaultFont", 10),bg=bgcolor)
rating_entry=ttk.Entry(insert_frame,textvariable=rating_var,width=28)
age_label=Label(insert_frame,text="Age",font=("TkDefaultFont", 10),bg=bgcolor)
age_entry=ttk.Entry(insert_frame,textvariable=age_var,width=28)

sid_label.grid(row=0,column=0,sticky="w",padx=(20,0),pady=(20,10))
sid_entry.grid(row=0,column=1,ipady=3,pady=(20,10),padx=(0,20))
sname_label.grid(row=1,column=0,sticky="w",padx=(20,10),pady=10)
sname_entry.grid(row=1,column=1,ipady=3,padx=(0,20))
rating_label.grid(row=2,column=0,sticky="w",padx=(20,0),pady=10)
rating_entry.grid(row=2,column=1,ipady=3,padx=(0,20))
age_label.grid(row=3,column=0,sticky="w",padx=(20,0),pady=10)
age_entry.grid(row=3,column=1,ipady=3,padx=(0,20))

btn_frame=Frame(insert_frame)
btn_frame.grid(row=4,columnspan=2,pady=20,sticky="s")

add_btn=ttk.Button(btn_frame,text="Add",width=18,command=add_data)
update_btn=ttk.Button(btn_frame,text="Update",width=18,command=update_data)
delete_btn=ttk.Button(btn_frame,text="Delete",width=18,command=delete_data)
clear_btn=ttk.Button(btn_frame,text="Clear",width=18,command=clear_input)

add_btn.grid(row=0,column=0,ipady=5)
update_btn.grid(row=0,column=1,ipady=5)
delete_btn.grid(row=1,column=0,ipady=5)
clear_btn.grid(row=1,column=1,ipady=5)

scroll_y=Scrollbar(display_frame,orient=VERTICAL)
database_table=ttk.Treeview(display_frame,columns=("sid","sname","rating","age"),yscrollcommand=scroll_y.set)
scroll_y.pack(side=RIGHT,fill=Y)
scroll_y.config(command=database_table.yview)
database_table.pack(fill=BOTH,expand=True,pady=20)

database_table.heading("sid",text="Sid")
database_table.heading("sname",text="Sname")
database_table.heading("rating",text="Rating")
database_table.heading("age",text="Age")
database_table.column("sid",width=20,anchor=CENTER)
database_table.column("sname",width=20,anchor=CENTER)
database_table.column("rating",width=20,anchor=CENTER)
database_table.column("age",width=20,anchor=CENTER)
database_table['show']="headings"
database_table.bind("<ButtonRelease-1>",get_input_data)

insert_frame.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

display_database()
root.mainloop() #runs the application