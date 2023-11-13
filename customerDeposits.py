import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
import db
import util
import customerDashboard
import mysql
from datetime import datetime
import accountStatements
import customerPayBills
import login
import customerFundTransfer

customerDepositWindow = ""


def close():
	print("--- Entering bankAdminWindow close() ---")
	global customerDepositWindow
	customerDepositWindow.destroy()


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

def switchToStatements(accNo,uname, customer_id):
	print("--- Entering switchToStatements() ---" + accNo)
	print("--- Entering switchToStatements() ---" + uname)
	print("--- Entering switchToStatements() ---" + str(customer_id))
	close()
	accountStatements.loadDefaultStatement(accNo,uname,customer_id)

def switchToPayBills(accNo,uname, customer_id):
	print("--- Entering switchToPayBills() ---" + accNo)
	print("--- Entering switchToPayBills() ---" + uname)
	print("--- Entering switchToPayBills() ---" + str(customer_id))
	close()
	customerPayBills.loadPayBills(accNo,uname,customer_id)

#------To fundTransfer--------
def switchToFundTransfer(accNo,uname, customer_id):
	print("--- Entering switchToStatements() ---" + accNo)
	print("--- Entering switchToStatements() ---" + uname)
	print("--- Entering switchToStatements() ---" + str(customer_id))
	close()
	customerFundTransfer.loadFundTransfer(accNo,uname,customer_id)		


#------To deposit--------
def confirmDeposit(depositAmount,acc_no,uname,customer_id):	
	print("--- Entering confirmDeposit() ---" + depositAmount)
	print("--- Entering confirmDeposit module for ---"+str(uname))
	print("--- Entering confirmDeposit module for ---"+str(acc_no))
	print("--- Entering confirmDeposit module for ---"+str(customer_id))


	if util.isPositiveNumber(depositAmount):
		try:

			#get a DBConnection
			con = db.getDBConnection()
			cur = con.cursor()

			#get the latest amount for that user
			cur.execute("select balance from accounts where acc_no=%s",(acc_no,))
			balance = cur.fetchone()[0]

			balance = balance + int(depositAmount)
			print("--- Entering confirmDeposit new balance is ---"+str(balance))


			cur.execute("update accounts set balance=%s where acc_no = %s",(balance,acc_no))


			#Doing something to get the current date and time
			now = datetime.now()
			timeNow = now.strftime('%Y-%m-%d %H:%M:%S')

			cur.execute("insert into transaction (acc_no,trans_name,credit_debit,date,amt,balance) values(%s,%s,%s,%s,%s,%s)", (acc_no,'DEPOSIT','CREDIT',timeNow,depositAmount,balance))


			con.commit()

			successMessage = "Deposit Successful"
			messagebox.showinfo("Success" , successMessage)
			close()
			accountStatements.loadDefaultStatement(acc_no,uname,customer_id)
			

		except mysql.connector.Error as error:
			con.rollback()
			messagebox.showerror("Error" , "Transaction Failed")
			clearFields()	

		

		finally:
			#Close the DB connection
			db.closeDBConnection(con)

	else:
		messagebox.showerror("Error" , "Please enter a positive number")
				


#------To validate--------
def loadDeposits(acc_no,uname,customer_id):
	print("--- Entering loadDeposits module for ---"+str(uname))
	print("--- Entering loadDeposits module for ---"+str(acc_no))
	print("--- Entering loadDeposits module for ---"+str(customer_id))



	#get a DBConnection
	con = db.getDBConnection()
	cur = con.cursor()

	#fetch the customer id generated
	cur.execute("select concat(fname,' ',lname) as customer_name from customer where username=%s",(uname,))
	customer_name = cur.fetchone()[0]

	#Close the DB connection
	db.closeDBConnection(con)
	
	global customerDepositWindow
	customerDepositWindow = tk.Tk()
	customerDepositWindow.title("Welcome to Hogsmeade Bank | Customer Deposits")
	customerDepositWindow.state("zoomed")
	customerDepositWindow.columnconfigure(1, weight=6)

	#Logo
	logo = tk.Label(customerDepositWindow,text="Hogsmeade Bank", font="Calibri 43")
	logo.grid(row=0,column=0,sticky="w", ipadx="2", columnspan=6)


	# Seperator object	
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(customerDepositWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=1,column=0,columnspan=6, sticky='ew')


	

	#Error and Message Row
	messageFrame = tk.Frame(customerDepositWindow)
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
	menuFrame = tk.Frame(customerDepositWindow,width=350, height=100)
	menuSpacer_0 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_1 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_2 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_3 = Label(menuFrame, text="  ", font="Calibri 16")
	dashboardButton = Button(menuFrame,text=" Dashboard ", font="Calibri 12",command=lambda: switchToDashboard(uname))
	reportsButton = Button(menuFrame,text=" View Statement ", font="Calibri 12",command=lambda: switchToStatements(acc_no, uname, customer_id))
	fundTransferButton = Button(menuFrame,text=" Fund Transfer ", font="Calibri 12",command=lambda: switchToFundTransfer(acc_no, uname, customer_id))
	billPayButton = Button(menuFrame,text=" Pay Bills ", font="Calibri 12",command=lambda: switchToPayBills(acc_no, uname, customer_id))


	menuFrame.grid(row=3,column=0,sticky="w")
	menuSpacer_0.pack(side=LEFT)
	dashboardButton.pack(side=LEFT)
	menuSpacer_1.pack(side=LEFT)
	reportsButton.pack(side=LEFT)
	menuSpacer_2.pack(side=LEFT)
	fundTransferButton.pack(side=LEFT)
	menuSpacer_3.pack(side=LEFT)
	billPayButton.pack(side=LEFT)


	#BlankRow
	blankRow = Label(customerDepositWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=4,column=0,sticky="e",columnspan=6)


	#BlankRow
	blankRow = Label(customerDepositWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=5,column=0,sticky="e",columnspan=6)



	depAmountEntered = StringVar()

	#Deposit Row
	depFrame = tk.Frame(customerDepositWindow,width=350, height=100)
	depSpacer_0 = Label(depFrame, text="  ", font="Calibri 16")
	depSpacer_1 = Label(depFrame, text=" Enter an amount for the selected Account Number ( ", font="Calibri 16")
	depSpacer_2 = Label(depFrame, text= acc_no, font="Calibri 16")
	depSpacer_3 = Label(depFrame, text=" ) : ", font="Calibri 16")
	depSpacer_4 = Label(depFrame, text="  ", font="Calibri 16")
	depAmount_entry = Entry(depFrame, textvariable=depAmountEntered)
	depositButton = Button(depFrame,text="Deposit", font="Calibri 12", padx=10, pady=2,command=lambda: confirmDeposit(depAmountEntered.get().strip(),acc_no,uname,customer_id))

	depFrame.grid(row=6,column=0,sticky="w")
	depSpacer_0.pack(side=LEFT)
	depSpacer_1.pack(side=LEFT)
	depSpacer_2.pack(side=LEFT)
	depSpacer_3.pack(side=LEFT)
	depAmount_entry.pack(side=LEFT)
	depSpacer_4.pack(side=LEFT)
	depositButton.pack(side=LEFT)



	#BlankRow
	blankRow = Label(customerDepositWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=7,column=0,sticky="e",columnspan=6)


	

	



		


	# Seperator object
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(customerDepositWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=12,column=0,columnspan=6, sticky='ew', pady=10)











	customerDepositWindow.mainloop()