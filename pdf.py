

from tkinter import *
from tkinter import messagebox
from check_appointment import check_register_appointment 
import sqlite3
from fpdf import FPDF
con =sqlite3.connect('crm.db')
cur =con.cursor()
class generate_pdf(Toplevel):
    def __init__(self):

         Toplevel.__init__(self)
         self.title("CRM System")
         self.geometry("700x550+350+200")
         self.resizable(False,False)


         self.top= Frame(self,height=150)
         self.top.pack(fill=X)
         self.bottom= Frame(self,height=600)
         self.bottom.pack(fill=X)
         self.heading=Label(self.top, text='Generate Reports',
                        font='arial 18 ')
         self.heading.place(x=275 ,y=40)
         
         self.scroll =Scrollbar(self.bottom,orient=VERTICAL)
         
        
         self.lb=Label(self.top, text='Choose the client to generate reports \n for. Selecting a client will save their \n client profile as a PDF file in the same \n folder of the program:',
                        font='arial 8' )
         self.lb.place(x=278 ,y=80,)

         self.listBox =Listbox(self.bottom,width=42,height=10,bg="silver", fg='black')
        #  self.listBox.grid(row=0,column=1,padx=(80,0))
         
         self.scroll.config(command=self.listBox.yview)

         self.listBox.config(yscrollcommand=self.scroll.set)
         self.listBox.bind("<<ListboxSelect>>", self.callback)

         self.btnNaN=Label(self.bottom,text="No Data Available. Go \nto the Manage Clients page \n& create a new client.",font='arial 16 ',width=22,height=4)
        
        
         lb=Label(self.bottom, text='Select the client & generate the report:',
                        font='arial 10 ')
         lb.grid(row=1,column=1,padx=(75,0))
         
         self.btnadd=Button(self.bottom,text=" Generate Report",font='arial 12 ',command=self.Generate_pdf)
         
         clients=cur.execute("select* from'client_info'").fetchall()
         if (len(clients))>0:
             
                 count=0
              
                 for client in clients:
                  self.listBox.grid(row=0,column=1,padx=(90,0))
                  self.scroll.grid(row=0,column=2 ,sticky=N+S)
                  self.listBox.insert(count,client[1])
                  self.client_iid=client[0]
                
                 
         else:
             
            self.btnNaN.grid(row=2,column=1,padx=(85,0))
        
         
        
         back=Button(self.bottom,text='Back To Main Menu',width=15,height=3, font='arial 12 ' ,command=self.destroy)
         
         back.grid(row=4,column=0,padx=(10,0),pady=(100,0))
         
    def Generate_pdf(self):
        selected_item =self.listBox.curselection()
        appointment=self.listBox.get(selected_item)
        client_id=appointment
        #print(client_id)
        clients=cur.execute("select * from client_info where full_name ='{}'".format(client_id)).fetchall()
     
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 45)
        pdf.cell(200,10,txt="Client Report\n",ln=1,align = 'L')
        pdf.set_font("Arial", size = 20)
        pdf.cell(200,10,txt="==="*15,ln=1,align = 'L')
        pdf.set_font("Arial", size = 15)
        f = clients
        #print(f[0])
        data = ['Client ID','Full Name, SIN#, DOB:','Job Title:','Phone Number:','Business Phone Number:','Net Worth:','Assets:','Liabilities:','Expenses:','E-mail:']
        for x,y in zip(f[0],data):
            string = " * {:<40} {:<30}".format(str(y),str(x))
            pdf.cell(200, 15, txt = string, ln = 1, align = 'L')
        try:
            pdf.output(f[0][1]+".pdf")
        except EXCEPTION as e:
            messagebox.showerror("Error", str(e))
        else:
            messagebox.showinfo("Success", "Report was generated successfully.")

         
    def callback(self,event):
        selection = event.widget.curselection()
        if selection:
           
            index = selection[0]
            data = event.widget.get(index)
            self.btnadd.grid(row=2,column=1,padx=(100,0))
            # label.configure(text=data)
        else:
           
            self.btnadd.grid(row=902,column=1,padx=(100,0))
            # label.configure(text="")

    
