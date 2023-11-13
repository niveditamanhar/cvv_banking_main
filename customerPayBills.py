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

customerPayBillsWindow = ""


def close():
	print("--- Entering customerPayBillsWindow close() ---")
	global customerPayBillsWindow
	customerPayBillsWindow.destroy()


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
	customerDashboard.loadDashboard(uname)

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


#------To fundTransfer--------
def switchToFundTransfer(accNo,uname, customer_id):
	print("--- Entering switchToStatements() ---" + accNo)
	print("--- Entering switchToStatements() ---" + uname)
	print("--- Entering switchToStatements() ---" + str(customer_id))
	close()
	customerFundTransfer.loadFundTransfer(accNo,uname,customer_id)	


#------To submitBillPay--------
def submitBillPay(billType, billNumber, billAmount,acc_no,uname,customer_id):
	print("--- submitBillPay billType ---" + str(billType))
	print("--- submitBillPay billNumber ---" + str(billNumber))
	print("--- submitBillPay billAmount ---" + str(billAmount))
	print("--- submitBillPay acc_no ---" + str(acc_no))
	print("--- submitBillPay uname ---" + str(uname))
	print("--- submitBillPay customer_id ---" + str(customer_id))

	billPayTransactionText = "BILLPAY | " + str(billType) +" | " + str(billNumber)

	try:

		#get a DBConnection
		con = db.getDBConnection()
		cur = con.cursor()

		#get the latest amount for that user
		cur.execute("select balance from accounts where acc_no=%s",(acc_no,))
		balance = cur.fetchone()[0]

		#check if sufficient balance available.
		assert(float(balance) > float(billAmount)),"Insufficient Balance"
		

		balance = balance - int(billAmount)
		
		print("--- Entering confirmDeposit new balance is ---"+str(balance))


		cur.execute("update accounts set balance=%s where acc_no = %s",(balance,acc_no))

		#making to -ve
		billAmount = (-1) * float(billAmount)
		print("--- Negative Bill Amount :: "+str(billAmount))


		#Doing something to get the current date and time
		now = datetime.now()
		timeNow = now.strftime('%Y-%m-%d %H:%M:%S')

		cur.execute("insert into transaction (acc_no,trans_name,credit_debit,date,amt,balance) values(%s,%s,%s,%s,%s,%s)", (acc_no,billPayTransactionText,'DEBIT',timeNow,billAmount,balance))


		con.commit()

		successMessage = "Bill Pay Successful"
		messagebox.showinfo("Success" , successMessage)
		close()
		accountStatements.loadDefaultStatement(acc_no,uname, customer_id)
		

	except mysql.connector.Error as error:
		con.rollback()
		messagebox.showerror("Error" , "Transaction Failed")
		clearFields()	

	except Exception as e:
		con.rollback()
		messagebox.showerror("Error" , "Transaction Failed, Insufficient Balance")
		clearFields()

	finally:
		#Close the DB connection
		db.closeDBConnection(con)






#------To validate--------
def loadPayBills(acc_no,uname,customer_id):
	print("--- Entering loadPayBills module for ---"+str(uname))
	print("--- Entering loadPayBills module for ---"+str(acc_no))
	print("--- Entering loadPayBills module for ---"+str(customer_id))



	#get a DBConnection
	con = db.getDBConnection()
	cur = con.cursor()

	#fetch the customer id generated
	cur.execute("select concat(fname,' ',lname) as customer_name from customer where username=%s",(uname,))
	customer_name = cur.fetchone()[0]


	#latest balance for an user
	cur.execute("select balance from accounts where acc_no=%s",(acc_no,))
	latestBalance = [balancerow[0] for balancerow in cur.fetchall()]

	#Close the DB connection
	db.closeDBConnection(con)
	
	global customerPayBillsWindow
	customerPayBillsWindow = tk.Tk()
	customerPayBillsWindow.title("Welcome to Hogsmeade Bank | Customer Pay Bills")
	customerPayBillsWindow.state("zoomed")
	customerPayBillsWindow.columnconfigure(1, weight=6)

	#Logo
	logo = tk.Label(customerPayBillsWindow,text="Hogsmeade Bank", font="Calibri 43")
	logo.grid(row=0,column=0,sticky="w", ipadx="2", columnspan=6)


	# Seperator object	
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(customerPayBillsWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=1,column=0,columnspan=6, sticky='ew')


	

	#Error and Message Row
	messageFrame = tk.Frame(customerPayBillsWindow)
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
	menuFrame = tk.Frame(customerPayBillsWindow,width=350, height=100)
	menuSpacer_0 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_1 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_2 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_3 = Label(menuFrame, text="  ", font="Calibri 16")
	dashboardButton = Button(menuFrame,text=" Dashboard ", font="Calibri 12",command=lambda: switchToDashboard(uname))
	depositsButton = Button(menuFrame,text=" Deposits ", font="Calibri 12",command=lambda: switchTodeposit(acc_no, uname, customer_id))
	reportsButton = Button(menuFrame,text=" View Statement ", font="Calibri 12",command=lambda: switchToStatements(acc_no, uname, customer_id))
	fundTransferButton = Button(menuFrame,text=" Fund Transfer ", font="Calibri 12",command=lambda: switchToFundTransfer(acc_no, uname, customer_id))



	menuFrame.grid(row=3,column=0,sticky="w")
	menuSpacer_0.pack(side=LEFT)
	dashboardButton.pack(side=LEFT)
	menuSpacer_1.pack(side=LEFT)
	depositsButton.pack(side=LEFT)
	menuSpacer_2.pack(side=LEFT)
	reportsButton.pack(side=LEFT)
	menuSpacer_3.pack(side=LEFT)
	fundTransferButton.pack(side=LEFT)
	


	#BlankRow
	blankRow = Label(customerPayBillsWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=4,column=0,sticky="e",columnspan=6)


	#BlankRow
	blankRow = Label(customerPayBillsWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=5,column=0,sticky="e",columnspan=6)



	#depAmountEntered = StringVar()

	#Selected Account Number Display Row
	balanceText = StringVar()
	balanceText.set("Selected Account Number is "+str(acc_no)+" with latest balance : "+str(latestBalance))
	selectedAccountDisplayFrame = tk.Frame(customerPayBillsWindow,width=350, height=100)
	spacer_0 = Label(selectedAccountDisplayFrame, text="  ", font="Calibri 12")
	#spacer_1 = Label(selectedAccountDisplayFrame, text=" Selected Account Number is ", font="Calibri 12")
	spacer_2 = Label(selectedAccountDisplayFrame, textvariable=balanceText, font="Calibri 12",bg="yellow")
	spacer_3 = Label(selectedAccountDisplayFrame, text="  ", font="Calibri 12")
	#depAmount_entry = Entry(depFrame, textvariable=depAmountEntered)
	#payBillButton = Button(depFrame,text="Deposit", font="Calibri 12", padx=10, pady=2,command=lambda: confirmDeposit(depAmountEntered.get().strip(),acc_no,uname,customer_id))

	selectedAccountDisplayFrame.grid(row=6,column=0,sticky="w")
	spacer_0.pack(side=LEFT)
	#spacer_1.pack(side=LEFT)
	spacer_2.pack(side=LEFT)
	spacer_3.pack(side=LEFT)
	#depAmount_entry.pack(side=LEFT)
	#depSpacer_4.pack(side=LEFT)
	#payBillButton.pack(side=LEFT)




	customer_billpay_types = [
    "Telephone", "Electric Charges", "Credit Card", "DTH", "Broadband", "Cooking Gas", 
	]

	#form fields
	billPayTypeSelected = StringVar()
	billPayNumberEntered = StringVar()
	billPayAmountEntered = StringVar()
	billPayTypeSelected.set(customer_billpay_types[0])


	#Billpay options  Frame
	billPayOptionsFrame = tk.Frame(customerPayBillsWindow,width=300, height=30)
	billPayOptionsFrame.pack_propagate(0)
	billPayOptions_label = Label(billPayOptionsFrame, text=" Bill Type *  : ", font="Calibri 12")
	billPayTypeDrop = OptionMenu( billPayOptionsFrame, billPayTypeSelected , *customer_billpay_types )
	billPayOptionsFrame.grid(row=7,column=0,sticky="w")
	billPayOptions_label.pack(side=LEFT)
	billPayTypeDrop.pack(side=LEFT)


	#Billpay Number  Frame
	billPayNumberFrame = tk.Frame(customerPayBillsWindow,width=300, height=30)
	billPayNumberFrame.pack_propagate(0)
	billPayNumber_label = Label(billPayNumberFrame, text=" Number * : ", font="Calibri 12")
	billPayNumber_entry = Entry(billPayNumberFrame, textvariable=billPayNumberEntered)
	billPayNumberFrame.grid(row=8,column=0,sticky="w")
	billPayNumber_label.pack(side=LEFT)
	billPayNumber_entry.pack(side=LEFT)


	#Billpay Amount  Frame
	billPayAmountFrame = tk.Frame(customerPayBillsWindow,width=300, height=30)
	billPayAmountFrame.pack_propagate(0)
	billPayAmountFrame_label = Label(billPayAmountFrame, text=" Amount * : ", font="Calibri 12")
	billPayAmountFrame_entry = Entry(billPayAmountFrame, textvariable=billPayAmountEntered)
	billPaySubmitButton = Button(billPayAmountFrame,text=" Pay ", font="Calibri 12", command=lambda: submitBillPay(billPayTypeSelected.get(),billPayNumberEntered.get(),billPayAmountEntered.get(),acc_no,uname,customer_id))
	spacer_4 = Label(billPayAmountFrame, text="    ", font="Calibri 12")
	billPayAmountFrame.grid(row=9,column=0,sticky="w")
	billPayAmountFrame_label.pack(side=LEFT)
	billPayAmountFrame_entry.pack(side=LEFT)
	spacer_4.pack(side=LEFT)
	billPaySubmitButton.pack(side=LEFT)






	#BlankRow
	blankRow = Label(customerPayBillsWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=11,column=0,sticky="e",columnspan=6)


	

	



		


	# Seperator object
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(customerPayBillsWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=12,column=0,columnspan=6, sticky='ew', pady=10)











	customerPayBillsWindow.mainloop()