import imp
from tkinter import *
from tkinter import messagebox
from check_appointment import check_register_appointment
import sqlite3

con = sqlite3.connect('crm.db')
cur = con.cursor()


class Menage_appointment(Toplevel):
    def __init__(self):

        Toplevel.__init__(self)
        self.title("CRM System")
        self.geometry("700x550+350+200")
        self.resizable(False, False)

        self.top = Frame(self, height=150)
        self.data = {}
        self.top.pack(fill=X)
        self.bottom = Frame(self, height=600)
        self.bottom.pack(fill=X)
        self.heading = Label(self.top, text='View Schedule & Appointments',
                             font='arial 18 ')
        self.heading.place(x=195, y=60)

        self.scroll = Scrollbar(self.bottom, orient=VERTICAL)
        self.lb = Label(self.top, text='Choose the client to manage\n appointments for:',
                        font='arial 12 ')
        self.lb.place(x=250, y=98)

        self.listBox = Listbox(self.bottom, width=40, height=10, bg="silver", fg='black')
        #  self.listBox.grid(row=0,column=1,padx=(100,0))

        self.scroll.config(command=self.listBox.yview)

        self.listBox.config(yscrollcommand=self.scroll.set)
        self.listBox.bind("<<ListboxSelect>>", self.callback)

        lb = Label(self.bottom, text='Check Appointments:',
                   font='arial 10 ')
        lb.grid(row=1, column=1, padx=(100, 0))

        self.btnadd = Button(self.bottom, text="Check Appointments", font='arial 12 ', command=self.check_appointment)
        self.btnNaN = Label(self.bottom,
                            text="No Data Available. Go to\n the Manage Clients page &\n create a new client first.",
                            font='arial 16 ', width=21, height=4)
        clients = cur.execute("select* from'client_info'").fetchall()

        if (len(clients)) > 0:

            count = 0

            for client in clients:
                self.listBox.grid(row=0, column=1, padx=(90, 0))
                self.scroll.grid(row=0, column=2, sticky=N + S)
                self.listBox.insert(count, client[1])
                self.data[client[1]] = client
        #   self.id=client[0]

        else:

            self.btnNaN.grid(row=1, column=1, padx=(85, 0))

        back = Button(self.bottom, text='Back To Main Menu', width=15, height=3, font='arial 12 ', command=self.destroy)

        back.grid(row=4, column=0, padx=(10, 0), pady=(10, 0))

    def check_appointment(self):
        selected_item = self.listBox.curselection()
        appointment = self.listBox.get(selected_item)

        client_id = self.data[appointment][0]
        client_name = self.data[appointment][1]

        check_appointment = check_register_appointment(client_id, client_name)
        self.destroy()

    def callback(self, event):
        selection = event.widget.curselection()
        if selection:

            index = selection[0]
            data = event.widget.get(index)
            self.btnadd.grid(row=2, column=1, padx=(100, 0))
            # label.configure(text=data)
        else:

            self.btnadd.grid(row=902, column=1, padx=(100, 0))
            # label.configure(text="")
