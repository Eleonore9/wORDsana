#!/usr/local/bin/python
# -*- coding=UTF-8 -*-
import os, sys
from flask import Flask, render_template, redirect, request, url_for, session
import model


app = Flask(__name__)


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
	print email
	print password
	user_auth = model.User.authenticate(email, password)
	if user_auth != None:
		return redirect(url_for("view_userpage"))
	else:
		return redirect(url_for("index"))


@app.route("/new_user")
def new_user():
	pass

#-----------------------User Page------------------------------------
@app.route("/user_page")
def view_userpage():
    return render_template("user_page.html")



if __name__ == "__main__":
    app.run(debug=True)
