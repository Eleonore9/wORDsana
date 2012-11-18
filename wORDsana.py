#!/usr/local/bin/python
# -*- coding=UTF-8 -*-
import os, sys
from flask import Flask, flash, render_template, redirect, request, url_for, session
import model

app = Flask(__name__)
app.secret_key = 'je_peux_pas_le_dire_c_est_un_secret'

#-------------------To configure the App-----------------------------
# login_manager = LoginManager()
# login_manager.setup_app(app)

# @login_manager.user_loader
# def load_user(userid):
# 	return User.get(userid)

# login_manager.login_view = "authenticate"

#---------------To login and access the app--------------------------
@app.route("/")
def index():
    return render_template("login.html")

@app.route("/authenticate", methods=['POST'])
def authenticate():
	email = request.form['email']
	password = request.form['password']
	user_auth = model.User.authenticate(email, password)
	if user_auth != None:
		session['user_id'] = user_auth.id
		flash('You were logged in successfully!')
		return redirect(url_for("view_userpage"))
	return redirect(url_for("index"))

@app.route("/sign_up")
def sign_up():
    return render_template("signup.html")

@app.route("/new_user", methods=['POST','GET'])
def new_user():
	email = request.form['email']
	password = request.form['password1']
	username = request.form['username']
	if model.User.authenticate(email, password) == None:
		if len(password) >= 5 and request.form['password1'] == request.form['password2']:
			if model.User.check_name(username) == None:
				new_user = model.User.new(email, password, username)
				if new_user != None:
					session['user_id'] = new_user.id
					return redirect(url_for("view_userpage"))
				return redirect(url_for("index"))
			else:
				flash("This username is already used. Please choose another one!")
				return redirect(url_for("sign_up"))			
		else:
			flash("Please retype your password")
			return redirect(url_for("sign_up"))		
	else:
		flash("You already have an account!")
		flash("Please, log in below with your email and password.")
		return redirect(url_for("index"))

#-----------------------User Page------------------------------------
@app.route("/user_page")
def view_userpage():
    return render_template("user_page.html")

@app.route("/settings")
def settings():
	pass


#-------------------------Log out------------------------------------
@app.route("/logout")
def logout():
	session.pop('user_id', None)
	flash('You were logged out.')
	return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
