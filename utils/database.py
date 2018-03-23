import sqlite3, json

def createTable():
	f="data/songs.db"
	db=sqlite3.connect(f)
	c=db.cursor()
	command = "CREATE TABLE IF NOT EXISTS login (username TEXT, password TEXT);"   #creates users table if it doesnt exist
	c.execute(command)
	db.commit()
	db.close()       #closes and commits changes

def insertIntoLoginTable(userStr,passwordStr):
	f="data/songs.db"
	db=sqlite3.connect(f)         #connects to Datebase to allow editing
	c=db.cursor()
	command = "INSERT INTO login VALUES('%s','%s');"%(userStr,passwordStr)
	c.execute(command)
	db.commit()
	db.close()

def isStringInTableCol(searchString,table,column):
		f="data/songs.db"
		db=sqlite3.connect(f)
		c=db.cursor()
		command= "SELECT " + column + " FROM " +  table + ";"
		colData=c.execute(command)
		for entry in colData:
			for deeperEntry in entry:
				if searchString==deeperEntry:
					db.commit()
					db.close()
					return True
		db.commit()
		db.close()
		return False

def isMatchUserAndPass(username,password):
	f="data/songs.db"
	db=sqlite3.connect(f)
	c=db.cursor()
	command = "SELECT username FROM login WHERE username='" + username + "' AND password='" + password + "';"
	c.executescript(command)
	user = c.execute(command)
	print "SELECT username FROM login WHERE username='" + username + "' AND password='" + password + "';"
	try:
		alls = c.fetchall()
		print alls
		if alls == []:
			return False
		for x in alls:
			return x
	except:
		return False
