from cgitb import grey
from msilib.schema import Icon
from string import whitespace
from tkinter import *
import sqlite3
from tkinter import messagebox
from turtle import bgcolor
from datetime import date
from datetime import datetime
con =sqlite3.connect('crm.db')
cur =con.cursor()


def numOfDays(date1, date2):
    return (date2-date1).days
class viewappointment(Toplevel):
    def __init__(self,appointment_client_id,appointment_name,appointment_client_name):
         Toplevel.__init__(self)
         self.title("CRM System")
         self.geometry("700x550+350+200")
         self.resizable(False,False)
        
         self.appointment_client_id=appointment_client_id
         self.appointment_name=appointment_name
         self.appointment_client_name=appointment_client_name
         query="select * from client_info where client_id = '{}'".format(self.appointment_client_id)
         result=cur.execute(query).fetchone()
        
         buisness_phone=result[4]
         phone=result[3]
         email=result[9]
         
        

         self.top= Frame(self,height=150)
         self.top.pack(fill=X)
         self.bottom= Frame(self,height=500)
         self.bottom.pack(fill=X)
         
         # appointment_name
         query2="select * from appointment where appointment_name = '{}'".format(self.appointment_name)
         result2=cur.execute(query2).fetchone()
        
         self.heading=Label(self.top, text=result2[3],
                        font='arial 18 ')
         self.heading.place(x=46 ,y=60)
        #  buisness_phone=result[4]
        #  phone=result[3]
        #  email=result[9]
         self.appointment_name=Label(self.bottom,text="Appointment name:",font='arial 15')
         self.appointment_name.place(x=49,y=19)
         self.entry_appointment_name=Label(self.bottom,text=result2[3],font='arial 15')
         
         self.entry_appointment_name.place(x=250,y=19)
        
        #  appointment_date
         self.apointment_date=Label(self.bottom,text="Appointment date:",font='arial 15')
         self.apointment_date.place(x=49,y=49)
         self.entry_appointment_date=Label(self.bottom,text=result2[1],font='arial 15')
         
        #  self.entry_appointment_date.bind("<FocusOut>", self.on_focus_out)

        #  self.text_date=Label(self.bottom,text="",font='arial 15')
        #  self.text_date.place(x=450,y=49)
       
         self.entry_appointment_date.place(x=250,y=49)
         #appointment details
         self.appointment_info=Label(self.bottom,text="Appointment details:",font='arial 15')
         self.appointment_info.place(x=49,y=79)
         self.entry_appointment_info=Label(self.bottom,text=result2[2],font='arial 10')
    
         self.entry_appointment_info.place(x=230,y=79, width=490,
        height=100)
        
         self.lb=Label(self.bottom, text='Client contact details:',
                        font='arial 10 ' )
         self.lb.place(x=49 ,y=180)
        #  #phonenumber
         self.lablel_phonenumber=Label(self.bottom,text="Phone number:",font='arial 15')
         self.lablel_phonenumber.place(x=49,y=210)
         self.lablel_phonenumber=Label(self.bottom,text=phone,font='arial 15')
         self.lablel_phonenumber.place(x=200,y=210)
         #  #Business_phonenumber
         self.lablel_phonenumber=Label(self.bottom,text="Business phone number:",font='arial 15')
         self.lablel_phonenumber.place(x=49,y=240)
         self.lablel_phonenumber=Label(self.bottom,text=buisness_phone,font='arial 15')
         self.lablel_phonenumber.place(x=280,y=240)
         #email
         self.lablel_phonenumber=Label(self.bottom,text="E-mail:",font='arial 15')
         self.lablel_phonenumber.place(x=49,y=270)
         self.lablel_phonenumber=Label(self.bottom,text=email,font='arial 15')
         self.lablel_phonenumber.place(x=120,y=270)
        #  self.entry_phonenumber=Entry(self.bottom,width=30,bd=4)
        #  self.entry_phonenumber.insert(0,"")
        #  self.entry_phonenumber.place(x=200,y=79)
        #  #Businessphonenumber
        #  self.lablel_buisnessphonenumber=Label(self.bottom,text="Business Phone number",font='arial 15')
        #  self.lablel_buisnessphonenumber.place(x=49,y=109)
        #  self.entry_buisnessphonenumber=Entry(self.bottom,width=30,bd=4)
        #  self.entry_buisnessphonenumber.insert(0,"")
        #  self.entry_buisnessphonenumber.place(x=280,y=109)
         
         
         
        #  #email
        #  self.lablel_email=Label(self.bottom,text="email",font='arial 15')
        #  self.lablel_email.place(x=49,y=259)
        #  self.entry_email=Entry(self.bottom,width=30,bd=4)
        #  self.entry_email.insert(0,"")
        #  self.entry_email.place(x=150,y=259)
         self.btnback=Button(self.bottom,text="Back To Main Menu",font='arial 12 ',width=16,height=2,command=self.destroy)
         self.btnback.place(x=490,y=300)


        #  btnadd=Button(self.top,text="Add New Client",font='arial 12 ')
        #  btnadd.place(x=250,y=400)
        #  back=Button(self.bottom,text="Back To Main Menu",font='arial 12 ',width=15,height=2)
        #  back.place(x=30,y=320)
    def on_focus_out(self,event):
        if event.widget == self.entry_appointment_date:
            

            today = date.today()
            date_new = datetime.strptime(self.entry_appointment_date.get(), '%Y-%m-%d').date()
            days = numOfDays(
             today,date_new,   
            )
           

            self.text_date.config(text = f'{days} days')
           
            # label.configure(text="I DON'T have focus")
    def add_appointment(self):
        
        client_id=self.clientID
        appointment_name=self.entry_appointment_name.get()

        appointment_date=self.entry_appointment_date.get()
        appointment_information=self.entry_appointment_info.get()
        
        if appointment_name and appointment_date and appointment_information  !="":
            try:
                query="insert into 'appointment'('client_id','appointment_name','appointment_date','appointment_information') values(?,?,?,?)"
                cur.execute(query,(client_id,appointment_name,appointment_date,appointment_information))
                con.commit()
                messagebox.showinfo("Success","Appointment added successfully")
            except EXCEPTION as e:
                messagebox.showerror("Error",str(e))
        else:
            messagebox.showerror("Error","fill all fields",icon='warning')
        