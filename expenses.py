from cgitb import grey
from msilib.schema import Icon
from string import whitespace
from tkinter import *
import sqlite3
from tkcalendar import Calendar
from tkinter import messagebox
from turtle import bgcolor

con = sqlite3.connect('crm.db')
cur = con.cursor()


class expenses(Toplevel):
    def __init__(self, user):
        Toplevel.__init__(self)
        self.user = user
        self.title("CRM System")
        self.geometry("700x550+350+200")
        self.resizable(False, False)

        self.total = 0.0

        self.totalCount = StringVar()
        self.totalCount.set(self.total)

        self.top = Frame(self, height=150)
        self.top.pack(fill=X)
        self.bottom = Frame(self, height=500)
        self.bottom.pack(fill=X)
        self.heading = Label(self.top, text='Expenses',
                             font='arial 18 ')
        self.heading.place(x=280, y=60)

        self.currentVal = StringVar(self)
        self.currentVal.set("Other")


        self.label1 = Label(self, text='Type')
        self.label1.pack()
        self.label1.place(x=130, y=100)

        self.label2 = Label(self, text='Amount')
        self.label2.pack()
        self.label2.place(x=280, y=100)

        self.label3 = Label(self, text='Date')
        self.label3.pack()
        self.label3.place(x=460, y=100)

        self.expenseType = OptionMenu(self, self.currentVal, "Marketing", "Membership", "Fuel", "Gift", "Reimbursement", "Other")
        self.expenseType.pack()
        self.expenseType.place(x=125, y=145)

        self.amount = Entry(self)
        self.amount.pack()
        self.amount.place(x=275, y=150)

        self.date = Entry(self)
        self.date.pack()
        self.date.place(x=450, y=150)

        self.totalLabel = Label(self, text='Total')
        self.totalLabel.pack()
        self.totalLabel.place(x=150, y=450)


        self.totalLabel = Label(self, textvariable=self.totalCount)
        self.totalLabel.pack()
        self.totalLabel.place(x=200, y=450)


        self.list = Listbox(
            self,
            font=('arial'),
            bg="#222222",
            fg="#ffffff",
            selectbackground="#00aa00",
            width=40
        )
        self.list.pack(fill=BOTH, expand=550)
        self.list.place(x=125, y=200)


        self.loginButton = Button(self, text="Add Expense", cursor="hand2", command=lambda : self.createExpense())
        self.loginButton.pack(pady=10, ipadx=30)
        self.loginButton.place(x=500, y=450)

        self.loadItems(self.user[0])

    def InsertItem(self, Type, Amount, Date):
        self.total += float(Amount)
        self.list.insert(END, "{0} / {1} / {2}".format(Type, Amount, Date))
        self.totalCount.set(self.total)


    def createExpense(self):
        type = self.currentVal.get()
        amount = self.amount.get()
        date = self.date.get()
        id = self.user[0]
        print(type, amount, date)
        query = "insert into Expenses (UserID, Type, Amount, Date) Values ({0}, '{1}', {2}, '{3}')".format(int(id), type, float(amount), date)
        print(query)
        cur.execute(query)
        con.commit()
        self.InsertItem(type, amount, date)
        self.amount.delete(0, END)
        self.date.delete(0, END)

    def loadItems(self, id):

        query = "select * from expenses where UserID = {0}".format(int(id))
        items = cur.execute(query).fetchall()

        for val in items:
            self.InsertItem(val[2], val[3], val[4])











