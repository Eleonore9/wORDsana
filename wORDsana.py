#!/usr/local/bin/python
# -*- coding=UTF-8 -*-
import os, sys
from flask import Flask, flash, render_template, redirect, request 
from flask import url_for, session, send_from_directory
import model
import datetime

app = Flask(__name__)
app.secret_key = 'je_peux_pas_le_dire_c_est_un_secret'

@app.teardown_request
def teardown_request(exc):
	model.session.close()
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
	if model.User.authenticate(email, password) != None:
		flash("You already have an account!")
		flash("Please, log in below with your email and password.")
		return redirect(url_for("index"))
	elif len(password) < 5 or request.form['password1'] != request.form['password2']:
		flash("Please retype your password")
		return redirect(url_for("sign_up"))	
	elif model.User.check_name(username) != None:
		flash("This username is already used. Please choose another one!")
		return redirect(url_for("sign_up"))
	else:
		new_user = model.User.new(email, password, username)
		if new_user != None:
			session['user_id'] = new_user.id
			return redirect(url_for("view_userpage"))
		return redirect(url_for("index"))
#-------------------- ---About---------------------------------------
@app.route("/about")
def about():
	return render_template("about.html")
#-----------------------User Page------------------------------------
# @app.route("/user_page")
# def view_userpage():
# 	user_id = session.get("user_id", None)
# 	if user_id:
# 		return render_template("user_page.html")
# 	else:
# 		flash('Log in to access this page!')
# 		return redirect(url_for("index"))

@app.route("/user_page1")
def view_userpage():
	user_id = session.get("user_id", None)
	if user_id:
		return render_template("user_page1.html")
	else:
		flash('Log in to access this page!')
		return redirect(url_for("index"))

@app.route("/user_page2", methods=['POST'])
def view_recorder():
	user_id = session.get("user_id", None)
	if user_id:
		text = request.form['text']
		posted_at = datetime.datetime.now()
		post = model.Post.new(None, text, posted_at, user_id)
		post_id = post.id
		return render_template("user_page2.html", id=post_id)
	else:
		flash('Log in to access this page!')
		return redirect(url_for("index"))

@app.route("/settings")
def settings():
	user_id = session.get("user_id", None)
	user = model.User.get(user_id)
	user_name = user.username
	user_email = user.email
	return render_template("settings.html", username=user_name, email=user_email)

@app.route("/save_new_password", methods=['POST'])
def save_new_password():
	new_password = request.form["new_password"]
	user_id = session.get("user_id", None)
	user = model.User.get(user_id)
	model.User.change_password(user, user_id, new_password)
	flash('Your new password has been saved!')
	return redirect(url_for("settings"))

#--------------------------Saving audio -----------------------------

@app.route("/crossdomain.xml")
def crossdomain():
	return """\
<?xml version="1.0" ?>
<cross-domain-policy>
<allow-access-from domain="*" />
</cross-domain-policy>
"""

@app.route("/record/<int:id>", methods=['POST'])
def receive_audio(id):
	new_file = open("/tmp/recording_%d.wav"%(id), "w")
	new_file.write(request.data)
	new_file.close()
	post = model.Post.get(id)
	post.sound = "/get_audio/%d"%(id)
	model.session.commit()
	return "audio file"

@app.route("/get_audio/<int:id>")
def get_audio(id):
	return send_from_directory("/tmp/", id)

#-------------------------Log out------------------------------------
@app.route("/logout")
def logout():
	session.pop('user_id', None)
	flash('You were logged out.')
	return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")








#------------example of badly written function----------------
# def new_user():
# 	email = request.form['email']
# 	password = request.form['password1']
# 	username = request.form['username']
# 	if model.User.authenticate(email, password) == None:
# 		if len(password) >= 5 and request.form['password1'] == request.form['password2']:
# 			if model.User.check_name(username) == None:
# 				new_user = model.User.new(email, password, username)
# 				if new_user != None:
# 					session['user_id'] = new_user.id
# 					return redirect(url_for("view_userpage"))
# 				return redirect(url_for("index"))
# 			else:
# 				flash("This username is already used. Please choose another one!")
# 				return redirect(url_for("sign_up"))			
# 		else:
# 			flash("Please retype your password")
# 			return redirect(url_for("sign_up"))		
# 	else:
# 		flash("You already have an account!")
# 		flash("Please, log in below with your email and password.")
# 		return redirect(url_for("index"))