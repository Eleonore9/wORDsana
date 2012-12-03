#!/usr/local/bin/python
# -*- coding=UTF-8 -*-
import os, sys
from flask import Flask, flash, render_template, redirect, request 
from flask import url_for, session, send_from_directory
import model
import datetime
import pretty

app = Flask(__name__)
app.secret_key = 'je_peux_pas_le_dire_c_est_un_secret'

@app.teardown_request
def teardown_request(exc):
	model.session.close()

#---------------To login and access the app--------------------------
@app.route("/")
def index():
    return render_template("login.html")

@app.route("/authenticate", methods=['POST'])
def authenticate():
	print 1
	email = request.form['email']
	password = request.form['password']
	print 2
	user_auth = model.User.authenticate(email, password)
	print 3
	if user_auth is not None:
		session['user_id'] = user_auth.id
		flash('You were logged in successfully!')
		print 4
		return redirect(url_for("enter_text"))
	return redirect(url_for("index"))

@app.route("/sign_up")
def sign_up():
    return render_template("signup.html")

@app.route("/new_user", methods=['POST','GET'])
def new_user():
	email = request.form['email']
	password = request.form['password1']
	username = request.form['username']
	if model.User.authenticate(email, password) is not None:
		flash("You already have an account!")
		flash("Please, log in below with your email and password.")
		return redirect(url_for("index"))
	
	if len(password) < 5 or request.form['password1'] != request.form['password2']:
		flash("Please retype your password")
		return redirect(url_for("sign_up"))

	if model.User.check_name(username) is not None:
		flash("This username is already used. Please choose another one!")
		return redirect(url_for("sign_up"))

	new_user = model.User.new(email, password, username)
	if new_user is not None:
		session['user_id'] = new_user.id
		return redirect(url_for("enter_text"))
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

@app.route("/enter_text")
def enter_text():
	print "At /enter_text"
	user_id = session.get("user_id", None)
	if user_id:
		return render_template("enter_text.html")
	
	print "not logged in"
	flash('Log in to access this page!')
	return redirect(url_for("index"))

@app.route("/save_text", methods=['POST'])
def save_text():
	user_id = session.get("user_id", None)
	# "Guard clause"
	if not user_id:
		flash('Log in to access this page!')
		return redirect(url_for("index"))

	text = request.form['text']
	posted_at = datetime.datetime.now()
	post = model.Post.new(None, text, posted_at, user_id)
	post_id = post.id
	return redirect(url_for("use_recorder", post_id=post_id))

@app.route("/recorder/<int:post_id>")
def use_recorder(post_id):
	user_id = session.get("user_id", None)
	if user_id:
		return render_template("use_recorder.html", id=post_id)
	
	flash('Log in to access this page!')
	return redirect(url_for("index"))

#for Sound files and Sound URLs, cf. "Saving Audio"

@app.route("/display_collection")
def display_collection():
	user_id = session.get("user_id", None)
	user = model.User.get(user_id)
	rows = model.User.get_posts(user, user_id)
	# for row in rows:
	# 	post_id = row.id
	# 	comments = model.Post.get_comments(row, post_id)
	# 	num_likes = model.Post.num_likes(row, post_id)
	# 	num_comments = model.Post.num_comments(row, post_id)
	return render_template("display_collection.html", rows=rows)
	#return render_template("display_collection.html", rows=rows, comments=comments)
	#return render_template("display_collection.html", rows=rows, num_likes=num_likes, num_comments=num_comments)

#-------------------------User Settingss-------------------------------
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

#------------------------All Collections-------------------------------
@app.route("/all_collections")
def all_collections():
	all_posts = model.Post.all()
	return render_template("all_collections.html", posts=all_posts)

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
	new_file = open("static/upload/recording_%d.wav" % id, "wb")
	new_file.write(request.data)
	new_file.close()
	post = model.Post.get(id)
	post.sound = "/get_audio/%d" % id
	model.session.commit()
	return "audio file"

@app.route("/get_audio/<int:id>")
def get_audio(id):
	return send_from_directory("static/upload/", "recording_%d.wav" % 
		id)

#-------------------------Adding comments----------------------------
@app.route("/add_like/<int:post_id>", methods=['POST'])
def add_like(post_id):
	posted_at = datetime.datetime.now()
	user_id = session.get("user_id", None)
	model.Comment.new_like(1, None, None, posted_at, post_id, user_id)
	return redirect(url_for("display_collection"))

@app.route("/add_text_comment/<int:post_id>", methods=['POST'])
def text_comment(post_id):
	print post_id
	text = request.form['text_comment']
	posted_at = datetime.datetime.now()
	user_id = session.get("user_id", None)
	print user_id
	model.Comment.new_comment(0, None, text, posted_at, user_id, post_id)
	return redirect(url_for("display_collection"))

#-------------------------Deleting stuffs----------------------------
@app.route("/delete_sound/<int:post_id>", methods=['POST'])
def delete_sound(post_id):
	post = model.Post.get(post_id)
	model.Post.delete_sound(post, post_id)
	flash('Your sound was deleted')
	return redirect(url_for("display_collection"))

@app.route("/delete_text/<int:post_id>", methods=['POST'])
def delete_text(post_id):
	post = model.Post.get(post_id)
	model.Post.delete_text(post, post_id)
	flash('Your text was deleted')
	return redirect(url_for("display_collection"))

@app.route("/delete_comment/<int:post_id>", methods=['POST'])
def delete_comment(post_id):
	post = model.Post.get(post_id)
	model.Post.delete_comment(post, post_id)
	flash('Your comment was deleted')
	return redirect(url_for("display_collection"))

#-------------------------Log out------------------------------------
@app.route("/logout")
def logout():
	session.pop('user_id', None)
	flash('You were logged out.')
	return redirect(url_for('index'))


#-------------------------calling Flask Filters ---------------------
@app.template_filter("pretty_date")
def pretty_date_filter(d):
	return pretty.date(d)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

	# app.run(debug=True, host="0.0.0.0")




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