import mysql.connector as sq

#------To DB connection--------
def getDBConnection():
	print("--- getDBConnection() ---")
	con=sq.connect(host='localhost',user='root',password='qwerty',database='bank')
	return con

#------close DB connection --------
def closeDBConnection(con):
	print("--- closeDBConnection() ---")
	if con.is_connected():
		con.cursor().close()
		con.close()