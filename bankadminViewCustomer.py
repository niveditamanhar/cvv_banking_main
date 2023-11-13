import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
import db
import util
import customerDashboard
import mysql
from datetime import datetime
import accountStatements
import customerDeposits
import login
import customerFundTransfer
import bankadmin

bankadminViewCustomerWindow = ""


def close():
	print("--- Entering customerPayBillsWindow close() ---")
	global bankadminViewCustomerWindow
	bankadminViewCustomerWindow.destroy()


#------To clear the Fields--------
def clearFields():
	print("--- Entering clearFields() ---")
	
#----------------------------------

def logout():
	print("--- Entering logout()")
	close()
	login.loadLogin()

#--- navigate to dashboard -----
def switchToDashboard(uname):
	print("--- Entering switchToDashboard() ---" + uname)
	close()
	bankadmin.loadDashboard(uname)



#---- Load Cusotmers
def loadCustomers():
	#get a DBConnection
	con = db.getDBConnection()
	cur = con.cursor()

	#fetch the customer id generated
	cur.execute("select concat(fname,' ',lname) as customer_name from customer where username=%s",("admin",))
	customer_name = cur.fetchone()[0]


	#load all customers
	cur.execute("select concat(fname,' ',lname) as customer_name, a.acc_no, a.balance,c.phone,c.email  from customer c, accounts a where c.username!=%s and c.customer_id=a.customer_id",("admin",))
	account__holder_names = cur.fetchall()
	print("Number of Account Holders : ---- " + str(len(account__holder_names)))



	#Close the DB connection
	db.closeDBConnection(con)
	
	global bankadminViewCustomerWindow
	bankadminViewCustomerWindow = tk.Tk()
	bankadminViewCustomerWindow.title("Welcome to Hogsmeade Bank | View Customers")
	bankadminViewCustomerWindow.state("zoomed")
	bankadminViewCustomerWindow.columnconfigure(1, weight=6)

	#Logo
	logo = tk.Label(bankadminViewCustomerWindow,text="Hogsmeade Bank", font="Calibri 43")
	logo.grid(row=0,column=0,sticky="w", ipadx="2", columnspan=6)


	# Seperator object	
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(bankadminViewCustomerWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=1,column=0,columnspan=6, sticky='ew')


	

	#Error and Message Row
	messageFrame = tk.Frame(bankadminViewCustomerWindow)
	messageText = Label(messageFrame, text="Hi "+ customer_name, font="Calibri 16")
	messageSpacer_0 = Label(messageFrame, text="  ", font="Calibri 16")
	messageSpacer_1 = Label(messageFrame, text="  ", font="Calibri 16")
	messageSpacer_2 = Label(messageFrame, text="  ", font="Calibri 16")
	logoutButton = Button(messageFrame,text=" Logout ", font="Calibri 12",command=lambda: logout())
	messageFrame.grid(row=2,column=4,sticky="e")
	messageText.pack(side=LEFT)
	messageSpacer_0.pack(side=LEFT)
	logoutButton.pack(side=LEFT)
	messageSpacer_1.pack(side=LEFT)
	messageSpacer_2.pack(side=LEFT)



	#Customer Menu
	menuFrame = tk.Frame(bankadminViewCustomerWindow,width=350, height=100)
	menuSpacer_0 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_1 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_2 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_3 = Label(menuFrame, text="  ", font="Calibri 16")
	dashboardButton = Button(menuFrame,text=" Dashboard ", font="Calibri 12",command=lambda: switchToDashboard("admin"))


	#----------------------------------

		#Load Statements (Iterate over the transactions)
	# Add a Treeview widget
	s = ttk.Style()
	s.theme_use('clam')
	s.configure('Treeview.Heading', font="Calibri 14")
	tranSpacer_0 = Label(menuFrame, text="  ", font="Calibri 11")
	accountHolderNamesFrame = tk.Frame(bankadminViewCustomerWindow)
	tree = ttk.Treeview(accountHolderNamesFrame, column=("Name", "Account Number","Balance","Phone","Email"), show='headings', height=11)
	tree.column("# 1",width="200")
	tree.heading("# 1", text="Name")
	tree.column("# 2", width="175")
	tree.heading("# 2", text="Acc. Number")
	tree.column("# 3", width="100")
	tree.heading("# 3", text="Balance")
	tree.column("# 4", width="100")
	tree.heading("# 4", text="Phone")
	tree.column("# 5", width="125")
	tree.heading("# 5", text="Email")
	

	accountHolderNamesFrame.grid(row=8,column=0,sticky="e", ipadx=20, ipady=20)

	
	for row in account__holder_names:
		tree.insert('', 'end', text="1", values=(row[0],row[1],row[2],row[3],row[4]))	

	tranSpacer_0.pack(side=LEFT)
	tree.pack()




	#----------------------------------



	menuFrame.grid(row=3,column=0,sticky="w")
	menuSpacer_0.pack(side=LEFT)
	dashboardButton.pack(side=LEFT)

	

	#BlankRow
	blankRow = Label(bankadminViewCustomerWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=5,column=0,sticky="e",columnspan=6)


	


	# Seperator object
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(bankadminViewCustomerWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=12,column=0,columnspan=6, sticky='ew', pady=10)



	bankadminViewCustomerWindow.mainloop()