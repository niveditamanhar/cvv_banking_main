import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
import db
import signup
import util
import customerDashboard
import bankadmin


def close():
	indexWindow.destroy()	


#------To clear the Fields--------
def clearCredentials():
	print("--- Entering clearCredentials() ---")
	userNameEntered.set('')
	passEntered.set('')
	username_entry.focus()
#----------------------------------



#------To Login--------
def login():
	print("--- Entering Index login() ---")
	uname = userNameEntered.get().strip()
	pwd = passEntered.get().strip()
	if uname=="" or pwd.strip()=="":
		messagebox.showerror("Error","Enter User Name And Password",parent=indexWindow)
		clearCredentials();	
	else:
		pwd = util.encrypt(pwd)
		validate(uname, pwd)
#----------------------------------


#------To validate--------
def validate(uname, pwd):
	print("--- Entering validate() ---")
	#get a DBConnection
	con = db.getDBConnection()
	cur = con.cursor()

	
	cur.execute("select username from customer where username=%s && pwd=%s",(uname,pwd))
	row = cur.fetchone()

	if row==None:
		messagebox.showerror("Error" , "Invalid User Name And Password", parent = indexWindow)
		clearCredentials()

	else:
		#messagebox.showinfo("Success" , "Successfully Login, I will Redirect to your Login (To Do) " , parent = indexWindow)
		close()
		if uname=='admin':
			bankadmin.loadDashboard(uname)
		else:	
			customerDashboard.loadDashboard(uname)
		#customerDashboard.loadDashboard(uname)

	#Close the DB connection
	db.closeDBConnection(con)

	

#------To validate--------
def switchToSignUp():
	print("--- Entering signup function ---")
	close()
	signup.loadSignupModule()
	


#-------------------------------UI Code ----------------------------------
indexWindow = tk.Tk()
indexWindow.title("Welcome to Hogsmeade Bank | Index Screen")
#indexWindow.geometry('1024x768')
#indexWindow.attributes("-fullscreen", True)
indexWindow.state("zoomed")

# configure the grid
#indexWindow.columnconfigure(0, weight=1)
indexWindow.columnconfigure(1, weight=6)



#Logo
logo = tk.Label(indexWindow,text="Hogsmeade Bank", font="Calibri 43")
logo.grid(row=0,column=0,sticky="w", ipadx="2", columnspan=6)

# Seperator object
line_style = ttk.Style()
line_style.configure("Line.TSeparator", background="#FF0000")
separator = ttk.Separator(indexWindow, orient='horizontal', style="Line.TSeparator")
separator.grid(row=1,column=0,columnspan=6, sticky='ew')


#Error and Message Row
messageFrame = tk.Frame(indexWindow)
messageText = Label(messageFrame, text=" ", font="Calibri 16")
messageSpacer = Label(messageFrame, text="  ", font="Calibri 16")
messageFrame.grid(row=2,column=0,sticky="w")
messageText.pack(side=TOP);
messageSpacer.pack(side=TOP);


#username and password entered by user
userNameEntered = StringVar()
passEntered = StringVar()


userNameFrame = tk.Frame(indexWindow)
username_label = Label(userNameFrame, text=" Username * ", font="Calibri 16")
username_entry = Entry(userNameFrame, textvariable=userNameEntered)
username_entry.focus()
userNameFrame.grid(row=3,column=0,sticky="w")
username_label.pack(side=LEFT);
username_entry.pack(side=LEFT);


#Password and Submit Button Frame
passwordFrame = tk.Frame(indexWindow)
passwordLabel = Label(passwordFrame,text=" Password *  ", font="Calibri 16")
passwordEntry = Entry(passwordFrame, textvariable=passEntered, show='*')
textSpacer = Label(passwordFrame,text="   ")
loginButton = Button(passwordFrame,text="Login", font="Calibri 12", padx=10, pady=2,command = login)
clearButton = Button(passwordFrame,text="Clear", font="Calibri 12", padx=10,pady=2,command = clearCredentials)
passwordFrame.grid(row=4,column=0,sticky="w")
passwordLabel.pack(side=LEFT);
passwordEntry.pack(side=LEFT);
textSpacer.pack(side=LEFT);
clearButton.pack(side=RIGHT);
loginButton.pack(side=RIGHT);


#BlankRow
blankRow = Label(indexWindow,text=" ", font="Calibri 12")
blankRow.grid(row=5,column=0,sticky="e")


#Signup Frame, Lable and Button
signUpFrame = tk.Frame(indexWindow)
signUpLabel = Label(signUpFrame,text="New User?", font="Calibri 12")
signUpButton = Button(signUpFrame,text=" Sign Up ", font="Calibri 12", command = switchToSignUp)
signUpFrame.grid(row=6,column=0,sticky="w")
signUpLabel.pack(side=LEFT);
signUpButton.pack(side=LEFT);


#BlankRow
blankRow = Label(indexWindow,text=" ", font="Calibri 12")
blankRow.grid(row=7,column=0,sticky="e",columnspan=6)


# Seperator object
line_style = ttk.Style()
line_style.configure("Line.TSeparator", background="#FF0000")
separator = ttk.Separator(indexWindow, orient='horizontal', style="Line.TSeparator")
separator.grid(row=8,column=0,columnspan=6, sticky='ew')


indexWindow.mainloop()

