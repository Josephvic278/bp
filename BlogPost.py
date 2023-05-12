from flask import Flask, render_template, request, redirect, url_for
import urllib 
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
import shutil
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config["SQLALCHEMY_BINDS"] = {"user":"sqlite:///user.db" }

db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    article = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.String, nullable=False)
    author = db.Column(db.String(20), nullable=False)
    img_path = db.Column(db.String)

class User_signup(db.Model):
	__bind_key__ = "user"
	id = db.Column(db.Integer, primary_key = True)
	first_name = db.Column(db.String, default="User"+str(id))
	last_name = db.Column(db.String, nullable=False)
	user_name = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable = False)
	
#checks if database exists
list_dir = os.listdir()
if "main.db" and "user.db"not in list_dir:
    app.app_context().push()
    db.create_all()

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/t_s_f/sign_up", methods=["GET","POST"])
def sign_up():
	if request.method == "POST":
		first_name = request.form["firstname"]
		last_name = request.form["lastname"]
		user_name = request.form["username"]
		email = request.form["email"]
		password = request.form["password"]
		
		new_user = User_signup(first_name=first_name,last_name=last_name,user_name=user_name,email=email,password=password)
		
		db.session.add(new_user)
		db.session.commit()
		return redirect("/t_s_f/log_in")
	else:
		return render_template("signup.html")

@app.route("/t_s_f/log_in", methods=["GET","POST"])
def log_in():
	
	email_list1 = []
	vrd = []
	#this doesthisjdjdjdj
	log_data = db.session.query(User_signup).all()
	for email_list in range(len(log_data)):
		email_list1.append(log_data[email_list].email)
		vrd.append(log_data[email_list].password)
	
	if request.method == "POST":
		email_address = request.form["email"]
		password = request.form["password"]
		
		if email_address in email_list1:
			for db_data in range(len(log_data)):
				if password == log_data[db_data].password:
					print(log_data[db_data].id,log_data[db_data].email)
		
		return redirect ("/t_s_f/log_in")
	
	else:
		return render_template("login.html")
		

@app.route("/main", methods=["GET","POST"])
def create_post():
	if request.method=="POST":
		title = request.form["title"]
		article = request.form["content"]
    
		date_time = str(datetime.date.today()) + " " + time.strftime("%H:%M:%S")
		author = request.form["author"]
		img_path = request.form["img"]
		new_post = BlogPost(title=title, article=article, 							date_time=date_time, author=author,img_path=img_path)

		print(img_path)
		print(os.getcwd())
		db.session.add(new_post)
		db.session.commit()
		return redirect("/main")
	else:
		data = db.session.query(BlogPost).all()
		return render_template("base.html",data=data)

if __name__ == "__main__":
    app.run(debug=True)
