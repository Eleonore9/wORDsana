#!/usr/local/bin/python
# -*- coding=UTF-8 -*-
import os, sys
from flask import Flask, flash, render_template, redirect, request, url_for, session
import model


app = Flask(__name__)
app.secret_key = 'je_peux_pas_le_dire_c_est_un_secret'

#---------------To login and access the app--------------------------
@app.route("/")
def index():
    return render_template("login.html")

@app.route("/sign_up")
def sign_up():
    return render_template("signup.html")

@app.route("/authenticate", methods=['POST'])
def authenticate():
	email = request.form['email']
	password = request.form['password']
	user_auth = model.User.authenticate(email, password)
	if user_auth != None:
		return redirect(url_for("view_userpage"))
	return redirect(url_for("index"))

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



if __name__ == "__main__":
    app.run(debug=True)
