from flask import Flask, render_template, request, session, redirect, url_for, flash
from utils import database
import os, sqlite3, hashlib, requests, json

app = Flask(__name__)
app.secret_key = os.urandom(64)
database.createTable()


@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home')
def home():
        return render_template('home.html')


@app.route('/makeaccount',methods = ['GET','POST'])
def makeaccount():
	username = request.form['username']
	password = request.form['password']
	confirmPassword = request.form['confirmPassword']

	#check if username already exists
	if (database.isStringInTableCol(username,'login','username')==True):
		"""return render_template('accountErrorPage.html',linkString='/register',buttonString='Username already exists, click here to go back')"""
		flash("Username already exists.")
		return redirect(url_for('register'))
		#check if passwords are the same
	elif(password != confirmPassword):
		"""return render_template('accountErrorPage.html',linkString='/register',buttonString='Passwords do not match, click here to try again')"""
		flash("Passwords do not match")
		return redirect(url_for('register'))
	#all seems good, add to DB
	else:
		database.insertIntoLoginTable(username,password)
		return render_template('login.html')


@app.route('/logout')
def logout():
    #print "USERNAME"
    #print session['user']
    #print session
    if session.has_key("user") == True:
        username = session.pop('user')
        msg = "Successfully logged out " + username
        flash(msg)
        return redirect(url_for('login'))
    else:
        return render_template('home.html')

@app.route('/login',methods=['GET','Post'])
def login():
	#print session.has_key("user")
	if session.has_key("user") == False:
		return render_template('login.html')
	return redirect(url_for('userWelcome'))

@app.route('/register',methods=['GET','Post'])
def register():
    if 'user' in session:
        #print "USER\n"
        #print session
        flash("You are already logged in")
        return redirect(url_for("userWelcome"))
    return render_template('register.html')



@app.route('/userWelcomePage',methods=['GET','POST'])
def userWelcome():
    if bool(session) == False:
        if request.form['submitType'] == "Sign In": #detects a sign in request
            username = request.form['username']
            password = request.form['password']
        if (database.isMatchUserAndPass(username,password) != False):	#check if user login is correct
            thing = database.isMatchUserAndPass(username,password)
            print thing
            yes = ''.join(thing)
            session['user']=yes
            flash(session['user'])
            return render_template('input.html')
        else:
            flash("Wrong Password.")
            return redirect(url_for('login'))
    else:
        return render_template('home.html')






if __name__ == '__main__':
	app.debug = True
	app.run()        #runs the app
