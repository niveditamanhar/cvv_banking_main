import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
import db
import util
import login
import datetime as dt
import bankadminViewCustomer

bankAdminWindow = ""


def logout():
	print("--- Entering logout()")
	close()
	login.loadLogin()


def close():
	print("--- Entering bankAdminWindow close() ---")
	global bankAdminWindow
	bankAdminWindow.destroy()


#------To clear the Fields--------
def clearFields():
	print("--- Entering clearFields() ---")
	
#----------------------------------


def switchToadminViewCustomerDetails():
	close()
	bankadminViewCustomer.loadCustomers()	



#------To validate--------
def loadDashboard(uname):
	print("--- Entering dashboard module for ---"+str(uname))


	#get a DBConnection
	con = db.getDBConnection()
	cur = con.cursor()

	#fetch the customer id generated
	cur.execute("select concat(fname,' ',lname) as customer_name from customer where username=%s",(uname,))
	customer_name = cur.fetchone()[0]


	#load todays transactions
	transactionSQL = "select * from transaction where date >= CURRENT_DATE AND date <= date_add(curdate(),interval 1 day)"
	print(transactionSQL)
	cur.execute("select * from transaction where date >= CURRENT_DATE AND date <= date_add(curdate(),interval 1 day)")
	transactions = cur.fetchall()
	print("Number of Transactions : ---- " + str(len(transactions)))



	#Close the DB connection
	db.closeDBConnection(con)
	
	global bankAdminWindow
	bankAdminWindow = tk.Tk()
	bankAdminWindow.title("Welcome to Hogsmeade Bank | Bank Admin")
	bankAdminWindow.state("zoomed")
	bankAdminWindow.columnconfigure(1, weight=6)

	#Logo
	logo = tk.Label(bankAdminWindow,text="Hogsmeade Bank", font="Calibri 43")
	logo.grid(row=0,column=0,sticky="w", ipadx="2", columnspan=6)


	# Seperator object
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(bankAdminWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=1,column=0,columnspan=6, sticky='ew')


	

	#Error and Message Row
	messageFrame = tk.Frame(bankAdminWindow)
	messageText = Label(messageFrame, text="Hi "+ customer_name, font="Calibri 14")
	#messageSpacer_0 = Label(messageFrame, text="  ", font="Calibri 14")
	messageSpacer_1 = Label(messageFrame, text="  ", font="Calibri 14")
	logoutButton = Button(messageFrame,text=" Logout ", font="Calibri 12",command=lambda: logout())
	messageFrame.grid(row=2,column=4,sticky="e")
	messageText.pack(side=LEFT)
	#messageSpacer_0.pack(side=LEFT)
	logoutButton.pack(side=LEFT)
	messageSpacer_1.pack(side=LEFT)



	#Admin Menu
	menuFrame = tk.Frame(bankAdminWindow,width=350, height=100)
	menuSpacer_1 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_2 = Label(menuFrame, text="  ", font="Calibri 16")
	ViewCustomerDetailsButton = Button(menuFrame,text=" View Customer Details ", font="Calibri 12",command=lambda: switchToadminViewCustomerDetails())
	#reportsButton = Button(menuFrame,text=" View Statement ", font="Calibri 12")
	#fundTransferButton = Button(menuFrame,text=" Fund Transfer ", font="Calibri 12")


	menuFrame.grid(row=3,column=0,sticky="w")
	menuSpacer_2.pack(side=LEFT)
	ViewCustomerDetailsButton.pack(side=LEFT)
	menuSpacer_1.pack(side=LEFT)
	#reportsButton.pack(side=LEFT)
	#fundTransferButton.pack(side=LEFT)


	#BlankRow
	blankRow = Label(bankAdminWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=6,column=0,sticky="e",columnspan=6)


	#Statement for today
	date = dt.datetime.now()
	dateFrame = tk.Frame(bankAdminWindow,width=350, height=20)
	dateSpace_0 = Label(dateFrame, text="  ", font="Calibri 12")
	dateText = Label(dateFrame, text="Statement for date :", font="Calibri 12")
	dateText_1 = Label(dateFrame,font="Calibri 12", bg="yellow", text=f"{date:%A, %B %d, %Y}")
	dateText.pack(side=LEFT)
	dateSpace_0.pack(side=LEFT)
	dateText_1.pack(side=LEFT)
	dateFrame.grid(row=7,column=0,sticky="w",ipadx=75)


	#Load Statements (Iterate over the transactions)
	# Add a Treeview widget
	s = ttk.Style()
	s.theme_use('clam')
	s.configure('Treeview.Heading', font="Calibri 14")
	tranSpacer_0 = Label(menuFrame, text="  ", font="Calibri 12")
	transactionFrame = tk.Frame(bankAdminWindow,width=300)
	tree = ttk.Treeview(transactionFrame, column=("Transaction Name", "Transaction Type", "Account Number", "Date","Amount"), show='headings', height=11)
	tree.column("# 1")
	tree.heading("# 1", text="Trans. Name")
	tree.column("# 2")
	tree.heading("# 2", text="Trans. Type")
	tree.column("# 3")
	tree.heading("# 3", text="Acc. Number")
	tree.column("# 4")
	tree.heading("# 4", text="Date")
	tree.column("# 5")
	tree.heading("# 5", text="Amount")

	transactionFrame.grid(row=8,column=0,sticky="e", ipadx=20, ipady=20)

	
	for row in transactions:
		tree.insert('', 'end', text="1", values=(row[2],row[3],row[1],row[4],row[5]))	

	tranSpacer_0.pack(side=LEFT)
	tree.pack()




	#BlankRow
	blankRow = Label(bankAdminWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=7,column=0,sticky="e",columnspan=6)


	

	



		


	# Seperator object
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(bankAdminWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=12,column=0,columnspan=6, sticky='ew', pady=10)











	bankAdminWindow.mainloop()