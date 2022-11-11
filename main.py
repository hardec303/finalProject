import time
from tkinter import *
import sqlite3
from menage_clint import Menage_client
from apointment import Menage_appointment
from calculator import calc
from expenses import expenses
from pdf import generate_pdf
import tkinter.ttk as ttk  # ttk is the themed tkinter
from tkinter import messagebox
import os  # os is a module that allows us to interact with the operating system
import pyglet  # pyglet is a module that allows us to use different fonts in python

dir_path = os.path.dirname(os.path.realpath(__file__)) # dir_path is the path of the current directory
pyglet.font.add_file(os.path.join(dir_path, 'files', 'pacifico-font', 'pacifico-v17-latin-regular.ttf')) # add font to pyglet
pyglet.font.add_file(os.path.join(dir_path, 'files', 'merriweather-font', 'merriweather-v28-latin-regular.ttf')) # add font to pyglet

con = sqlite3.connect('crm.db')
cur = con.cursor()


class Application(object):

    def __init__(self, master):
        self.style = ttk.Style()
        self.master = master
        self.top = Frame(master, height=150)
        self.top.pack(fill=X)
        self.bottom = Frame(master, height=500)
        self.bottom.pack(fill=X)
        self.initialRender(master)

    def myHash(self, text: str):
        hash = 0
        for ch in text:
            hash = (hash * 281 ^ ord(ch) * 997) & 0xFFFFFFFF
        return hash

    def loginFunction(self, master, username, password):
        hashedPassword = self.myHash(password.get())
        print(username, hashedPassword)
        query = "select * from User where UserName = '{0}'".format(username.get())
        result = cur.execute(query).fetchone()
        if(result is None):
            messagebox.showinfo("Error", "Incorrect username or password.")
            return

        if (result[2] != str(hashedPassword)):
            messagebox.showinfo("Error", "Incorrect username or password.")
            return


        print(result)
        if(result[2] == str(hashedPassword)):
            self.name = result[4] + ' ' + result[5]
            self.user = result
            self.userLabel.destroy()
            self.userInput.destroy()
            self.passwordLabel.destroy()
            self.passwordInput.destroy()
            self.loginButton.destroy()
            self.mainPageRender(master)

    def initialRender(self, master):
        self.userLabel = Label(self.bottom, text="User ID", font='arial 15', bg="white", fg="black")
        self.userLabel.pack()

        username = StringVar()
        self.userInput = ttk.Entry(self.bottom, textvariable=username, style="Username.TEntry", font=("Merriweather", 11))
        self.style.configure("Username.TEntry", foreground="black", background="#8c66ff", selectbackground="#007fff", selectforeground="white")
        self.userInput.pack(pady=(2,14))

        self.passwordLabel = Label(self.bottom, text="Password", font='arial 15', bg="white", fg="black")
        self.passwordLabel.pack()

        password = StringVar()
        self.passwordInput = ttk.Entry(self.bottom, textvariable=password, show='*', style="Password.TEntry", font=("Merriweather", 11))
        self.style.configure("Password.TEntry", foreground="black", background="#8c66ff", selectbackground="#007fff", selectforeground="white")
        self.passwordInput.pack(pady=(2,14))


        self.loginButton = ttk.Button(self.bottom, text="Login", style="Loginn.Accent.TButton", cursor="hand2", command=lambda: self.loginFunction(master, username, password))
        self.style.configure("Loginn.Accent.TButton", foreground="white", background="#8c66ff", font=("Merriweather", 12))
        self.loginButton.pack(pady=10, ipadx=30)

    def mainPageRender(self, master):
        self.heading = Label(self.top, text='Welcome', font='pacifico 26 bold')
        self.heading.pack(pady=23, anchor=CENTER)

        self.style.configure("nn.Accent.TButton", font='arial 12 bold')

        self.menageclient = ttk.Button(self.bottom, text='Manage Clients', width=28, style="nn.Accent.TButton", command=self.mypoeple)
        self.menageclient.pack(pady=15, ipady=10)

        self.viewappointment = ttk.Button(self.bottom, text='View & Schedule Appointments', width=28, style="nn.Accent.TButton", command=self.myappointment)
        self.viewappointment.pack(pady=15, ipady=10)

        self.generatereport = ttk.Button(self.bottom, text='Generate Reports', width=28, style="nn.Accent.TButton", command=self.pdf)
        self.generatereport.pack(pady=15, ipady=10)

        self.viewcalculator = ttk.Button(self.bottom, text='Calculator', width=28, style="nn.Accent.TButton", command=calc)
        self.viewcalculator.pack(pady=15, ipady=10)

        self.expense = ttk.Button(self.bottom, text='Expenses', width=28, style="nn.Accent.TButton", command= lambda: expenses(self.user))
        self.expense.pack(pady=15, ipady=10)


    def mypoeple(self):
        people = Menage_client()

    def myappointment(self):
        # pass
        people = Menage_appointment()

    def pdf(self):
        # pass
        people = generate_pdf()

    def calculator(self):
        calc()


def main():
    root = Tk()
    style = ttk.Style(root)
    root.tk.call('source', os.path.join(dir_path, 'files', 'Theme', 'forest-light.tcl'))
    style.theme_use('forest-light')
    root.iconbitmap(os.path.join(dir_path, 'files', 'app.ico'))
    # root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=os.path.join(dir_path, 'files', 'app-icon.png')))
    app = Application(root)
    root.title("CRM System")
    root.geometry("650x550+350+200")
    root.resizable(False, False)

    # ==================== Move Window to Center ==========================
    root.update()
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate))

    root.mainloop()


if __name__ == "__main__":
    main()
