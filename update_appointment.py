from cgitb import grey
from msilib.schema import Icon
from string import whitespace
from tkinter import *
import sqlite3
from tkinter import messagebox
from turtle import bgcolor

import datetime
from datetime import date
from datetime import datetime


con = sqlite3.connect('crm.db')
cur = con.cursor()

current_day = datetime.now().day
current_month = datetime.now().month
current_year = datetime.now().year


def numOfDays(date1, date2):
    return (date2 - date1).days


class updateappointment(Toplevel):
    def __init__(self, appointment_client_name, appointment_client_id, appointment_name):
        Toplevel.__init__(self)
        self.title("CRM System")
        self.geometry("700x550+350+200")
        self.resizable(False, False)
        self.appointmentclient_name = appointment_client_name
        self.appointment_name_update = appointment_name
        self.appointment_client_id = appointment_client_id

        query = "select * from client_info where full_name = '{}'".format(self.appointmentclient_name)
        result = cur.execute(query).fetchone()
        self.name = result[1]
        buisness_phone = result[4]
        phone = result[3]
        email = result[9]
        query2 = "select * from appointment where appointment_name = '{}'".format(self.appointment_name_update)
        result2 = cur.execute(query2).fetchone()

        self.top = Frame(self, height=150)
        self.top.pack(fill=X)
        self.bottom = Frame(self, height=500)
        self.bottom.pack(fill=X)
        self.heading = Label(self.top, text="Update" + " " + result2[3],
                             font='arial 18 ')
        self.heading.place(x=46, y=60)

        self.appointment_name = Label(self.bottom,
                                      text="Input only words, numbers, commas, and periods in the name & details field.",
                                      font='arial 10')
        self.appointment_name.place(x=49, y=-6)

        # appointment_name
        self.appointment_name = Label(self.bottom, text="Appointment name:", font='arial 15')
        self.appointment_name.place(x=49, y=19)
        self.entry_appointment_name = Entry(self.bottom, width=30, bd=4)
        self.entry_appointment_name.insert(0, result2[3])
        self.entry_appointment_name.place(x=250, y=19)
        #  appointment_date
        self.apointment_date = Label(self.bottom, text="Appointment date:", font='arial 15')
        self.apointment_date.place(x=49, y=49)
        self.entry_appointment_date = Entry(self.bottom, width=30, bd=4, )
        self.entry_appointment_date.insert(0, result2[1])
        self.entry_appointment_date.bind("<FocusOut>", self.on_focus_out)
        self.text_date = Label(self.bottom, text="", font='arial 15')
        self.text_date.place(x=450, y=49)
        self.entry_appointment_date.insert(0, "")
        self.entry_appointment_date.place(x=250, y=49)
        # appointment details
        self.appointment_info = Label(self.bottom, text="Appointment details:", font='arial 15')
        self.appointment_info.place(x=49, y=79)
        self.entry_appointment_info = Entry(self.bottom, bd=4)
        self.entry_appointment_info.insert(0, result2[2])
        self.entry_appointment_info.place(x=250, y=79, width=190,
                                          height=100)
        self.lb = Label(self.bottom, text='Client contact details:',
                        font='arial 10 ')
        self.lb.place(x=49, y=180)
        #  #phonenumber
        self.lablel_phonenumber = Label(self.bottom, text="Phone number:", font='arial 15')
        self.lablel_phonenumber.place(x=49, y=210)
        self.lablel_phonenumber = Label(self.bottom, text=phone, font='arial 15')
        self.lablel_phonenumber.place(x=200, y=210)
        #  #Business_phonenumber
        self.lablel_phonenumber = Label(self.bottom, text="Business phone number:", font='arial 15')
        self.lablel_phonenumber.place(x=49, y=240)
        self.lablel_phonenumber = Label(self.bottom, text=buisness_phone, font='arial 15')
        self.lablel_phonenumber.place(x=280, y=240)
        # email
        self.lablel_phonenumber = Label(self.bottom, text="E-mail:", font='arial 15')
        self.lablel_phonenumber.place(x=49, y=270)
        self.lablel_phonenumber = Label(self.bottom, text=email, font='arial 15')
        self.lablel_phonenumber.place(x=120, y=270)
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
        self.btnback = Button(self.bottom, text="Update Appointment", font='arial 12 ', width=16, height=2,
                              command=self.add_appointment)
        self.btnback.place(x=490, y=300)

    #  btnadd=Button(self.top,text="Add New Client",font='arial 12 ')
    #  btnadd.place(x=250,y=400)
    #  back=Button(self.bottom,text="Back To Main Page",font='arial 12 ',width=15,height=2)
    #  back.place(x=30,y=320)
    def on_focus_out(self, event):
        if event.widget == self.entry_appointment_date:
            today_variable = date.today()
            days_variable = self.numOfDays(self.entry_appointment_date.get())

            # date_new = datetime.strptime(self.entry_appointment_date.get(), '%Y-%m-%d').date()
            # days = numOfDays(
            #  today,date_new,   
            # )

            self.text_date.config(text=f'{days_variable[0]} days {days_variable[1]} hours {days_variable[2]} min')

            # label.configure(text="I DON'T have focus")

    def days_hours_minutes(self, td):
        return td.days, td.seconds // 3600, (td.seconds // 60) % 60

    def numOfDays(self, date):
        date_time_str = date
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        now = date_time_obj - datetime.now()
        return self.days_hours_minutes(now)

    def add_appointment(self):
        client_id = self.appointment_client_id
        update_for_name = self.appointment_name_update

        full_name = self.appointmentclient_name
        appointment_name = self.entry_appointment_name.get()
        appointment_date = self.entry_appointment_date.get()
        appointment_information = self.entry_appointment_info.get()

        appointment_error: bool = False


        # checks if the date is in the format prior to splitting it up into a list for more error checking
        if appointment_date.count('-') != 2 or appointment_date.count(':') != 1 or appointment_date.count(' ') != 1:
            messagebox.showinfo("Error","Please enter the date in the YYYY-MM-DD H:M format. Use two dashes a colon and one space.")
            appointment_error: bool = True
            self.destroy()
        else:

            # list that contains the year, month and day+H+M sections
            date_list = appointment_date.split("-")
            # list that contains the day, and H+M sections
            day_time_list = date_list[2].split(" ")
            # list that contains the hour, and minute sections
            hour_minute_list = day_time_list[1].split(":")

            # checks if the date length is in the right format
            if len(date_list[0]) != 4 or len(date_list[1]) != 2 or len(
                    day_time_list[0]) != 2 or len(
                hour_minute_list[0]) != 2 or len(
                hour_minute_list[1]) != 2:
                messagebox.showinfo("Error","Please enter the date in the YYYY-MM-DD H:M format, the length of some sections is incorrect.")
                appointment_error: bool = True
                self.destroy()

            # checks that all inputs other than the dashes and colon are numeric
            if date_list[0].isnumeric() is False or date_list[1].isnumeric() is False or day_time_list[
                0].isnumeric() is False or hour_minute_list[0].isnumeric() is False or hour_minute_list[
                1].isnumeric() is False:
                messagebox.showinfo("Error","Please enter the date in the YYYY-MM-DD H:M format, some of the characters entered that were extpected to be numerals were incorrect.")
                appointment_error: bool = True
                self.destroy()

            # checks that the date not before the current day
            if int(date_list[0]) == int(current_year) and int(date_list[1]) == int(current_month) and int(
                    day_time_list[0]) < int(current_day):
                messagebox.showinfo("Error", "you have entered a date that is before the current date.")
                appointment_error = True
                self.destroy()

            # checks that the date not before the current month
            if int(date_list[0]) == int(current_year) and int(date_list[1]) < int(current_month):
                messagebox.showinfo("Error", "you have entered a date that is before the current date.")
                appointment_error = True
                self.destroy()

            # checks that the date not before the current year
            if int(date_list[0]) < int(current_year):
                messagebox.showinfo("Error", "you have entered a date that is before the current date.")
                appointment_error = True
                self.destroy()

        if appointment_error is False:
            try:
                query = "update appointment set full_name ='{}',appointment_name ='{}', appointment_date='{}',appointment_information='{}' ,client_id='{}' where appointment_name='{}' ".format(
                full_name, appointment_name, appointment_date, appointment_information, client_id, update_for_name)
                cur.execute(query)
                con.commit()
                messagebox.showinfo("Success", "Appointment was updated successfully.")
                self.destroy()
            except:
                messagebox.showerror("Error")
                self.destroy()
