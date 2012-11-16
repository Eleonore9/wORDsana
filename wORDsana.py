#!/usr/local/bin/python
# -*- coding=UTF-8 -*-
import os, sys
from flask import Flask, render_template, redirect, request, url_for, session



app = Flask(__name__)


#---------------To login and access the app--------------------------
@app.route("/")
def index():
    return render_template("login.html")

@app.route("/sign_up")
def sign_up():
    return render_template("signup.html")

@app.route("/authenticate")
def authenticate():
	pass

@app.route("/new_user")
def new_user():
	pass

#-----------------------User Page------------------------------------
@app.route("/user_page")
def view_userpage():
    return render_template("test.html")



if __name__ == "__main__":
    app.run(debug=True)
