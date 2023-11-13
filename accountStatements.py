import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
import db
import util
import customerDashboard
import mysql
from datetime import datetime
import customerPayBills
import customerDeposits
import login
from tkcalendar import Calendar, DateEntry
import accountStatements
import customerFundTransfer


accountStatementWindow = ""


def close():
	print("--- Entering accountStatementWindow close() ---")
	global accountStatementWindow
	accountStatementWindow.destroy()


#------To clear the Fields--------
def clearFields():
	print("--- Entering clearFields() ---")
	
#----------------------------------

#--- navigate to dashboard -----
def switchToDashboard(uname):
	print("--- Entering switchToDashboard() ---" + uname)
	close()
	customerDashboard.loadDashboard(uname)

#------To fundTransfer--------
def switchToFundTransfer(accNo,uname, customer_id):
	print("--- Entering switchToStatements() ---" + accNo)
	print("--- Entering switchToStatements() ---" + uname)
	print("--- Entering switchToStatements() ---" + str(customer_id))
	close()
	customerFundTransfer.loadFundTransfer(accNo,uname,customer_id)		



#--- navigate to loadCustomStatement -----
def loadCustomStatement(acc_no,uname,customer_id,fromDate,toDate):
	print("--- Entering loadCustomStatement() ---" + uname)
	print("--- Entering loadCustomStatement() ---" + str(acc_no))
	print("--- Entering loadCustomStatement() ---" + str(customer_id))
	print("--- Entering loadCustomStatement() ---" + str(fromDate))
	print("--- Entering loadCustomStatement() ---" + str(toDate))
	if(toDate <= fromDate):
		messagebox.showerror("Error" , "To date should be greater than from date")
	else:	
		close()
		accountStatements.loadStatementByDate(acc_no,uname,customer_id,fromDate,toDate)
	


def loadStatementByDate(acc_no,uname,customer_id,fromDate,toDate):
	print("------------- Loading loadStatementByDate <ToDo> ----- ")
	print("--- Entering loadStatementByDate module for ---"+str(uname))
	print("--- Entering loadStatementByDate module for ---"+str(acc_no))
	print("--- Entering loadStatementByDate module for ---"+str(customer_id))
	print("--- Entering loadStatementByDate() ---" + str(fromDate))
	print("--- Entering loadStatementByDate() ---" + str(toDate))



	#get a DBConnection
	con = db.getDBConnection()
	cur = con.cursor()

	#fetch the customer id generated
	cur.execute("select concat(fname,' ',lname) as customer_name from customer where username=%s",(uname,))
	customer_name = cur.fetchone()[0]



	#load last 10 transactions for the user
	transactionSQL = "select * from transaction where acc_no='"+str(acc_no)+"' and (date>='"+str(fromDate)+"' and date<='"+str(toDate)+"') order by date DESC"
	print(transactionSQL)
	cur.execute("select * from transaction where acc_no=%s and (date >= %s AND date <= DATE_ADD(%s, INTERVAL 1 DAY)) order by date DESC",(acc_no,str(fromDate),str(toDate)))
	transactions = cur.fetchall()
	print("Number of Transactions : ---- " + str(len(transactions)))

	#latest balance for an user
	cur.execute("select balance from accounts where acc_no=%s",(acc_no,))
	latestBalance = [balancerow[0] for balancerow in cur.fetchall()]

	#Close the DB connection
	db.closeDBConnection(con)
	
	global accountStatementWindow
	accountStatementWindow = tk.Tk()
	accountStatementWindow.title("Welcome to Hogsmeade Bank| Customer Account Statements")
	accountStatementWindow.state("zoomed")
	accountStatementWindow.columnconfigure(1, weight=6)

	#Logo
	logo = tk.Label(accountStatementWindow,text="Hogsmeade Bank", font="Calibri 43")
	logo.grid(row=0,column=0,sticky="w", ipadx="2", columnspan=6)


	# Seperator object	
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(accountStatementWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=1,column=0,columnspan=6, sticky='ew')


	

	#Error and Message Row
	messageFrame = tk.Frame(accountStatementWindow)
	messageText = Label(messageFrame, text="Hi "+ customer_name, font="Calibri 16")
	messageSpacer_0 = Label(messageFrame, text="  ", font="Calibri 16")
	messageSpacer_1 = Label(messageFrame, text="  ", font="Calibri 16")
	logoutButton = Button(messageFrame,text=" Logout ", font="Calibri 12",command=lambda: logout())
	messageFrame.grid(row=2,column=4,sticky="e")
	messageText.pack(side=LEFT)
	messageSpacer_0.pack(side=LEFT)
	logoutButton.pack(side=LEFT)
	messageSpacer_1.pack(side=LEFT)



	#Customer Menu
	menuFrame = tk.Frame(accountStatementWindow,width=350, height=100)
	menuSpacer_0 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_1 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_2 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_3 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_4 = Label(menuFrame, text="  ", font="Calibri 16")
	dashboardButton = Button(menuFrame,text=" Dashboard ", font="Calibri 12",command=lambda: switchToDashboard(uname))
	depositsButton = Button(menuFrame,text=" Deposits ", font="Calibri 12",command=lambda: switchTodeposit(acc_no, uname, customer_id))
	fundTransferButton = Button(menuFrame,text=" Fund Transfer ", font="Calibri 12",command=lambda: switchToFundTransfer(acc_no, uname, customer_id))
	billPayButton = Button(menuFrame,text=" Pay Bills ", font="Calibri 12",command=lambda: switchToPayBills(acc_no, uname, customer_id))
	reportsButton = Button(menuFrame,text=" View Statement ", font="Calibri 12",command=lambda: switchToStatements(acc_no, uname, customer_id))



	menuFrame.grid(row=3,column=0,sticky="w")
	menuSpacer_0.pack(side=LEFT)
	dashboardButton.pack(side=LEFT)
	menuSpacer_1.pack(side=LEFT)
	depositsButton.pack(side=LEFT)
	menuSpacer_2.pack(side=LEFT)
	fundTransferButton.pack(side=LEFT)
	menuSpacer_3.pack(side=LEFT)
	billPayButton.pack(side=LEFT)
	menuSpacer_4.pack(side=LEFT)
	reportsButton.pack(side=LEFT)


	#BlankRow
	blankRow = Label(accountStatementWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=4,column=0,sticky="e",columnspan=6)


	fromDate = StringVar()
	toDate = StringVar()

	#Date Row
	dateFrame = tk.Frame(accountStatementWindow,width=350, height=100)
	dateSpacer_0 = Label(dateFrame, text="  ", font="Calibri 12")
	dateSpacer_1 = Label(dateFrame, text=" Enter a date range for the selected Account Number ( ", font="Calibri 12")
	dateSpacer_2 = Label(dateFrame, text= acc_no, font="Calibri 12")
	dateSpacer_3 = Label(dateFrame, text=" ) : From :", font="Calibri 12")
	dateSpacer_4 = Label(dateFrame, text="  To :", font="Calibri 12")
	dateSpacer_5 = Label(dateFrame, text="  ", font="Calibri 12")
	fromDate_cal = DateEntry(dateFrame, width= 16, background= "magenta3", foreground= "white",bd=2)
	toDate_cal = DateEntry(dateFrame, width= 16, background= "magenta3", foreground= "white",bd=2)
	#fromDate_entry = Entry(dateFrame, textvariable=fromDate)
	#toDate_entry = Entry(dateFrame, textvariable=toDate)
	viewStatementButton = Button(dateFrame,text="View Statement", font="Calibri 12", padx=10,command=lambda: loadCustomStatement(acc_no,uname,customer_id,fromDate_cal.get_date(),toDate_cal.get_date()))

	dateFrame.grid(row=5,column=0,sticky="w")
	dateSpacer_0.pack(side=LEFT)
	dateSpacer_1.pack(side=LEFT)
	dateSpacer_2.pack(side=LEFT)
	dateSpacer_3.pack(side=LEFT)
	#fromDate_entry.pack(side=LEFT)
	fromDate_cal.pack(side=LEFT)
	dateSpacer_4.pack(side=LEFT)
	#toDate_entry.pack(side=LEFT)
	toDate_cal.pack(side=LEFT)
	dateSpacer_5.pack(side=LEFT)
	viewStatementButton.pack(side=LEFT)


	#BlankRow
	blankRow = Label(accountStatementWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=6,column=0,sticky="e",columnspan=6)


	#Latest Balance latestBalance
	balanceFrame = tk.Frame(accountStatementWindow,width=350, height=20)
	balanceSpace_0 = Label(balanceFrame, text="  ", font="Calibri 12")
	balanceText = " Latest balance for the selected Account Number is "+ str(latestBalance)
	balanceText_1 = Label(balanceFrame,font="Calibri 12", bg="yellow", text=balanceText)
	balanceSpace_0.pack(side=LEFT)
	balanceText_1.pack(side=LEFT)
	balanceFrame.grid(row=7,column=0,sticky="w",ipadx=75)
	





	#Load Statements (Iterate over the transactions)
	# Add a Treeview widget
	s = ttk.Style()
	s.theme_use('clam')
	s.configure('Treeview.Heading', font="Calibri 14")
	tranSpacer_0 = Label(menuFrame, text="  ", font="Calibri 12")
	transactionFrame = tk.Frame(accountStatementWindow,width=350)
	tree = ttk.Treeview(transactionFrame, column=("Transaction Name", "Transaction Type", "Date","Amount"), show='headings', height=11)
	tree.column("# 1")
	tree.heading("# 1", text="Transaction Name")
	tree.column("# 2")
	tree.heading("# 2", text="Transaction Type")
	tree.column("# 3")
	tree.heading("# 3", text="Date")
	tree.column("# 4")
	tree.heading("# 4", text="Amount")
	transactionFrame.grid(row=8,column=0,sticky="w", ipadx=75, ipady=20)

	
	for row in transactions:
		tree.insert('', 'end', text="1", values=(row[2], row[3], row[4],row[5]))	

	tranSpacer_0.pack(side=LEFT)
	tree.pack()




	
	#BlankRow
	#blankRow = Label(accountStatementWindow,text=" ", font="Calibri 12")
	#blankRow.grid(row=9,column=0,sticky="e",columnspan=6)


	# Seperator object
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(accountStatementWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=9,column=0,columnspan=6, sticky='ew', pady=10)



	accountStatementWindow.mainloop()



#--- navigate to deposit -----
def switchTodeposit(accNo,uname, customer_id):
	print("--- Entering switchTodeposit() ---" + accNo)
	print("--- Entering switchTodeposit() ---" + uname)
	print("--- Entering switchTodeposit() ---" + str(customer_id))
	close()
	customerDeposits.loadDeposits(accNo,uname,customer_id)

def logout():
	print("--- Entering logout()")
	close()
	login.loadLogin()


def switchToPayBills(accNo,uname, customer_id):
	print("--- Entering switchToPayBills() ---" + accNo)
	print("--- Entering switchToPayBills() ---" + uname)
	print("--- Entering switchToPayBills() ---" + str(customer_id))
	close()
	customerPayBills.loadPayBills(accNo,uname,customer_id)


#------To viewstatement--------
def loadDefaultStatement(acc_no,uname,customer_id):
	print("--- Entering viewStatement module for ---"+str(uname))
	print("--- Entering viewStatement module for ---"+str(acc_no))
	print("--- Entering viewStatement module for ---"+str(customer_id))


	#get a DBConnection
	con = db.getDBConnection()
	cur = con.cursor()

	#fetch the customer id generated
	cur.execute("select concat(fname,' ',lname) as customer_name from customer where username=%s",(uname,))
	customer_name = cur.fetchone()[0]



	#load last 10 transactions for the user
	cur.execute("select * from transaction where acc_no=%s order by date DESC LIMIT 10",(acc_no,))
	transactions = cur.fetchall()
	print("Number of Transactions : ---- " + str(len(transactions)))

	#latest balance for an user
	cur.execute("select balance from accounts where acc_no=%s",(acc_no,))
	latestBalance = [balancerow[0] for balancerow in cur.fetchall()]

	#Close the DB connection
	db.closeDBConnection(con)
	
	global accountStatementWindow
	accountStatementWindow = tk.Tk()
	accountStatementWindow.title("Welcome to Hogsmeade Bank | Customer Account Statements")
	accountStatementWindow.state("zoomed")
	accountStatementWindow.columnconfigure(1, weight=6)

	#Logo
	logo = tk.Label(accountStatementWindow,text="Hogsmeade Bank", font="Calibri 43")
	logo.grid(row=0,column=0,sticky="w", ipadx="2", columnspan=6)


	# Seperator object	
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(accountStatementWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=1,column=0,columnspan=6, sticky='ew')


	

	#Error and Message Row
	messageFrame = tk.Frame(accountStatementWindow)
	messageText = Label(messageFrame, text="Hi "+ customer_name, font="Calibri 16")
	messageSpacer_0 = Label(messageFrame, text="  ", font="Calibri 16")
	messageSpacer_1 = Label(messageFrame, text="  ", font="Calibri 16")
	logoutButton = Button(messageFrame,text=" Logout ", font="Calibri 12",command=lambda: logout())
	messageFrame.grid(row=2,column=4,sticky="e")
	messageText.pack(side=LEFT)
	messageSpacer_0.pack(side=LEFT)
	logoutButton.pack(side=LEFT)
	messageSpacer_1.pack(side=LEFT)



	#Customer Menu
	menuFrame = tk.Frame(accountStatementWindow,width=350, height=100)
	menuSpacer_0 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_1 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_2 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_3 = Label(menuFrame, text="  ", font="Calibri 16")
	dashboardButton = Button(menuFrame,text=" Dashboard ", font="Calibri 12",command=lambda: switchToDashboard(uname))
	depositsButton = Button(menuFrame,text=" Deposits ", font="Calibri 12",command=lambda: switchTodeposit(acc_no, uname, customer_id))
	fundTransferButton = Button(menuFrame,text=" Fund Transfer ", font="Calibri 12",command=lambda: switchToFundTransfer(acc_no, uname, customer_id))
	billPayButton = Button(menuFrame,text=" Pay Bills ", font="Calibri 12",command=lambda: switchToPayBills(acc_no, uname, customer_id))


	menuFrame.grid(row=3,column=0,sticky="w")
	menuSpacer_0.pack(side=LEFT)
	dashboardButton.pack(side=LEFT)
	menuSpacer_1.pack(side=LEFT)
	depositsButton.pack(side=LEFT)
	menuSpacer_2.pack(side=LEFT)
	fundTransferButton.pack(side=LEFT)
	menuSpacer_3.pack(side=LEFT)
	billPayButton.pack(side=LEFT)


	#BlankRow
	blankRow = Label(accountStatementWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=4,column=0,sticky="e",columnspan=6)


	fromDate = StringVar()
	toDate = StringVar()

	#Date Row
	dateFrame = tk.Frame(accountStatementWindow,width=350, height=100)
	dateSpacer_0 = Label(dateFrame, text="  ", font="Calibri 12")
	dateSpacer_1 = Label(dateFrame, text=" Enter a date range for the selected Account Number ( ", font="Calibri 12")
	dateSpacer_2 = Label(dateFrame, text= acc_no, font="Calibri 12")
	dateSpacer_3 = Label(dateFrame, text=" ) : From :", font="Calibri 12")
	dateSpacer_4 = Label(dateFrame, text="  To :", font="Calibri 12")
	dateSpacer_5 = Label(dateFrame, text="  ", font="Calibri 12")
	fromDate_cal = DateEntry(dateFrame, width= 16, background= "magenta3", foreground= "white",bd=2)
	toDate_cal = DateEntry(dateFrame, width= 16, background= "magenta3", foreground= "white",bd=2)
	#fromDate_entry = Entry(dateFrame, textvariable=fromDate)
	#toDate_entry = Entry(dateFrame, textvariable=toDate)
	viewStatementButton = Button(dateFrame,text="View Statement", font="Calibri 12", padx=10,command=lambda: loadCustomStatement(acc_no,uname,customer_id,fromDate_cal.get_date(),toDate_cal.get_date()))

	dateFrame.grid(row=5,column=0,sticky="w")
	dateSpacer_0.pack(side=LEFT)
	dateSpacer_1.pack(side=LEFT)
	dateSpacer_2.pack(side=LEFT)
	dateSpacer_3.pack(side=LEFT)
	#fromDate_entry.pack(side=LEFT)
	fromDate_cal.pack(side=LEFT)
	dateSpacer_4.pack(side=LEFT)
	#toDate_entry.pack(side=LEFT)
	toDate_cal.pack(side=LEFT)
	dateSpacer_5.pack(side=LEFT)
	viewStatementButton.pack(side=LEFT)


	#BlankRow
	blankRow = Label(accountStatementWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=6,column=0,sticky="e",columnspan=6)


	#Latest Balance latestBalance
	balanceFrame = tk.Frame(accountStatementWindow,width=350, height=20)
	balanceSpace_0 = Label(balanceFrame, text="  ", font="Calibri 12")
	balanceText = " Latest balance for the selected Account Number is "+ str(latestBalance)
	balanceText_1 = Label(balanceFrame,font="Calibri 12", bg="yellow", text=balanceText)
	balanceSpace_0.pack(side=LEFT)
	balanceText_1.pack(side=LEFT)
	balanceFrame.grid(row=7,column=0,sticky="w",ipadx=75)
	





	#Load Statements (Iterate over the transactions)
	# Add a Treeview widget
	s = ttk.Style()
	s.theme_use('clam')
	s.configure('Treeview.Heading', font="Calibri 14")
	tranSpacer_0 = Label(menuFrame, text="  ", font="Calibri 12")
	transactionFrame = tk.Frame(accountStatementWindow,width=350)
	tree = ttk.Treeview(transactionFrame, column=("Transaction Name", "Transaction Type", "Date","Amount"), show='headings', height=11)
	tree.column("# 1")
	tree.heading("# 1", text="Transaction Name")
	tree.column("# 2")
	tree.heading("# 2", text="Transaction Type")
	tree.column("# 3")
	tree.heading("# 3", text="Date")
	tree.column("# 4")
	tree.heading("# 4", text="Amount")
	transactionFrame.grid(row=8,column=0,sticky="w", ipadx=75, ipady=20)

	
	for row in transactions:
		tree.insert('', 'end', text="1", values=(row[2], row[3], row[4],row[5]))	

	tranSpacer_0.pack(side=LEFT)
	tree.pack()




	
	#BlankRow
	#blankRow = Label(accountStatementWindow,text=" ", font="Calibri 12")
	#blankRow.grid(row=9,column=0,sticky="e",columnspan=6)


	# Seperator object
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(accountStatementWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=9,column=0,columnspan=6, sticky='ew', pady=10)



	accountStatementWindow.mainloop()