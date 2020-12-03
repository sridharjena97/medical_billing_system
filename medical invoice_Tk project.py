from tkinter import *
import time, mysql.connector,csv
from mysql.connector import errorcode
from tkinter import messagebox
class window(Tk):
    def __init__(self):
        super().__init__()
        # create sql connection obeject and testing connection
        try:
            with open("dbconn.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    username=str(row[0])
                    password=str(row[1])
                    host=str(row[2])
                    database=str(row[3])
                    break
        except:
            messagebox.showerror("Error","Please configure database connection. Goto- Options->DB Connection")
        try:
            cnx = mysql.connector.connect(user=username, password=password, host=host, database=database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                messagebox.showerror(title="Error",message="Invalid user name or Password")
                print("Something is wrong with your user name or password. Goto: Options->DB Connection to setup connection")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                messagebox.showerror(title="Error",message="Database does not exsit. Goto: Options->DB Connection to setup connection")
                print("Database does not exist")
            else:
                messagebox.showerror(title="Error",message="Connection Error. Goto: Options->DB Connection to setup connection")
                print(err)
        else:
            cnx.close()

        # initializing window
        self.geometry("852x600+0+0")
        self.minsize(852,600)
        self.title("Hotel ManagemeBilling System")
        self.config(bg="powder blue")
        try:
            self.iconbitmap("notepad.ico")
        except:
            pass
    def statusbar(self):
        '''
        To show status at buttom of GUI
        '''
        self.status=StringVar()
        self.status.set("Ready")
        self.sbar=Label(self,textvariable=self.status,relief=SUNKEN,anchor="w")
        self.sbar.pack(side=BOTTOM,fill=X)
    def update_status(self,state="Ready",freeze=0):
        '''
        To update status of GUI
        '''
        self.status.set(state)
        self.sbar.update()
        if freeze>0:
            time.sleep(freeze)
    def create_button(self,master=None,btntxt="Button",bg="sky blue",relief=RAISED,bd=6,funcname=None,side=None,padx=3,pady=3,anchor=None,ipadx=10,ipady=None,**kwargs):
        '''
        To Create a button
        '''
        kargs={}
        for key,value in kwargs.items():
            kargs.__setitem__(key,value)
        btn=Button(master,text=btntxt,command=funcname,bg=bg,relief=relief,bd=bd,**kargs)
        btn.pack(side=side,padx=padx,pady=pady,anchor=anchor,ipadx=ipadx,ipady=ipady)
   
    def create_grid_label(self,master=None,text="unknown",bg=None,relief=SUNKEN,bd=None,padx=None,pady=None,ipady=None,ipadx=None,column=None,row=None,columnspan=None,rowspan=None,**kwargs):
        '''
        To Create a label
        '''
        kargs={}
        for key,value in kwargs.items():
            kargs.__setitem__(key,value)
        label=Label(master,text=text,bg=bg,relief=relief,bd=bd,**kargs)
        label.grid(ipadx=ipadx,ipady=ipady,columnspan=columnspan,rowspan=rowspan,row=row,column=column)
    def create_grid_entry(self,master=None,bg=None,variable=None,relief=SUNKEN,bd=None,padx=None,pady=None,ipady=None,ipadx=None,column=None,row=None,columnspan=None,rowspan=None,**kwargs):
        '''
        To Create a entry
        '''
        kargs={}
        for key,value in kwargs.items():
            kargs.__setitem__(key,value)
        entry=Entry(master,bg=bg,relief=relief,bd=bd,textvariable=variable,**kargs)
        entry.grid(ipadx=ipadx,ipady=ipady,padx=padx,pady=pady,columnspan=columnspan,rowspan=rowspan,row=row,column=column)
    def exit(self):
        self.destroy()
class conn_window(Frame):
    def __init__(self):
        Frame.__init__(self)
        window1=Toplevel(self)
        window1.title("Database connection wizard")
        window1.geometry("500x120+100+100")
        # variables
        # window1.configure(bg=theme)
        # font1="Arial 12 normal"
        # methods
        def updateConnectionData():
            user=username.get()
            passwd=password.get()
            hst=host.get()
            db=database.get()
            try:
                cnx = mysql.connector.connect(user=user, password=passwd, host=hst, database=db)
            except:
                Label(frame,text="Failed!!! Please try again...").grid(row=2,column=0)
            else:
                Label(frame,text="Success!!! Restart the program").grid(row=2,column=0)
                cnx.close()
            
        username=StringVar()
        password=StringVar()
        host=StringVar()
        database=StringVar()
        try:
            with open("dbconn.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    username.set(str(row[0]))
                    password.set(str(row[1]))
                    host.set(str(row[2]))
                    database.set(str(row[3]))
                    break
        except:
            messagebox.showinfo("Info","please enter appropriate details to continue")
            with open("dbconn.csv","w") as csv_file:
                file=csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                file.writerow(["lipun","1234","127.0.0.1","invoice"])
            window1.destroy()
            new=conn_window()
        frame=Frame(window1)
        frame.pack(anchor="w",padx=10,pady=10)
        Label(frame,text="User Name",font=font1).grid(row=0,column=0,padx=2,sticky="w")
        Entry(frame,textvariable=username).grid(row=0,column=1,padx=2)
        Label(frame,text="Password",font=font1).grid(row=1,column=0,padx=2,sticky="w")
        Entry(frame,textvariable=password).grid(row=1,column=1,padx=2)
        Label(frame,text="Host",font=font1).grid(row=0,column=2,padx=2,sticky="w")
        Entry(frame,textvariable=host).grid(row=0,column=3,padx=2)
        Label(frame,text="Database Name",font=font1).grid(row=1,column=2,padx=2,sticky="w")
        Entry(frame,textvariable=database).grid(row=1,column=3,padx=2)
        Button(window1,text="update",font=font1,bg="skyblue",command=updateConnectionData).pack(anchor="w",padx=10,pady=5)

        
font1="Arial 12 normal"
font2="Arial 13 normal"
theme="powder blue"
labelwidth=15
if __name__ == "__main__":
    # Definations here
    def dbconn():
        new=conn_window()
    def create_table(master,row,column):
        global entry
        rows = row+1
        columns = column+1
        # create the table of widgets
        for row in range(1,rows):
            for column in range(1,columns):
                index = (row, column)
                e = Entry(master,font=font2)
                e.grid(row=row, column=column, stick="nsew")
                entry[index] = e
        # adjust column weights so they all expand equally
        for column in range(columns):
            master.grid_columnconfigure(column, weight=1)
        # designate a final, empty row to fill up any extra space
        master.grid_rowconfigure(rows, weight=1)

    def get_table(row,column):
        '''Return a list of lists, containing the data in the table'''
        rows=row+1
        columns=column+1
        result = []
        for row in range(1,rows):
            current_row = []
            for column in range(1,columns):
                index = (row, column)
                current_row.append(entry[index].get())
            result.append(current_row)
        return result
    # Program Start
    root= window()
    root.statusbar()
    Label(root,text="Medical Billing System",bg="white",font="Algerian 30 bold",fg="SlateBlue3",bd=5,relief=GROOVE).pack(pady=6,ipadx=6,ipady=5)
    # menubar
    mainmenu=Menu(root)
    optionsmenu=Menu(mainmenu,tearoff=0)
    optionsmenu.add_command(label="DB Connection",command=dbconn)
    optionsmenu.add_separator()
    optionsmenu.add_command(label="Print")
    optionsmenu.add_command(label="Exit",command=root.exit)
    mainmenu.add_cascade(label="Options",menu=optionsmenu)
    root.configure(menu=mainmenu)
    # Creating a frame for taking basic details
    frame1=Frame(root,bg=theme)
    frame1.pack(anchor="nw",padx=10)
    # frame1 containts
    # Variables
    inv_no=StringVar()
    customer_name=StringVar()
    local_add=StringVar()
    city=StringVar()
    state=StringVar()
    doctor=StringVar()
    # Basic Details
    # labels
    root.create_grid_label(master=frame1,text="Invoice no :",font=font1,row=0,column=0,width=labelwidth,bg=theme,anchor="e")
    root.create_grid_label(master=frame1,text="Customer Name :",font=font1,row=1,column=0,width=labelwidth,bg=theme,anchor="e")
    root.create_grid_label(master=frame1,text="Address :",font=font1,row=2,column=0,width=labelwidth,bg=theme,anchor="e")
    root.create_grid_label(master=frame1,text="City :",font=font1,row=3,column=0,width=labelwidth,bg=theme,anchor="e")
    root.create_grid_label(master=frame1,text="State :",font=font1,row=4,column=0,width=labelwidth,bg=theme,anchor="e")
    root.create_grid_label(master=frame1,text="Pescribed By Dr :",font=font1,row=5,column=0,width=labelwidth,bg=theme,anchor="e")
    # Input Box
    root.create_grid_entry(master=frame1,variable=inv_no,row=0,column=1,font=font1,padx=3,bd=3)
    root.create_grid_entry(master=frame1,variable=customer_name,row=1,column=1,font=font1,padx=3,bd=3)
    root.create_grid_entry(master=frame1,variable=local_add,row=2,column=1,font=font1,padx=3,bd=3)
    root.create_grid_entry(master=frame1,variable=city,row=3,column=1,font=font1,padx=3,bd=3)
    root.create_grid_entry(master=frame1,variable=state,row=4,column=1,font=font1,padx=3,bd=3)
    root.create_grid_entry(master=frame1,variable=doctor,row=5,column=1,font=font1,padx=3,bd=3)
    Button(frame1,text="Load from database",bg="RoyalBlue3",font=font1,fg="white").grid(row=0,column=2,padx=7)
    # creating frame2 for taking medicine details
    frame2=Frame(root)
    frame2.pack(pady=10,anchor="w",padx=10)
    # frame2 containts
    # variables
    table_title=[("Srl",0),("Medicine Name",1),("Qty",2),("Rate",3),("Total",4)]
    # important constants for table
    row=4
    column=10
    entry = {}
    
    create_table(frame2,column,row)
    for text,col in table_title:
        root.create_grid_label(master=frame2,text=text,row=0,column=col,font=font1,relief=None)
    for row in range(1,11):
        root.create_grid_label(master=frame2,text=str(row),row=row,column=0,font=font1,bd=None,relief=None)
    # Frame3 for action buttons
    frame3=Frame(root,bg=theme)
    frame3.pack(anchor="w",padx=10)
    # frame3 containts
    # buttons
    root.create_button(frame3,"Create",side=LEFT,font=font2,padx=80)  
    root.create_button(frame3,"Print",side=LEFT,font=font2,padx=80,ipadx=20)  
    root.create_button(frame3,"Exit",side=LEFT,font=font2,padx=80,ipadx=25,funcname=root.exit) 
    
            



    root.mainloop()
