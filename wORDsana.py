#!/usr/local/bin/python
# -*- coding=UTF-8 -*-
import os, sys
from flask import Flask, render_template, redirect, request, url_for, session, g



app = Flask(__name__)


#---------------To login and access the app--------------------------
# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/sign_up")
# def sign_up():
#     return render_template("sign_up.html")


#-----------------------User Page------------------------------------
# @app.route("/user_page")
@app.route("/")
def view_userpage():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)
