from cgitb import grey
from msilib.schema import Icon
from string import whitespace
from tkinter import *
import sqlite3
from tkinter import messagebox
from turtle import bgcolor
con =sqlite3.connect('crm.db')
cur =con.cursor()



class viewclient(Toplevel):
    def __init__(self,client_id):
         Toplevel.__init__(self)
         self.title("CRM System")
         self.geometry("700x550+350+200")
         self.resizable(False,False)
         self.clientID=client_id 
       
         query="select * from client_info where full_name = '{}'".format(client_id)
         result=cur.execute(query).fetchone()
        

         self.top= Frame(self,height=150)
         self.top.pack(fill=X)
         self.bottom= Frame(self,height=500)
         self.bottom.pack(fill=X)
         self.heading=Label(self.top, text='View Client Details',
                        font='arial 18 ')
         self.heading.place(x=260 ,y=60)
         # fullname
         self.lablel_fullname=Label(self.bottom,text="Full name, SIN#, DOB:",font='arial 15')
         self.lablel_fullname.place(x=49,y=14)
         self.entry_fullname=Label(self.bottom,text=result[1],font='arial 12')
        
         self.entry_fullname.place(x=265,y=17)

         #jobtitle
         self.lablel_JobTittle=Label(self.bottom,text="Job title:",font='arial 15')
         self.lablel_JobTittle.place(x=49,y=45)
         self.entry_JobTittle=Label(self.bottom,text=result[2],font='arial 12')
        
         self.entry_JobTittle.place(x=150,y=49)
         #phonenumber
         self.lablel_phonenumber=Label(self.bottom,text="Phone number:",font='arial 15')
         self.lablel_phonenumber.place(x=49,y=76)
         self.entry_phonenumber=Label(self.bottom,text=result[3],font='arial 12')
         
         self.entry_phonenumber.place(x=200,y=79)
         #buisnessphonenumber
         self.lablel_buisnessphonenumber=Label(self.bottom,text="Business phone number:",font='arial 15')
         self.lablel_buisnessphonenumber.place(x=49,y=106)
         self.entry_buisnessphonenumber=Label(self.bottom,text=result[4],font='arial 12')
        
         self.entry_buisnessphonenumber.place(x=280,y=109)
         #networth
         self.lablel_networth=Label(self.bottom,text="Net worth:",font='arial 15')
         self.lablel_networth.place(x=49,y=136)
         self.entry_networth=Label(self.bottom,text=result[5],font='arial 12')
        
         self.entry_networth.place(x=150,y=139)
         #assets
         self.lablel_assets=Label(self.bottom,text="Assets:",font='arial 15')
         self.lablel_assets.place(x=49,y=166)
         self.entry_assets=Label(self.bottom,text=result[6],font='arial 12')
         
         self.entry_assets.place(x=150,y=169)
         #liabilities
         self.lablel_liabilities=Label(self.bottom,text="Liabilities:",font='arial 15')
         self.lablel_liabilities.place(x=49,y=196)
         self.entry_liabilities=Label(self.bottom,text=result[7],font='arial 12')
        
         self.entry_liabilities.place(x=150,y=199)
         #expenses
         self.lablel_expenses=Label(self.bottom,text="Expenses:",font='arial 15')
         self.lablel_expenses.place(x=49,y=226)
         self.entry_expenses=Label(self.bottom,text=result[8],font='arial 12')
        
         self.entry_expenses.place(x=150,y=229)
         #email
         self.lablel_email=Label(self.bottom,text="E-mail:",font='arial 15')
         self.lablel_email.place(x=49,y=256)
         self.entry_email=Label(self.bottom,text=result[9],font='arial 12')
         
         self.entry_email.place(x=150,y=259)
         


         btnadd=Button(self.bottom,text="Back To Main Menu",font='arial 12 ',width=15,height=2,command=self.destroy)
         btnadd.place(x=285,y=320)
        
    def add_client(self):
        full_name=self.entry_fullname.get()
        job_tittle=self.entry_JobTittle.get()

        phone_number=self.entry_phonenumber.get()
        buisness_number=self.entry_buisnessphonenumber.get()
        net_worth=self.entry_networth.get()
        assets=self.entry_assets.get()
        liabilites=self.entry_liabilities.get()
        Expenses=self.entry_expenses.get()
        email=self.entry_email.get()
        if full_name and job_tittle and phone_number and buisness_number and net_worth and assets and liabilites and Expenses and email !="":
            try:
                query="insert into 'client_info'('full_name','job_tittle','phone_number','buisness_number','net_worth','assets','liabilites','Expenses','email') values(?,?,?,?,?,?,?,?,?)"
                cur.execute(query,(full_name,job_tittle,phone_number,buisness_number,net_worth,assets,liabilites,Expenses,email))
                con.commit()
                messagebox.showinfo("Success","Client was added successfully.")
            except EXCEPTION as e:
                messagebox.showerror("Error",str(e))
        else:
            messagebox.showerror("Error","Fill all the fields.",icon='warning')
        