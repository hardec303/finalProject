from cgitb import grey
from msilib.schema import Icon
from string import whitespace
from tkinter import *
import sqlite3
from tkinter import messagebox
from turtle import bgcolor
con =sqlite3.connect('crm.db')
cur =con.cursor()



class updateclient(Toplevel):
    def __init__(self,client_id):
         Toplevel.__init__(self)
         self.title("CRM System")
         self.geometry("700x550+350+200")
         self.resizable(False,False)
         self.clientID=client_id
      
         query="select * from client_info where full_name = '{}'".format(client_id)
         result=cur.execute(query).fetchone()
      
         client1_id= result[0]
         self.id=client1_id
         self.top= Frame(self,height=150)
         self.top.pack(fill=X)
         self.bottom= Frame(self,height=500)
         self.bottom.pack(fill=X)
         self.heading=Label(self.top, text='Update '+""+result[1],
                        font='arial 18 ')
         self.heading.place(x=46 ,y=60)

         self.lablel_fullname = Label(self.bottom, text="If it doesn't update when you click update, you used incorrect format. Retry with the correct format.", font='arial 10')
         self.lablel_fullname.place(x=49, y=-6)

         # fullname
         self.lablel_fullname=Label(self.bottom,text="Full name, SIN#, DOB:",font='arial 15')
         self.lablel_fullname.place(x=49,y=19)
         self.entry_fullname=Entry(self.bottom,width=30,bd=4)
         self.entry_fullname.insert(0,result[1])
         self.entry_fullname.place(x=265,y=19)

         #jobtitle
         self.lablel_JobTittle=Label(self.bottom,text="Job title:",font='arial 15')
         self.lablel_JobTittle.place(x=49,y=49)
         self.entry_JobTittle=Entry(self.bottom,width=30,bd=4)
         self.entry_JobTittle.insert(0,result[2])
         self.entry_JobTittle.place(x=150,y=49)
         #phonenumber
         self.lablel_phonenumber=Label(self.bottom,text="Phone number:",font='arial 15')
         self.lablel_phonenumber.place(x=49,y=79)
         self.entry_phonenumber=Entry(self.bottom,width=30,bd=4)
         self.entry_phonenumber.insert(0,result[3])
         self.entry_phonenumber.place(x=200,y=79)
         #buisnessphonenumber
         self.lablel_buisnessphonenumber=Label(self.bottom,text="Business phone number:",font='arial 15')
         self.lablel_buisnessphonenumber.place(x=49,y=109)
         self.entry_buisnessphonenumber=Entry(self.bottom,width=30,bd=4)
         self.entry_buisnessphonenumber.insert(0,result[4])
         self.entry_buisnessphonenumber.place(x=280,y=109)
         #networth
         self.lablel_networth=Label(self.bottom,text="Net worth:",font='arial 15')
         self.lablel_networth.place(x=49,y=139)
         self.entry_networth=Entry(self.bottom,width=30,bd=4)
         self.entry_networth.insert(0,result[5])
         self.entry_networth.place(x=150,y=139)
         #assets
         self.lablel_assets=Label(self.bottom,text="Assets:",font='arial 15')
         self.lablel_assets.place(x=49,y=169)
         self.entry_assets=Entry(self.bottom,width=30,bd=4)
         self.entry_assets.insert(0,result[6])
         self.entry_assets.place(x=150,y=169)
         #liabilities
         self.lablel_liabilities=Label(self.bottom,text="Liabilities:",font='arial 15')
         self.lablel_liabilities.place(x=49,y=199)
         self.entry_liabilities=Entry(self.bottom,width=30,bd=4)
         self.entry_liabilities.insert(0,result[7])
         self.entry_liabilities.place(x=150,y=199)
         #expenses
         self.lablel_expenses=Label(self.bottom,text="Expenses:",font='arial 15')
         self.lablel_expenses.place(x=49,y=229)
         self.entry_expenses=Entry(self.bottom,width=30,bd=4)
         self.entry_expenses.insert(0,result[8])
         self.entry_expenses.place(x=150,y=229)
         #email
         self.lablel_email=Label(self.bottom,text="E-mail:",font='arial 15')
         self.lablel_email.place(x=49,y=259)
         self.entry_email=Entry(self.bottom,width=30,bd=4)
         self.entry_email.insert(0,result[9])
         self.entry_email.place(x=150,y=259)
         


         btnadd=Button(self.bottom,text="Update Client",font='arial 12 ',width=15,height=2,command=self.add_client)
         btnadd.place(x=500,y=320)
        
    def add_client(self):
        id=self.id

    

        full_name=self.entry_fullname.get()
        job_tittle=self.entry_JobTittle.get()

        phone_number=self.entry_phonenumber.get()
        buisness_number=self.entry_buisnessphonenumber.get()
        net_worth=self.entry_networth.get()
        assets=self.entry_assets.get()
        liabilites=self.entry_liabilities.get()
        Expenses=self.entry_expenses.get()
        email=self.entry_email.get()
        
        #stores error variable to check for user input mistakes
        client_error: bool = False

        # check if the client information contains errors

        if full_name == "" or job_tittle == "" or phone_number == "" or buisness_number == "" or net_worth == "" or assets == "" or liabilites == "" or Expenses == "" or email == "":
            messagebox.showinfo("Error", "Please fill all the fields.")
            client_error = True
            self.destroy()

        if isinstance(full_name, str) is False or isinstance(job_tittle,str) is False or phone_number.isnumeric() is False or buisness_number.isnumeric() is False or net_worth.isnumeric() is False or isinstance(assets, str) is False or isinstance(liabilites,str) is False or Expenses.isnumeric() is False or isinstance(email,str) is False:
            messagebox.showinfo("Error", "One or more variable is not in the correct format (integer, string, etc).")
            client_error = True
            self.destroy()

        # checks if the full name is in the correct format prior to splitting it up into lists for further error checking
        if full_name.count('-') != 2 or full_name.count(',') != 2:
            messagebox.showinfo("Error",
                                "Please enter the names, social security number and date of birth seperated by commas and the date of birth in the YYYY-MM-DD format.")
            client_error = True
            self.destroy()
        else:
            # holds the name, sin number and dob in a list
            client_list = full_name.split(",")

            # date of birth sections in a list
            date_of_birth_list = client_list[2].split("-")

            # checks the number of numbers  in the SIN number, must be a 9 digit number
            if len(client_list[1]) - client_list[1].count(' ') != 9:
                messagebox.showinfo("Error", "Please enter a SIN number with 9 digits.")
                client_error = True
                self.destroy()

            #checks if the SIN number is numeric
            if client_list[1].strip().isnumeric() == False:
                messagebox.showinfo("Error", "Please enter a SIN number with with only numeric characters.")
                client_error = True
                self.destroy()

            # checks if the date of birth is in the right format
            if client_list[2].count('-') != 2 or len(date_of_birth_list[0]) - date_of_birth_list[0].count(
                    ' ') != 4 or len(date_of_birth_list[1]) - date_of_birth_list[1].count(' ') != 2 or len(
                date_of_birth_list[2]) - date_of_birth_list[2].count(' ') != 2:
                messagebox.showinfo("Error", "Please enter the date of birth in the YYYY-MM-DD format.")
                client_error = True
                self.destroy()

        if email.count('@') < 1:
            messagebox.showinfo("Error", "Please enter a email with a @ symbol.")
            client_error = True
            self.destroy()

        if len(buisness_number) != 10:
            messagebox.showinfo("Error", "Please enter a 10 digit phone number.")
            client_error = True
            self.destroy()
            
        if len(phone_number) != 10:
            messagebox.showinfo("Error","Please enter a 10 digit phone number.")
            client_error = True
            self.destroy()

        # if no errors are present, try to upadate the client info in the db
        if client_error == False:
            query2="update appointment set full_name ='{}' where client_id={} " .format(full_name,id)
            query="update client_info set full_name ='{}', job_tittle='{}',phone_number={},buisness_number={},net_worth ={},assets='{}',liabilites='{}',Expenses={},email='{}' where client_id={} " .format(full_name,job_tittle,phone_number,buisness_number,net_worth,assets,liabilites,Expenses,email,id)

            try:
                cur.execute(query)
                cur.execute(query2)
            except Exception:
                messagebox.showinfo("Failure", "Client Information was entered in the wrong format.")
                self.destroy()
            else:
                con.commit()
                con.commit()
                messagebox.showinfo("Success", "Client updated successfully.")
                self.destroy()
