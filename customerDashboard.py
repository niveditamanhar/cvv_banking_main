import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
import db
import util
import customerDeposits
import accountStatements
import customerPayBills
import login
import customerFundTransfer

customerDashboardWindow = ""


def close():
	print("--- Entering customerDashboardWindow close() ---")
	global customerDashboardWindow
	customerDashboardWindow.destroy()


#------To clear the Fields--------
def clearFields():
	print("--- Entering clearFields() ---")
	
#----------------------------------


#--- navigate to deposit -----
def switchTodeposit(accNo,uname, customer_id):
	print("--- Entering switchTodeposit() ---" + accNo)
	print("--- Entering switchTodeposit() ---" + uname)
	print("--- Entering switchTodeposit() ---" + str(customer_id))
	close()
	customerDeposits.loadDeposits(accNo,uname,customer_id)

def switchToStatements(accNo,uname, customer_id):
	print("--- Entering switchToStatements() ---" + accNo)
	print("--- Entering switchToStatements() ---" + uname)
	print("--- Entering switchToStatements() ---" + str(customer_id))
	close()
	accountStatements.loadDefaultStatement(accNo,uname,customer_id)

def switchToFundTransfer(accNo,uname, customer_id):
	print("--- Entering switchToStatements() ---" + accNo)
	print("--- Entering switchToStatements() ---" + uname)
	print("--- Entering switchToStatements() ---" + str(customer_id))
	close()
	customerFundTransfer.loadFundTransfer(accNo,uname,customer_id)	


def switchToPayBills(accNo,uname, customer_id):
	print("--- Entering switchToPayBills() ---" + accNo)
	print("--- Entering switchToPayBills() ---" + uname)
	print("--- Entering switchToPayBills() ---" + str(customer_id))
	close()
	customerPayBills.loadPayBills(accNo,uname,customer_id)

def logout():
	print("--- Entering logout()")
	close()
	login.loadLogin()


#------To load dashboard--------
def loadDashboard(uname):
	print("--- Entering dashboard module for ---"+str(uname))


	#get a DBConnection
	con = db.getDBConnection()
	cur = con.cursor()

	#fetch the customer name generated
	cur.execute("select concat(fname,' ',lname) as customer_name, c.customer_id, a.acc_no from customer c,accounts a where c.username=%s and c.customer_id = a.customer_id",(uname,) )
	customer_records = cur.fetchall()

	customer_name = ""
	customer_id = 0
	acc_no = 0

	print("Total rows are:  ", len(customer_records))

	for row in customer_records:
		 customer_name = row[0]
		 customer_id = row[1]
		 acc_no = row[2]
	

	# #fetch the customer account numbers
	# cur.execute("select acc_no from accounts where customer_id=%s",(customer_id,))
	# account_number = cur.fetchone()[1]
	# print("--- Customer Account Number ---"+str(account_number))

	#Close the DB connection
	db.closeDBConnection(con)
	
	global customerDashboardWindow
	customerDashboardWindow = tk.Tk()
	customerDashboardWindow.title("Welcome to Hogsmeade Bank | Customer Dashboard")
	customerDashboardWindow.state("zoomed")
	customerDashboardWindow.columnconfigure(1, weight=6)

	#Logo
	logo = tk.Label(customerDashboardWindow,text="Hogsmeade Bank", font="Calibri 43")
	logo.grid(row=0,column=0,sticky="w", ipadx="2", columnspan=6)


	# Seperator object
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(customerDashboardWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=1,column=0,columnspan=6, sticky='ew')


	

	#Error and Message Row
	messageFrame = tk.Frame(customerDashboardWindow)
	messageText = Label(messageFrame, text="Hi "+ customer_name, font="Calibri 16")
	messageSpacer_0 = Label(messageFrame, text="  ", font="Calibri 16")
	messageSpacer_1 = Label(messageFrame, text="  ", font="Calibri 16")
	logoutButton = Button(messageFrame,text=" Logout ", font="Calibri 12",command=lambda: logout())
	messageFrame.grid(row=2,column=4,sticky="e")
	messageText.pack(side=LEFT)
	messageSpacer_0.pack(side=LEFT)
	logoutButton.pack(side=LEFT)
	messageSpacer_1.pack(side=LEFT)




	customer_account_numbers = [
    ""+str(acc_no),
	]



	#form fields
	accNumberSelected = StringVar()
	accNumberSelected.set(customer_account_numbers[0])



	#Customer Menu
	menuFrame = tk.Frame(customerDashboardWindow,width=350, height=100)
	menuSpacer_0 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_1 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_2 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_3 = Label(menuFrame, text="  ", font="Calibri 16")
	depositsButton = Button(menuFrame,text=" Deposits ", font="Calibri 12",command=lambda: switchTodeposit(accNumberSelected.get().strip(), uname, customer_id))
	reportsButton = Button(menuFrame,text=" View Statement ", font="Calibri 12",command=lambda: switchToStatements(accNumberSelected.get().strip(), uname, customer_id))
	fundTransferButton = Button(menuFrame,text=" Fund Transfer ", font="Calibri 12",command=lambda: switchToFundTransfer(accNumberSelected.get().strip(), uname, customer_id))
	billPayButton = Button(menuFrame,text=" Pay Bills ", font="Calibri 12",command=lambda: switchToPayBills(accNumberSelected.get().strip(), uname, customer_id))


	menuFrame.grid(row=3,column=0,sticky="w")
	menuSpacer_0.pack(side=LEFT)
	depositsButton.pack(side=LEFT)
	menuSpacer_1.pack(side=LEFT)
	reportsButton.pack(side=LEFT)
	menuSpacer_2.pack(side=LEFT)
	fundTransferButton.pack(side=LEFT)
	menuSpacer_3.pack(side=LEFT)
	billPayButton.pack(side=LEFT)

	#BlankRow
	blankRow_1 = Label(customerDashboardWindow,text=" ", font="Calibri 12")
	blankRow_1.grid(row=4,column=0,sticky="e")

	#Instruction
	instructionLabel = Label(customerDashboardWindow,text="   Select an account number and click on the action above ", font="Calibri 12")
	instructionLabel.grid(row=5,column=0,sticky="w")

	#BlankRow
	blankRow_2 = Label(customerDashboardWindow,text=" ", font="Calibri 12")
	blankRow_2.grid(row=6,column=0,sticky="e")



	

	
	#Account Number Selection
	accountNumberFrame = tk.Frame(customerDashboardWindow,width=300, height=30)
	accountNumberFrame.pack_propagate(0)
	accnumber_label = Label(accountNumberFrame, text="   Account Number * ", font="Calibri 16")
	#accountNumber_entry = Entry(accountNumberFrame, textvariable=accNumberSelected)
	drop = OptionMenu( accountNumberFrame , accNumberSelected , *customer_account_numbers )
	accountNumberFrame.grid(row=7,column=0,sticky="w")
	accnumber_label.pack(side=LEFT)
	#accountNumber_entry.pack(side=RIGHT)
	drop.pack(side=RIGHT)

	



		


	# Seperator object
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(customerDashboardWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=12,column=0,columnspan=6, sticky='ew', pady=10)











	customerDashboardWindow.mainloop()