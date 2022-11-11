

from tkinter import *
from tkinter import messagebox
from create_client import Createclient 
from update_client import  updateclient 
from view_client import viewclient
import sqlite3
con =sqlite3.connect('crm.db')
cur =con.cursor()
class Menage_client(Toplevel):
    def __init__(self):

         Toplevel.__init__(self)
         self.title("CRM System")
         self.geometry("700x550+350+200")
         self.resizable(False,False)


         self.top= Frame(self,height=150)
         self.top.pack(fill=X)
         self.bottom= Frame(self,height=600)
         self.bottom.pack(fill=X)
         self.heading=Label(self.top, text='Manage Clients',
                        font='arial 18 ')
         self.heading.place(x=260 ,y=60)
         
         self.scroll =Scrollbar(self.bottom,orient=VERTICAL)
         self.lb=Label(self.top, text='Existing Clients:',
                        font='arial 12 ')
         self.lb.place(x=283 ,y=128)

         self.listBox =Listbox(self.bottom,width=40,height=10,bg="silver", fg='black')
         
         self.listBox.config(yscrollcommand=self.scroll.set)
         self.listBox.bind("<<ListboxSelect>>", self.callback)
         self.listBox.place(x=130,y=200)
         self.scroll.config(command=self.listBox.yview)
         self.lb=Label(self.top, text='Existing Clients:',
                        font='arial 12 ')
         self.lb.place(x=283 ,y=128)


         


         
        
        
         lb=Label(self.bottom, text='Create New Client:',
                        font='arial 10 ')
         lb.grid(row=1,column=1,padx=(50,0))
         btnadd=Button(self.bottom,text="Create New Client",font='arial 12 ',command=self.createnewclient)
         btnadd.grid(row=2,column=1,padx=(50,0))
         self.btnNaN=Label(self.bottom,text="No Data Available",font='arial 16 ',width=17,height=4)
       
         clients=cur.execute("select* from`client_info`ORDER BY `client_id` ASC").fetchall()
         if (len(clients))>0:
               
                 count=0
                

                 for client in clients:
                  self.listBox.grid(row=0,column=1,padx=(50,0))
                  self.scroll.grid(row=0,column=2 ,sticky=N+S)
                  self.listBox.insert(count,client[1])
                 
         else:

            self.btnNaN.grid(row=1,column=1,padx=(65,0))
              
         
             
                
         self.btnupdate=Button(self.bottom,text="update",font='arial 12 ',bd=4,command=self.updateclient)
         
         self.btnview=Button(self.bottom,text="view",font='arial 12 ',bd=4,command=self.viewclient)
         
         self.btndell=Button(self.bottom,text="DELETE",font='arial 12 ',bd=0,command=self.dellet_client)
        
         btnback=Button(self.bottom,text="Back To Main Menu",font='arial 12 ',width=15,height=2,command=self.destroy)
         btnback.grid(row=5,column=0,padx=(10,20))
        
        #  back=Button(self.bottom,text='Back',width=15,height=3, font='arial 12 ')
        #  back.place(x=70,y=280)
         
    def createnewclient(self):
     client=Createclient()
     self.destroy()
    def updateclient(self):
     selected_item =self.listBox.curselection()
     appointment=self.listBox.get(selected_item)
    
     client_id=appointment
    
     client= updateclient(client_id)
    
     self.destroy()
    def viewclient(self):

     selected_item =self.listBox.curselection()
     appointment=self.listBox.get(selected_item)
     client_id=appointment.split(".")[0]
        
     client=viewclient(client_id)
     
    def callback(self,event):
        selection = event.widget.curselection()
        if selection:
           
            index = selection[0]
            data = event.widget.get(index)
            self.btnview.place(x=80,y=30)
            self.btnupdate.place(x=10,y=30)
            self.btndell.grid(row=0,column=3,pady=0)
            
            # label.configure(text=data)
        else:
           
            self.btnadd.grid(row=902,column=1,padx=(100,0))
            # label.configure(text="")
    
    def dellet_client(self):
        selected_item = self.listBox.curselection()
  
        client=self.listBox.get(selected_item)
       
        client_id=client
     
        query="DELETE from client_info where full_name='{}'".format(client_id)
        answer= messagebox.askquestion("Warning","Are you sure you want to delete?")
        if answer=="yes":
            try:

                cur.execute(query)
                con.commit()
                messagebox.showinfo("Success","Deleted")
            except Exception as e:
                messagebox.showinfo("info","str(e)")
        self.destroy()
