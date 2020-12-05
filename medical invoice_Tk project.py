from tkinter import *
import time, mysql.connector,csv,os,subprocess
from PIL import Image
from ast import literal_eval
from mysql.connector import errorcode
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
class window(Tk):
    def __init__(self):
        super().__init__()
        # create sql connection obeject and testing connection
        try:
            with open("dbconn.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    self.username=str(row[0])
                    self.password=str(row[1])
                    self.host=str(row[2])
                    self.database=str(row[3])
                    self.tablename="medicalbill"
                    break
        except:
            messagebox.showerror("Error","Please configure database connection. Goto- Options->DB Connection")
        try:
            self.cnx = mysql.connector.connect(user=self.username, password=self.password, host=self.host, database=self.database)
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
        # else:
        #     self.cursor=self.cnx.cursor()
        #     self.cnx.close()

        # initializing window
        self.geometry("852x600+0+0")
        self.minsize(852,600)
        self.title("Medical Billing System")
        self.config(bg="powder blue")
        try:
            self.iconbitmap("icon.ico")
        except:
            pass
    def commit_db(self,query):
        self.cnx.database = self.database
        cursor=self.cnx.cursor()
        cursor.execute(query)
        self.cnx.commit()
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
        self.cnx.close() # Closing the connection before exit
        self.destroy()
class conn_window(Frame):
    def __init__(self):
        Frame.__init__(self)
        window1=Toplevel(self)
        window1.title("Database connection wizard")
        window1.geometry("500x150+100+100")
        try:
            window1.iconbitmap("dbconn.ico")
        except:
            pass
        # methods
        def updateconnfile(username,password,host,database):
            with open("dbconn.csv","w") as csv_file:
                file=csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                file.writerow([username,password,host,database])
        def updateConnectionData():
            user=username.get()
            passwd=password.get()
            hst=host.get()
            db=database.get()
            try:
                cnx = mysql.connector.connect(user=user, password=passwd, host=hst, database=db)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    Label(frame1,text="Invalid user name or Password", bg="red").pack(side=TOP,pady=3)
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    Label(frame1,text="Database doesnot exit. Creating Database...",bg="red").pack(side=TOP,pady=3)
                    # intializing connection
                    cnx = mysql.connector.connect(user=user, password=passwd, host=hst)
                    # creating cursor
                    cursor = cnx.cursor()
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db} DEFAULT CHARACTER SET 'utf8'")
                    # updating database details
                    cnx.database = db
                    Label(frame1,text=f"Success!!! Please restart the program to continue...",bg="green").pack(side=TOP,pady=3)
                    # initialing table
                    cursor.execute(f"CREATE TABLE `{db}`.`medicalbill` ( `srl_no` INT NOT NULL AUTO_INCREMENT,`invoice_no` INT NOT NULL , `customer` VARCHAR(50) NOT NULL , `address` VARCHAR(150) NOT NULL , `city` VARCHAR(50) NOT NULL , `state` VARCHAR(50) NOT NULL , `doctor` VARCHAR(50) NOT NULL , `purchage_data` TEXT NOT NULL , PRIMARY KEY (`srl_no`)) ENGINE = InnoDB")
                    # Intializing invoice number from 1001
                    # cursor.execute(f"ALTER TABLE medicalbill AUTO_INCREMENT=1001;")
                    cursor.close()
                    cnx.close()

                else:
                    Label(frame1,text=f"Error{err}", bg="red").pack(side=TOP,pady=3)
            else:
                Label(frame1,text="Success!!! Restart the program.",bg="green").pack(side=TOP)
                cnx.close()
            updateconnfile(username=user,password=passwd,host=hst,database=db)
            
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
        frame1=Frame(window1)
        frame1.pack(anchor="w",padx=10,pady=10)
        Button(frame1,text="update",font=font1,bg="skyblue",command=updateConnectionData).pack(padx=10,pady=5,side=LEFT)
        Button(frame1,text="close",font=font1,bg="skyblue",command=window1.destroy).pack(side=LEFT,padx=10)
class print_window(Frame):
    def __init__(self):
        Frame.__init__(self)
        window1=Toplevel(self)
        # definations
        def savedata():
            if check_duplicate_invoice(invoice=inv_no.get()):
                response=messagebox.askquestion("Question","Do you want to save DUPLICATE INVOICE?")
                if response == "yes":
                    savePDF()
                    clear_entries()
            else:
                savePDF()
                push_invoice()
        def savePDF():
            try:
                self.canvas.postscript(file="tmp.ps",colormode='color')
                file=asksaveasfilename(initialfile="Untitled.pdf",defaultextension=".pdf",filetypes=[("All Files","*.*"),("PDF Documents","*.pdf")])
                process = subprocess.Popen(["ps2pdf", "tmp.ps", file], shell=True)
                process.wait()
                os.remove("tmp.ps")
            except:
                messagebox.showerror("Error","Install Ghost Script and add it's bin and lib file to system envronment.")
                os.remove("tmp.ps")
        def printdata():
            try:
                self.canvas.postscript(file="tmp.ps",colormode='color')
                img=Image.open("tmp.ps")
                img.save("tmp.png")
                os.startfile("tmp.png","print")
                os.remove("tmp.ps")
            except:
                messagebox.showerror("Error","Install Ghost Script and add it's bin and lib file to system envronment.")
                os.remove("tmp.ps")
                os.remove("tmp.png")
        def checkprintdata():
            if check_duplicate_invoice(invoice=inv_no.get()):
                response=messagebox.askquestion("Question","Do you want to print DUPLICATE INVOICE?")
                if response == "yes":
                    printdata()
                    clear_entries()
            else:
                push_invoice()
                printdata()
        # Initializing Window
        window1.geometry("650x620+100+20")
        window1.minsize(650,600)
        window1.configure(bg="gray20")
        window1.title("Print")
        # Trying to set icon
        try:
            window1.iconbitmap("print.ico")
        except:
            pass
        # variables
        invoice=inv_no.get()
        customer=customer_name.get()
        c_address= local_add.get()
        c_city= city.get()
        c_state= state.get()
        doc= doctor.get()
        purchage_data= get_table()
        # FONTS
        fontlabel="Eras 9 bold"
        fontinvoice= "Lucida 13 bold"
        fontdata= "Lucida 13 normal"
        fontdata1= "Lucida 8 bold"
        fontdata2= "Lucida 8 normal"
        # Creatting frame for displaying preview
        frame1=Frame(window1)
        frame1.pack(fill=BOTH)
        # Frame for buttons
        frame2=Frame(window1,bg="gray30")
        frame2.pack(side=BOTTOM,fill=X)
        Button(frame2,text="Print",font=font2,bd=3,relief=RAISED,command=checkprintdata).pack(side=LEFT,padx=10,pady=5)
        Button(frame2,text="Save As PDF",font=font2,bd=3,relief=RAISED,command=savedata).pack(side=LEFT,padx=10,pady=5)
        Button(frame2,text="Cancel",font=font2,bd=3,relief=RAISED, command=window1.destroy).pack(side=LEFT,padx=10,pady=5)
        # creating casvas and ploting data
        self.canvaswidth=600
        self.canvasheight=550
        self.canvas=Canvas(window1,height=self.canvasheight,width=self.canvaswidth,bd=1,relief=GROOVE)
        self.canvas.create_text(300,25,font="Rockwell 17 bold",text="PAYMENT RECEIPT")
        self.canvas.create_line(0,45,600,45,dash=(200,1))
        self.canvas.create_text(10,70,font=fontlabel,text="INVOICE NUMBER:",anchor="w")
        self.canvas.create_text(120,70,font=fontinvoice,text=invoice,anchor="w")
        self.canvas.create_text(10,100,font=fontlabel,text="CUSTOMER NAME:",anchor="w")
        self.canvas.create_text(120,100,font=fontdata,text=customer,anchor="w")
        self.canvas.create_text(10,130,font=fontlabel,text="ADDRESS:",anchor="w")
        self.canvas.create_text(73,130,font=fontdata,text=c_address,anchor="w")
        self.canvas.create_text(392,130,font=fontlabel,text="CITY:",anchor="w")
        self.canvas.create_text(425,130,font=fontdata,text=c_city,anchor="w")
        self.canvas.create_text(380,160,font=fontlabel,text="STATE:",anchor="w")
        self.canvas.create_text(425,160,font=fontdata,text=c_state,anchor="w")
        self.canvas.create_text(10,160,font=fontlabel,text="REFERRED BY:",anchor="w")
        self.canvas.create_text(93,160,font=fontdata,text=doc,anchor="w")
        self.canvas.create_line(10,200,590,200) #table upper line
        self.canvas.create_line(10,400,590,400) #table bottom line
        self.canvas.create_line(10,200,10,400)  #table left line
        self.canvas.create_line(590,200,590,400)#table right line
        self.canvas.create_line(50,200,50,400,dash=(4,1))#table column1
        self.canvas.create_line(340,200,340,400,dash=(4,1))#table column2
        self.canvas.create_line(415,200,415,400,dash=(4,1))#table column3
        self.canvas.create_line(490,200,490,400,dash=(4,1))#table column4
        #self.canvas.create_line(10,230,590,230,dash=(4,1)) #table row1
        ycord=230
        a=0
        while a<10:
            self.canvas.create_line(10,ycord,590,ycord,dash=(4,1))
            ycord+=17
            a+=1
        self.canvas.create_text(20,210,font=fontdata1,text="Srl.",anchor="w")    
        self.canvas.create_text(70,210,font=fontdata1,text="MEDICINE NAME",anchor="w")
        self.canvas.create_text(365,210,font=fontdata1,text="QTY",anchor="w")
        self.canvas.create_text(425,210,font=fontdata1,text="UNIT PRICE",anchor="w")
        self.canvas.create_text(505,210,font=fontdata1,text="TOTAL PRICE",anchor="w")
        # self.canvas.create_text(25,233,font=fontdata1,text="1",anchor="w")
        ycord=238
        srl=1
        for srl in range(1,11):
            self.canvas.create_text(25,ycord,font=fontdata1,text=str(srl),anchor="w")
            ycord+=17
            srl+=1
        ycord=238
        xcord=[60,345,420,500]
        for row in range(10):
            for column in range(4):
                self.canvas.create_text(xcord[column],ycord,font=fontdata2,text=purchage_data[row][column],anchor="w")
            ycord+=17
        self.canvas.create_text(450,460,font=fontlabel,text="SIGNATURE",anchor="w")
        self.canvas.create_line(400,450,570,450)
        self.canvas.create_text(300,490,font="Bookman 14 bold",text="JENA MEDICAL STORE")
        self.canvas.create_text(300,510,font="Arial 11 normal",text="25/10 New market (Near SBI ATM), Choota Govindpur, Jamshedpur, pin-831010")
        self.canvas.create_text(300,525,font="Arial 8 normal",text="Busniess timing: 8AM - 8PM (online delivery abailabe on phone. Call 999999999 for enquiry)")
        self.canvas.create_text(300,542,font="Arial 8 normal",text="Tel- 0657 669 6652   Mobile- 999999999 / 88888888888")
        self.canvas.pack(padx=10,pady=10)
# Gui Variables for setting widets
font1="Arial 12 normal"
font2="Arial 13 normal"
theme="powder blue"
labelwidth=15
# Main Program
if __name__ == "__main__":
    # Definations here
    def clear_entries(row=10,column=4):
        '''Clear Previous entries'''
        rows=row+1
        columns=column+1
        customer_name.set("")
        local_add.set("")
        doctor.set("Dr. ")
        for row in range(1,rows):
            for column in range(1,columns):
                index = (row, column)
                entry[index].delete(0,'end')  
    def encodeList(list):
        '''Encoding algorith of list for database entry'''
        string=str(list)
        prepared_data=""
        for char in string:
            if char=="\'":
                prepared_data += "\\'"
            elif char==",":
                prepared_data += "\\,"
            else:
                prepared_data += char

        return prepared_data
    def decodeList(str):
        '''decoding algorithm for encoded list'''
        list=str.replace("\\","")
        list=literal_eval(list) #convering string to list
        return list
    def plot_invoice():
        '''Recreate invoice from invoice number. It connect to data base and fetch respective data from database.'''
        try:
            inv=inv_no.get()
            cursor= root.cnx.cursor()
            query=f"SELECT * FROM `medicalbill` where invoice_no={inv}"
            cursor.execute(query)
            row=cursor.fetchall()
            if row:
                clear_entries()
                cursor.execute(query)
                for(srl_no,invoice_no,customer,address,cty,ste,doc,purchage_data) in cursor:
                    customer_name.set(customer)
                    local_add.set(address)
                    city.set(cty)
                    state.set(ste)
                    doctor.set(doc)
                    decoded_list=decodeList(purchage_data)
                    set_table(decoded_list)
                    cursor.close()
            else:
                messagebox.showerror("Error","No Entry Found on database!!!")
                cursor.close()       
        except:
            messagebox.showerror("Error","Please Enter a Value. If value entered, Please check database connection.")
    def set_invoice_no():
        inv=get_invoice_no()
        inv_no.set(str(inv))
        frame1.update()
    def get_invoice_no():
        '''It coonect to database then fetch the last invoice number and return next invoice number'''
        try:
            cursor= root.cnx.cursor()
            query="SELECT * FROM `medicalbill` ORDER BY `invoice_no` DESC"
            cursor.execute(query)
            list= cursor.fetchall() #retuns a list of tupples(each result in a tuple).
            if not list:
                lastinv="1001"
            else:
                l=1
                for row in list:
                    if l==1:
                        inv=row[1]
                        l+=1
                    else:
                        continue   
                lastinv=inv+1
            cursor.close()
        except:
            cursor.close()
            messagebox.showerror("Error","Internal Error")
        return lastinv
    def create_invoice():
        '''Create a invoice without printing'''
        try:
            push_invoice()
        except:
            messagebox.showerror("error","Internal Error")
        else:
            set_invoice_no()
    def check_duplicate_invoice(invoice):
        cursor= root.cnx.cursor()
        query=f"SELECT * FROM `medicalbill` WHERE invoice_no={invoice}"
        cursor.execute(query)
        row= cursor.fetchall()
        cursor.close()
        if row:
            return True #duplicate exist
        else:
            return False
    def validate_form():
        '''Form Validation'''
        invoice= inv_no.get()
        customer=customer_name.get()
        table= get_table()
        count=1
        if invoice=="":
            messagebox.showwarning("Information","Invoice Number Required!")
            return False
        elif customer=="":
            messagebox.showwarning("Information","Customer Name Required!")
            return False
        elif table[0][0]=="":
            messagebox.showwarning("Information","Atleast 1 Item Required!")
            return False
        elif count==1:
            rowcount=1
            for row in table:
                if row[0] != "":
                    if row[1]=="" or row[2]=="" or row[3]=="":
                        messagebox.showwarning("Information",f"Fill all details in Row No-{rowcount}")
                        return False
                rowcount+=1
            return True    
    def push_invoice():
        '''It push invoice data entered by user to database'''
        root.update_status("Pushing data to database...")
        invoice= get_invoice_no()
        if check_duplicate_invoice(invoice):
            messagebox.showerror("Error","Duplicate Entry Found")
        elif validate_form():
            print("pushing data")
            customer=customer_name.get()
            purchage_data= get_table()
            c_address= local_add.get()
            c_city= city.get()
            c_state= state.get()
            doc= doctor.get()
            #encoding list data to insert into db
            prepared_data= encodeList(purchage_data)              
            try:
                root.commit_db(query=f"INSERT INTO `{root.database}`.`{root.tablename}` (`invoice_no`,`customer`, `address`, `city`, `state`, `doctor`, `purchage_data`) VALUES ('{invoice}','{customer}', '{c_address}', '{c_city}', '{c_state}', '{doc}', '{prepared_data}')")
                messagebox.showinfo("Information","Invoice Created")
            except:
                messagebox.showerror("Error","Error Creating Invoice Entry")
            else:
                clear_entries()
        else:
            pass
        root.update_status()
    def about():
        '''Shows information about the application'''
        messagebox.showinfo("About","Developed By: ")
    def dbconn():
        '''Insentiate a database connection window'''
        # creating connection window
        new=conn_window()
    def create_table(master,row=4,column=10):
        '''
        Plot series of input boxes on GUI and store all addresses in entry dictionary which is a global variable.
        Note: Alter the value of row and column(Beacuse master of this grid managed by pack manager)
        '''
        global entry
        rows = row+1 #leaving space for labels eg: medicine name,qty,rate,total
        columns = column+1 #leaving space for labels eg: srl,1,2,3....
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
    def set_table(list,row=10,column=4):
        '''Set the value of table from list generated by get_table method'''
        rows=row+1
        columns=column+1
        for row in range(1,rows):
            for column in range(1,columns):
                index = (row, column)
                entry[index].insert(0,list[(row-1)][column-1])
    def print_invoice():
        '''calls print preview window'''
        if not validate_form():
            pass
        else:
            new= print_window()
    def get_table(row=10,column=4):
        '''Return a list of lists, containing the data inside the table'''
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
    optionsmenu.add_command(label="Print",command=print_invoice)
    optionsmenu.add_command(label="Exit",command=root.exit)
    mainmenu.add_cascade(label="Options",menu=optionsmenu)
    helpmenu=Menu(mainmenu,tearoff=0)
    helpmenu.add_command(label="About",command=about)
    mainmenu.add_cascade(label="Help",menu=helpmenu)
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
    # setting default values
    city.set("Jamshedpur")
    state.set("Jharkhand")
    doctor.set("Dr. ")
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
    Button(frame1,text="Get invoice No",bg="RoyalBlue3",font=font1,fg="white",command=set_invoice_no).grid(row=0,column=2,padx=7)
    Button(frame1,text="Load data from DB",bg="RoyalBlue3",font=font1,fg="white",command=plot_invoice).grid(row=0,column=3,padx=7)
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
    # creating entry table
    create_table(frame2,column,row)
    # creating table headers
    for text,col in table_title:
        root.create_grid_label(master=frame2,text=text,row=0,column=col,font=font1,relief=None)
    for row in range(1,11):
        root.create_grid_label(master=frame2,text=str(row),row=row,column=0,font=font1,bd=None,relief=None)
    # Frame3 for action buttons
    frame3=Frame(root,bg=theme)
    frame3.pack(anchor="w",padx=10)
    # frame3 containts
    # buttons
    root.create_button(frame3,"Create",side=LEFT,font=font2,padx=80,funcname=create_invoice)  
    root.create_button(frame3,"Print",side=LEFT,font=font2,padx=80,ipadx=20,funcname=print_invoice)  
    root.create_button(frame3,"Exit",side=LEFT,font=font2,padx=80,ipadx=25,funcname=root.exit)

    root.mainloop()