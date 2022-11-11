from tkinter import *
from tkinter import messagebox
from create_client import Createclient
import sqlite3
from new_appointment import Createnewappointment
from update_appointment import updateappointment
from view_appointment import viewappointment

con = sqlite3.connect('crm.db')
cur = con.cursor()


class check_register_appointment(Toplevel):
    def __init__(self, client_id, client_name):

        Toplevel.__init__(self)
        self.title("CRM System")
        self.geometry("700x550+350+200")
        self.resizable(False, False)

        self.id = client_id
        self.name = client_name

        self.top = Frame(self, height=150)
        self.top.pack(fill=X)
        self.bottom = Frame(self, height=600)
        self.bottom.pack(fill=X)
        self.heading = Label(self.top, text=self.name,
                             font='arial 18 ')
        self.heading.place(x=10, y=60)
        self.scroll = Scrollbar(self.bottom, orient=VERTICAL)
        self.lb = Label(self.top, text='Existing Appointments for Client:',
                        font='arial 12 ')
        self.lb.place(x=230, y=128)
        self.listBox = Listbox(self.bottom, width=40, height=10, bg="silver", fg='black')
        self.data = {}
        self.listBox.bind("<<ListboxSelect>>", self.callback)

        self.scroll.config(command=self.listBox.yview)

        self.listBox.config(yscrollcommand=self.scroll.set)

        lb = Label(self.bottom, text='Create New Appointment:',
                   font='arial 10 ')
        lb.grid(row=1, column=1, padx=(50, 0))
        self.btndell = Button(self.bottom, text="DELETE", font='arial 12 ', bd=0, command=self.dellet_client)
        self.btnupdate = Button(self.bottom, text="update", font='arial 12 ', bd=4, command=self.updateclient)

        self.btnview = Button(self.bottom, text="view", font='arial 12 ', bd=4, command=self.viewclient)
        btnadd = Button(self.bottom, text="Create New Appointment", font='arial 12 ', command=self.createnewappointment)
        btnadd.grid(row=2, column=1, padx=(85, 32))
        self.btnNaN = Label(self.bottom, text="No Appointments Exist", font='arial 16 ', width=24, height=2)

        clients = cur.execute("select * from appointment where full_name ='{}'".format(self.name)).fetchall()

        if (len(clients)) > 0:

            count = 0

            for client in clients:
                self.listBox.grid(row=0, column=1, padx=(30, 0))
                self.scroll.grid(row=0, column=2, sticky=N + S)
                self.listBox.insert(count, client[3])
                self.data[client[3]] = client

        #   self.client_iid=client[0]

        else:

            self.btnNaN.grid(row=1, column=1, padx=(70, 0))

        btnback = Button(self.bottom, text="Back To Main Menu", font='arial 12 ', width=15, height=2,
                         command=self.destroy)
        btnback.grid(row=3, column=0, padx=(10, 20))

    #  back=Button(self.bottom,text='Back',width=15,height=3, font='arial 12 ')
    #  back.place(x=70,y=280)

    def createnewappointment(self):
        # selected_item = self.listBox.curselection()

        # client=self.listBox.get(selected_item)

        # client_id=client
        client = Createnewappointment(self.name)

        self.destroy()

    def updateclient(self):
        selected_item = self.listBox.curselection()
        appointment = self.listBox.get(selected_item)

        appointment_client_name = self.data[appointment][0]
        appointment_client_id = self.data[appointment][4]
        appointment_name = self.data[appointment][3]

        #  iid=self.newid

        client = updateappointment(appointment_client_name, appointment_client_id, appointment_name)
        self.destroy()

    def viewclient(self):

        selected_item = self.listBox.curselection()
        appointment = self.listBox.get(selected_item)
        appointment_client_name = self.data[appointment][0]
        appointment_client_id = self.data[appointment][4]
        appointment_name = self.data[appointment][3]

        client = viewappointment(appointment_client_id, appointment_name, appointment_client_name)
        self.destroy()

    def dellet_client(self):
        selected_item = self.listBox.curselection()

        client = self.listBox.get(selected_item)

        client_id = client

        query = "DELETE from appointment where appointment_name='{}'".format(client_id)
        answer = messagebox.askquestion("Warning", "Are you sure you want to delete?")
        if answer == "yes":
            try:

                cur.execute(query)
                con.commit()

                messagebox.showinfo("Success", "Deleted")
            except Exception as e:
                messagebox.showinfo("info", "str(e)")
        self.destroy()

    def callback(self, event):
        selection = event.widget.curselection()
        if selection:

            index = selection[0]
            data = event.widget.get(index)
            self.btnview.place(x=80, y=30)
            self.btnupdate.place(x=10, y=30)
            self.btndell.grid(row=0, column=3, pady=0)
            # label.configure(text=data)
        else:

            self.btnadd.grid(row=902, column=1, padx=(100, 0))
