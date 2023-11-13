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
import customerDeposits

customerFundTransfer = ""


def close():
	print("--- Entering customerFundTransferWindow close() ---")
	global customerFundTransferWindow
	customerFundTransferWindow.destroy()


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

#--- navigate to deposit -----
def switchTodeposit(accNo,uname, customer_id):
	print("--- Entering switchTodeposit() ---" + accNo)
	print("--- Entering switchTodeposit() ---" + uname)
	print("--- Entering switchTodeposit() ---" + str(customer_id))
	close()
	customerDeposits.loadDeposits(accNo,uname,customer_id)	


#------To deposit--------
def confirmFundTransfer(depositAmount,source_acc_no,dest_acc_no,uname,source_customer_id,customer_balance):	
	
	print("--- Entering confirmFundTransfer() customer_balance : " + str(customer_balance))
	print("--- Entering confirmFundTransfer() depositAmount : " + depositAmount)
	print("--- Entering confirmFundTransfer uname : "+str(uname))
	print("--- Entering confirmFundTransfer source_acc_no : "+str(source_acc_no))
	print("--- Entering confirmFundTransfer dest_acc_no : "+str(dest_acc_no))
	print("--- Entering confirmFundTransfer Customer_id : "+str(source_customer_id))


	#Validate the types of the inputs
	try: 
		#get a DBConnection
		con = db.getDBConnection()
		cur = con.cursor()

		if util.isPositiveNumber(depositAmount) and util.isPositiveNumber(source_acc_no) and util.isPositiveNumber(dest_acc_no) :
			print("--- Entering confirmFundTransfer Customer_id - All conditions passed")

			#check if sufficient balance available in source account?
			if(int(source_acc_no) == int(dest_acc_no)):
				messagebox.showerror("Error" , "Source and Destination Account Numbers are same")

			else:	
				#check if sufficient balance available in source account?
				if(float(customer_balance) < float(depositAmount)):
					messagebox.showerror("Error" , "No sufficient balance in your account to make this transfer")

				else:	
			
					destination_account_number = 0
					destination_account_balance = 0.0	
					#Check if the destination account number is valid
					cur.execute("select a.acc_no,a.balance from accounts a,customer c where c.customer_id=a.customer_id and a.acc_no=%s and c.username!='admin'",(dest_acc_no,))
					records = cur.fetchall()

					#print("--- Length of records : " + str(len(records))

					for rows in records:
						destination_account_balance = float(rows[1])
						print("--- Entering confirmFundTransfer destination_account_balance : " + str(destination_account_balance))

					if len(records)==1:
						#Do the actual fund transfer
						updated_destination_account_balance = float(destination_account_balance) + float(depositAmount)
						updated_source_account_balance = float(customer_balance) - float(depositAmount)
						print("---- updated_destination_account_balance ---" + str(updated_destination_account_balance))
						print("---- updated_source_account_balance ---" + str(updated_source_account_balance))
						cur.execute("update accounts set balance=%s where acc_no = %s",(updated_destination_account_balance,dest_acc_no))
						cur.execute("update accounts set balance=%s where acc_no = %s",(updated_source_account_balance,source_acc_no))
						#Doing something to get the current date and time
						now = datetime.now()
						timeNow = now.strftime('%Y-%m-%d %H:%M:%S')
						negativeDepositAmount = (-1) * float(depositAmount)

						cur.execute("insert into transaction (acc_no,trans_name,credit_debit,date,amt,balance) values(%s,%s,%s,%s,%s,%s)", (source_acc_no,'TRANSFER','DEBIT',timeNow,negativeDepositAmount,updated_source_account_balance))
						cur.execute("insert into transaction (acc_no,trans_name,credit_debit,date,amt,balance) values(%s,%s,%s,%s,%s,%s)", (dest_acc_no,'TRANSFER','CREDIT',timeNow,depositAmount,updated_destination_account_balance))

						con.commit()
						messagebox.showinfo("Success" , "Transfer Successful")
						close()
						print("--- To enter loadCustomStatement() ---" + uname)
						print("--- To enter loadCustomStatement() ---" + str(source_acc_no))
						print("--- To enter loadCustomStatement() ---" + str(source_customer_id))
						accountStatements.loadDefaultStatement(source_acc_no,uname,source_customer_id)
					else:
						messagebox.showerror("Error" , "Destination Account Number Invalid")	

		else:
			print("--- Entering confirmFundTransfer Customer_id -  Conditions failed")
			messagebox.showerror("Error" , "Please enter valid data")
	except:
		messagebox.showerror("Error" , "Please enter valid data")
	finally:
		#print("--- Entering confirmFundTransfer Customer_id -  All inputs are valid")
		#Close the DB connection
		db.closeDBConnection(con)
				


	"""	
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
			accountStatements.loadDefaultStatement(acc_no,uname, customer_id)
			

		except mysql.connector.Error as error:
			con.rollback()
			messagebox.showerror("Error" , "Transaction Failed")
			clearFields()	

		

		finally:
			#Close the DB connection
			db.closeDBConnection(con)

	else:
		messagebox.showerror("Error" , "Please enter a positive number")
				
"""

#------To validate--------
def loadFundTransfer(source_acc_no,uname,customer_id):
	print("--- Entering loadDeposits module for ---"+str(uname))
	print("--- Entering loadDeposits module for ---"+str(source_acc_no))
	print("--- Entering loadDeposits module for ---"+str(customer_id))







	#get a DBConnection
	con = db.getDBConnection()
	cur = con.cursor()

	#fetch the customer id generated
	cur.execute("select concat(fname,' ',lname) as customer_name from customer where username=%s",(uname,))
	customer_name = cur.fetchone()[0]

	#fetch the latest balance for the source account number
	cur.execute("select balance from accounts where acc_no=%s",(source_acc_no,))
	customer_balance = cur.fetchone()[0]


	#Fetch all accounts other than the selected account
	#cur.execute("select concat(c.fname,' ',c.lname) as customer_name,a.acc_no from customer c, accounts a where c.customer_id=a.customer_id and a.acc_no!=%s and c.username!='admin'",(source_acc_no,))
	#beneficiary_accounts = cur.fetchall()

	#print("Total beneficiary rows are:  ", len(beneficiary_accounts))

	#beneficiary_accounts_and_name =["Select Beneficiary Account Number"]

	#for row in beneficiary_accounts:
	#	account_and_name=row[0]+" | "+ str(row[1])
	#	print(account_and_name)
	#	beneficiary_accounts_and_name.append(account_and_name)



	#Close the DB connection
	db.closeDBConnection(con)
	
	global customerFundTransferWindow
	customerFundTransferWindow = tk.Tk()
	customerFundTransferWindow.title("Welcome to Hogsmeade Bank | Customer Fund Transfer")
	customerFundTransferWindow.state("zoomed")
	customerFundTransferWindow.columnconfigure(1, weight=6)

	#Logo
	logo = tk.Label(customerFundTransferWindow,text="Hogsmeade Bank", font="Calibri 43")
	logo.grid(row=0,column=0,sticky="w", ipadx="2", columnspan=6)


	# Seperator object	
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(customerFundTransferWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=1,column=0,columnspan=6, sticky='ew')


	

	#Error and Message Row
	messageFrame = tk.Frame(customerFundTransferWindow)
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
	menuFrame = tk.Frame(customerFundTransferWindow,width=350, height=100)
	menuSpacer_0 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_1 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_2 = Label(menuFrame, text="  ", font="Calibri 16")
	menuSpacer_3 = Label(menuFrame, text="  ", font="Calibri 16")
	dashboardButton = Button(menuFrame,text=" Dashboard ", font="Calibri 12",command=lambda: switchToDashboard(uname))
	reportsButton = Button(menuFrame,text=" View Statement ", font="Calibri 12",command=lambda: switchToStatements(source_acc_no, uname, customer_id))
	#fundTransferButton = Button(menuFrame,text=" Fund Transfer ", font="Calibri 12")
	billPayButton = Button(menuFrame,text=" Pay Bills ", font="Calibri 12",command=lambda: switchToPayBills(source_acc_no, uname, customer_id))
	depositsButton = Button(menuFrame,text=" Deposits ", font="Calibri 12",command=lambda: switchTodeposit(source_acc_no, uname, customer_id))


	menuFrame.grid(row=3,column=0,sticky="w")
	menuSpacer_0.pack(side=LEFT)
	dashboardButton.pack(side=LEFT)
	menuSpacer_1.pack(side=LEFT)
	reportsButton.pack(side=LEFT)
	menuSpacer_2.pack(side=LEFT)
	depositsButton.pack(side=LEFT)
	menuSpacer_3.pack(side=LEFT)
	billPayButton.pack(side=LEFT)


	#BlankRow
	blankRow = Label(customerFundTransferWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=4,column=0,sticky="e",columnspan=6)


	#BlankRow
	blankRow = Label(customerFundTransferWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=5,column=0,sticky="e",columnspan=6)



	destAmountEntered = StringVar()
	destAccountEntered = StringVar()

	#Latest Balance Frame
	balanceFrame = tk.Frame(customerFundTransferWindow,width=350, height=100)
	balSpacer_0 = Label(balanceFrame, text="  ", font="Calibri 16")
	balSpacer_1 = Label(balanceFrame, text=" Latest balance of the selected Account Number (", font="Calibri 16")
	balSpacer_2 = Label(balanceFrame, text= source_acc_no, font="Calibri 16")
	balSpacer_3 = Label(balanceFrame, text="): ", font="Calibri 16")
	balSpacer_4 = Label(balanceFrame, text= customer_balance, font="Calibri 16")
	balanceFrame.grid(row=6,column=0,sticky="w")
	balSpacer_0.pack(side=LEFT)
	balSpacer_1.pack(side=LEFT)
	balSpacer_2.pack(side=LEFT)
	balSpacer_3.pack(side=LEFT)
	balSpacer_4.pack(side=LEFT)


	#Destination Acccount Selection Frame
	destAccountFrame = tk.Frame(customerFundTransferWindow,width=350, height=100)
	destSpacer_0 = Label(destAccountFrame, text="  ", font="Calibri 16")
	destSpacer_1 = Label(destAccountFrame, text=" Please Enter a Destination Account :  ", font="Calibri 16")
	destAccountEntry = Entry(destAccountFrame, textvariable=destAccountEntered)
	destAccountFrame.grid(row=7,column=0,sticky="w")
	destSpacer_0.pack(side=LEFT)
	destSpacer_1.pack(side=LEFT)
	destAccountEntry.pack(side=LEFT)
	






	#form fields
	#beneficiaryAccNumberSelected = StringVar()

	#beneficiaryAccNumberSelected.set(beneficiary_accounts_and_name[0])






	
	#Amount Frame
	destAmountFrame = tk.Frame(customerFundTransferWindow,width=350, height=100)
	destAmountSpacer_0 = Label(destAmountFrame, text="  ", font="Calibri 16")
	destAmountSpacer_1 = Label(destAmountFrame, text=" Amount : ", font="Calibri 16")
	destAmountSpacer_2 = Label(destAmountFrame, text="  ", font="Calibri 16")
	destAmountEntry = Entry(destAmountFrame, textvariable=destAmountEntered)

	#drop = OptionMenu( destAmountFrame , beneficiaryAccNumberSelected , *beneficiary_accounts_and_name)
	#destAccountEntry = Entry(destAmountFrame, textvariable=destAccountEntered)
	transferButton = Button(destAmountFrame,text="Click to Transfer", font="Calibri 12", padx=10, pady=2,command=lambda: confirmFundTransfer(destAmountEntered.get().strip(),source_acc_no,destAccountEntered.get().strip(),uname,customer_id,customer_balance))
	destAmountFrame.grid(row=8,column=0,sticky="w")
	#drop.pack(side=LEFT)
	destAmountSpacer_0.pack(side=LEFT)
	#destAccountEntry.pack(side=LEFT)
	destAmountSpacer_1.pack(side=LEFT),
	destAmountEntry.pack(side=LEFT)
	destAmountSpacer_2.pack(side=LEFT)
	transferButton.pack(side=LEFT)



	#BlankRow
	blankRow = Label(customerFundTransferWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=8,column=0,sticky="e",columnspan=6)


	

	



		


	# Seperator object
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(customerFundTransferWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=12,column=0,columnspan=6, sticky='ew', pady=10)











	customerFundTransferWindow.mainloop()