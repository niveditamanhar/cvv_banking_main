import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
from mysql import connector
import mysql
from mysql.connector.errors import Error
from datetime import datetime

import db
import util
import login


signUpWindow = ""


def close():
	print("--- Entering singup close() ---")
	global signUpWindow
	signUpWindow.destroy()


#------To clear the Fields--------
def clearFields(userNameEntered,passwordEntered,accountTypeEntered,fnameEntered,lnameEntered,phoneEntered,emailEntered,dobEntered,unameEntry):
	print("--- Entering clearFields() ---")
	userNameEntered.set('')
	passwordEntered.set('')
	accountTypeEntered.set('')
	fnameEntered.set('')
	lnameEntered.set('')
	phoneEntered.set('')
	emailEntered.set('')
	dobEntered.set('')
	unameEntry.focus()
#----------------------------------


#------To validate the Fields--------
def validateFields(uname,pwd,accType,fname,lname,phone,email,dob):
	print("---To do Validate Fields")


def switchToLogin():
	print("--- Entering signup function ---")
	close()
	login.loadLogin()
#------To signup--------
def signup(uname,pwd,accType,fname,lname,phone,email,dob):
	print("--- Entering signup() ---" + uname)
	pwd = util.encrypt(pwd)
	validateFields(uname,pwd,accType,fname,lname,phone,email,dob)
	try:
		#get a DBConnection
		con = db.getDBConnection()
		cur = con.cursor()
		con.autocommit = False #Setting this to false

		#validate with select query. cursor requires a tuble not string, thats why we have (,)
		cur.execute("insert into customer (fname,lname,phone,email,username,pwd,dob) values(%s,%s,%s,%s,%s,%s,%s)",(fname,lname,phone,email,uname,pwd,dob))
		#fetch the customer id generated
		cur.execute("select customer_id from customer where username=%s",(uname,))
		customer_id = cur.fetchone()[0]
		
		now = datetime.now()
		timeNow = now.strftime('%Y-%m-%d %H:%M:%S')

		cur.execute("insert into accounts (acc_type,customer_id,created_date,balance) values(%s,%s,%s,%s)",("SAVINGS",customer_id,timeNow,"0.0"))
		con.commit()
		
		#fetch the account Id generated
		cur.execute("select acc_no from accounts where customer_id=%s",(customer_id,))
		new_account_number = cur.fetchone()[0]
		successMessage = "SignUp Successfull, Your Customer Id is " + str(customer_id) + " and account number is " + str(new_account_number) +". We will Redirect to your Login."
		messagebox.showinfo("Success" , successMessage)
		close()
		login.loadLogin()

	except mysql.connector.Error as error:
		con.rollback()
		messagebox.showerror("Error" , "Customer Id not generated")
		clearFields()

	finally:
		db.closeDBConnection(con)








#----------------------------------

#------To validate--------
def loadSignupModule():
	print("--- Entering signup module ---")
	
	global signUpWindow
	signUpWindow = tk.Tk()
	signUpWindow.title("Welcome to Hogsmeade Bank | Sign Up")
	signUpWindow.state("zoomed")
	signUpWindow.columnconfigure(1, weight=6)

	#Logo
	logo = tk.Label(signUpWindow,text="Hogsmeade Bank", font="Calibri 43")
	logo.grid(row=0,column=0,sticky="w", ipadx="2", columnspan=6)


	# Seperator object
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(signUpWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=1,column=0,columnspan=6, sticky='ew')


	#form fields
	userNameEntered = StringVar()
	passwordEntered = StringVar()
	accountTypeEntered = StringVar()
	fnameEntered = StringVar()
	lnameEntered = StringVar()
	phoneEntered = StringVar()
	emailEntered = StringVar()
	dobEntered = StringVar()

	#Error and Message Row
	messageFrame = tk.Frame(signUpWindow)
	messageText = Label(messageFrame, text="Please enter your details", font="Calibri 16")
	messageSpacer = Label(messageFrame, text="  ", font="Calibri 16")
	messageFrame.grid(row=2,column=0,sticky="w")
	messageText.pack(side=TOP)
	messageSpacer.pack(side=TOP)

	#username  Frame
	userNameFrame = tk.Frame(signUpWindow,width=300, height=30)
	userNameFrame.pack_propagate(0)
	username_label = Label(userNameFrame, text=" Username * ", font="Calibri 16")
	username_entry = Entry(userNameFrame, textvariable=userNameEntered)
	username_entry.focus()
	userNameFrame.grid(row=3,column=0,sticky="w")
	username_label.pack(side=LEFT)
	username_entry.pack(side=RIGHT)


	#password Frame
	passwordFrame = tk.Frame(signUpWindow,width=300, height=30)
	passwordFrame.pack_propagate(0)
	password_label = Label(passwordFrame, text=" Password * ", font="Calibri 16")
	password_entry = Entry(passwordFrame, textvariable=passwordEntered, show='*')
	passwordFrame.grid(row=4,column=0,sticky="w")
	password_label.pack(side=LEFT)
	password_entry.pack(side=RIGHT)

	#accountType  Frame
	accountTypeFrame = tk.Frame(signUpWindow,width=300, height=30)
	accountTypeFrame.pack_propagate(0)
	accountType_label = Label(accountTypeFrame, text=" AccountType * ", font="Calibri 16")
	accountType_entry = Entry(accountTypeFrame, textvariable=accountTypeEntered)
	accountTypeFrame.grid(row=5,column=0,sticky="w")
	accountType_label.pack(side=LEFT)
	accountType_entry.pack(side=RIGHT)

	#Fname  Frame
	fnameFrame = tk.Frame(signUpWindow,width=300, height=30)
	fnameFrame.pack_propagate(0)
	fname_label = Label(fnameFrame, text=" First Name * ", font="Calibri 16")
	fname_entry = Entry(fnameFrame, textvariable=fnameEntered)
	fnameFrame.grid(row=6,column=0,sticky="w")
	fname_label.pack(side=LEFT)
	fname_entry.pack(side=RIGHT)


	#lname  Frame
	lnameFrame = tk.Frame(signUpWindow,width=300, height=30)
	lnameFrame.pack_propagate(0)
	lname_label = Label(lnameFrame, text=" Last Name * ", font="Calibri 16")
	lname_entry = Entry(lnameFrame, textvariable=lnameEntered)
	lnameFrame.grid(row=7,column=0,sticky="w")
	lname_label.pack(side=LEFT)
	lname_entry.pack(side=RIGHT)


	#phone  Frame
	phoneFrame = tk.Frame(signUpWindow,width=300, height=30)
	phoneFrame.pack_propagate(0)
	phone_label = Label(phoneFrame, text=" Phone * ", font="Calibri 16")
	phone_entry = Entry(phoneFrame, textvariable=phoneEntered)
	phoneFrame.grid(row=8,column=0,sticky="w")
	phone_label.pack(side=LEFT)
	phone_entry.pack(side=RIGHT)


	#email  Frame
	emailFrame = tk.Frame(signUpWindow,width=300, height=30)
	emailFrame.pack_propagate(0)
	email_label = Label(emailFrame, text=" Email * ", font="Calibri 16")
	email_entry = Entry(emailFrame, textvariable=emailEntered)
	emailFrame.grid(row=9,column=0,sticky="w")
	email_label.pack(side=LEFT)
	email_entry.pack(side=RIGHT)


	#dob  Frame
	dobFrame = tk.Frame(signUpWindow,width=300, height=30)
	dobFrame.pack_propagate(0)
	dob_label = Label(dobFrame, text=" DOB * ", font="Calibri 16")
	dob_entry = Entry(dobFrame, textvariable=dobEntered)
	dobFrame.grid(row=10,column=0,sticky="w")
	dob_label.pack(side=LEFT)
	dob_entry.pack(side=RIGHT)

	#control  Frame
	controlFrame = tk.Frame(signUpWindow,width=300, height=30)
	controlFrame.pack_propagate(0)
	submitButton = Button(controlFrame,text="Submit", font="Calibri 12", padx=10, pady=2,command=lambda: signup(userNameEntered.get().strip(),passwordEntered.get().strip(),accountTypeEntered.get().strip(),fnameEntered.get().strip(),lnameEntered.get().strip(),phoneEntered.get().strip(),emailEntered.get().strip(),dobEntered.get().strip()))
	clearButton = Button(controlFrame,text="Clear", font="Calibri 12", padx=10,pady=2,command=lambda: clearFields(userNameEntered,passwordEntered,accountTypeEntered,fnameEntered,lnameEntered,phoneEntered,emailEntered,dobEntered,username_entry))
	controlFrame.grid(row=11,column=0,sticky="e")
	submitButton.pack(side=RIGHT)
	clearButton.pack(side=RIGHT)


	#BlankRow
	blankRow = Label(signUpWindow,text=" ", font="Calibri 12")
	blankRow.grid(row=12,column=0,sticky="e")


	#Signup Frame, Lable and Button
	loginFrame = tk.Frame(signUpWindow)
	loginButton = Button(loginFrame,text=" Back to Login ", font="Calibri 12", command = switchToLogin)
	loginFrame.grid(row=13,column=0,sticky="w")
	loginButton.pack(side=LEFT);


	# Seperator object
	line_style = ttk.Style()
	line_style.configure("Line.TSeparator", background="#FF0000")
	separator = ttk.Separator(signUpWindow, orient='horizontal', style="Line.TSeparator")
	separator.grid(row=12,column=0,columnspan=6, sticky='ew', pady=10)






	signUpWindow.mainloop()
