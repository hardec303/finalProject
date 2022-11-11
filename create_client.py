from cgitb import grey
from msilib.schema import Icon
from string import whitespace
from tkinter import *
import sqlite3
from tkinter import messagebox
from turtle import bgcolor
con =sqlite3.connect('crm.db')
cur =con.cursor()



class Createclient(Toplevel):
    def __init__(self):
         Toplevel.__init__(self)
         self.title("CRM System")
         self.geometry("700x550+350+200")
         self.resizable(False,False)

         self.top= Frame(self,height=150)
         self.top.pack(fill=X)
         self.bottom= Frame(self,height=500)
         self.bottom.pack(fill=X)
         self.heading=Label(self.top, text='Create a Client',
                        font='arial 18 ')
         self.heading.place(x=260 ,y=60)

         self.lablel_fullname = Label(self.bottom, text="Utilize the same format as shown in the input fields below:", font='arial 10')
         self.lablel_fullname.place(x=49, y=-6)

         # fullname, sin, dob
         self.lablel_fullname=Label(self.bottom,text="Full name, SIN#, DOB:",font='arial 15')
         self.lablel_fullname.place(x=49,y=19)
         self.entry_fullname=Entry(self.bottom,width=30,bd=4)
         self.entry_fullname.insert(0,"John Doe, 999999999, 1960-01-01")
         self.entry_fullname.place(x=265,y=19)

         #jobtitle
         self.lablel_JobTittle=Label(self.bottom,text="Job title:",font='arial 15')
         self.lablel_JobTittle.place(x=49,y=49)
         self.entry_JobTittle=Entry(self.bottom,width=30,bd=4)
         self.entry_JobTittle.insert(0,"Manager")
         self.entry_JobTittle.place(x=150,y=49)
         #phonenumber
         self.lablel_phonenumber=Label(self.bottom,text="Phone number:",font='arial 15')
         self.lablel_phonenumber.place(x=49,y=79)
         self.entry_phonenumber=Entry(self.bottom,width=30,bd=4)
         self.entry_phonenumber.insert(0,"6040001111")
         self.entry_phonenumber.place(x=200,y=79)
         #buisnessphonenumber
         self.lablel_buisnessphonenumber=Label(self.bottom,text="Business phone number:",font='arial 15')
         self.lablel_buisnessphonenumber.place(x=49,y=109)
         self.entry_buisnessphonenumber=Entry(self.bottom,width=30,bd=4)
         self.entry_buisnessphonenumber.insert(0,"6040002222")
         self.entry_buisnessphonenumber.place(x=280,y=109)
         #networth
         self.lablel_networth=Label(self.bottom,text="Net worth:",font='arial 15')
         self.lablel_networth.place(x=49,y=139)
         self.entry_networth=Entry(self.bottom,width=30,bd=4)
         self.entry_networth.insert(0,"100000")
         self.entry_networth.place(x=150,y=139)
         #assets
         self.lablel_assets=Label(self.bottom,text="Assets:",font='arial 15')
         self.lablel_assets.place(x=49,y=169)
         self.entry_assets=Entry(self.bottom,width=30,bd=4)
         self.entry_assets.insert(0,"2 cars, 1 house")
         self.entry_assets.place(x=150,y=169)
         #liabilities
         self.lablel_liabilities=Label(self.bottom,text="Liabilities:",font='arial 15')
         self.lablel_liabilities.place(x=49,y=199)
         self.entry_liabilities=Entry(self.bottom,width=30,bd=4)
         self.entry_liabilities.insert(0,"Car payments, 2 CCs to pay off")
         self.entry_liabilities.place(x=150,y=199)
         #expenses
         self.lablel_expenses=Label(self.bottom,text="Expenses:",font='arial 15')
         self.lablel_expenses.place(x=49,y=229)
         self.entry_expenses=Entry(self.bottom,width=30,bd=4)
         self.entry_expenses.insert(0,"25000")
         self.entry_expenses.place(x=150,y=229)
         #email
         self.lablel_email=Label(self.bottom,text="E-mail:",font='arial 15')
         self.lablel_email.place(x=49,y=259)
         self.entry_email=Entry(self.bottom,width=30,bd=4)
         self.entry_email.insert(0,"email@johndoe.com")
         self.entry_email.place(x=150,y=259)
         


         btnadd=Button(self.bottom,text="Add New Client",font='arial 12 ',width=15,height=2,command=self.add_client)
         btnadd.place(x=270,y=320)
        
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

        client_error: bool = False

        #check if the client information contains errors

        if full_name == ""or job_tittle == ""or phone_number == ""or buisness_number == ""or net_worth == ""or assets == ""or liabilites == ""or Expenses == ""or email == "":
            messagebox.showinfo("Error","Please fill all the fields.")
            client_error = True
            self.destroy()

        if isinstance(full_name, str) is False or isinstance(job_tittle, str) is False or phone_number.isnumeric() is False or buisness_number.isnumeric() is False or net_worth.isnumeric() is False or isinstance(assets, str) is False or isinstance (liabilites, str) is False or Expenses.isnumeric() is False or isinstance(email, str) is False:
            messagebox.showinfo("Error","One or more user input is not in the correct format (numbers, letters, etc) Do not use the $ for money amounts.")
            client_error = True
            self.destroy()

        # checks if the full name is in the correct format prior to splitting it up into lists for further error checking
        if full_name.count('-') != 2 or full_name.count(',') != 2 or full_name.count(' ') < 2:
            messagebox.showinfo("Error",
                                "Please enter the names, social security number and date of birth seperated by commas and the date of birth in the YYYY-MM-DD format. Use spaces between the sections.")
            client_error = True
            self.destroy()
        else:
            # holds the name, sin number and dob in a list
            client_list = full_name.split(",")

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
            messagebox.showinfo("Error","Please enter a email with a @ symbol.")
            client_error = True
            self.destroy()

        if len(buisness_number) != 10:
            messagebox.showinfo("Error","Please enter a 10 digit phone number.")
            client_error = True
            self.destroy()
            
        if len(phone_number) != 10:
            messagebox.showinfo("Error","Please enter a 10 digit phone number.")
            client_error = True
            self.destroy()


        #if no errors are present, try to add the client into the db
        if client_error == False:
            try:
                query = "insert into 'client_info'('full_name','job_tittle','phone_number','buisness_number','net_worth','assets','liabilites','Expenses','email') values(?,?,?,?,?,?,?,?,?)"
                cur.execute(query, (
                full_name, job_tittle, phone_number, buisness_number, net_worth, assets, liabilites, Expenses, email))
            except:
                messagebox.showerror("Error")
                self.destroy()
            else:
                con.commit()
                messagebox.showinfo("Success", "Client was added successfully.")
                self.destroy()
