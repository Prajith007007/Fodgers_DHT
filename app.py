from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
from functools import wraps

import requests
import os

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.user_sqlite3'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(300), nullable=False)
app.config['SECRET_KEY'] = '1234567DHTCONSOLE'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'log' in session:
            return f(*args,**kwargs)
        else:
            flash("You need to login first","danger")
            return redirect(url_for('login'))

    return wrap

#home route 
@app.route("/")
def home():
    return render_template("home.html")

#Route for registering the user.
@app.route("/register", methods=["GET", "POST"])
def register():
    #flash(request.url_root)
    if request.method == "POST":
        name = request.form.get("name_field")
        username = request.form.get("user_field")
        email = request.form.get("email_field")
        password = request.form.get("password_field")
        confirm = request.form.get("password_confirm")
        secure_password = sha256_crypt.encrypt(str(password))
        user = Users.query.filter_by(username=username).first()
        if password == confirm:
            if user is None:
                new_user = Users(name=name, username=username, email=email, password=secure_password)
                test_response = requests.post('http://pj007.pythonanywhere.com/registerNetwork', json={'email_field': email, 'host_url_field': request.url_root})   
                if test_response.ok:
                    flash("host has been registered")
                else:
                    return "error"

                db.session.add(new_user)
                db.session.commit()
                flash("You are registered and can login","success")
                return redirect(url_for('login'))
            else:
                flash("Username already used","danger")
                return render_template("register.html")
        else:
            flash("Password does not match","danger")
            return render_template("register.html")

    return render_template("register.html")

#Route for login 
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("user_field")
        password = request.form.get("password_field")
        user = Users.query.filter_by(username=username).first()
        if user is None:
            flash("No username","danger")
            return render_template("login.html")
        else:
            if user and sha256_crypt.verify(password, user.password):
                session["log"] = True
                test_response = requests.post('http://pj007.pythonanywhere.com/updateNetwork', json={'email_field': user.email, 'host_url_field': request.url_root})   
                if test_response.ok:
                    print()
                else:
                    return "error"
                flash("You are now login","success")
                return redirect(url_for('home'))
            else:
                flash("Incorrect password","danger")
                return render_template("login.html")

    return render_template("login.html")
#Route for logout
@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You are Logged out","danger")
    return redirect(url_for('login'))
#this endpoint allows other nodes to upload file
@app.route("/imageUpdate", methods=["POST"])
def imageUpdate():

    user_image = request.files['user_image']
    print(user_image)
    target = os.path.join(APP_ROOT, 'images/')

    if not os.path.isdir(target):
        os.mkdir(target)
    if 'file' not in request.files:
        print('No file part') #return error response code
    else:
        file = request.files['user_image']
        destination = "/".join([target, file.filename])
        file.save(destination)

    return render_template("upload.html")


#this endpoint is for uploading files
@app.route("/upload", methods=["GET","POST"])
@login_required
def upload():
    target = os.path.join(APP_ROOT,'images/')
    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        if filename :
            destination = "/".join([target, filename])
            file.save(destination)
            os.system('python utils/encryption.py')
            flash("File Uploaded", "success")
           #it only picks files if its on the same path as this project, need to change that 
            files = {'user_image': open(filename, 'rb')} 
            # flash("File Uploaded", "success")
            test_response = requests.post('http://bec1e971dee4.ngrok.io/imageUpdate', files=files)
            if test_response.ok:
             flash("Upload completed successfully!" ,"success")
            else:
             flash("Something went wrong!")
            # content = response.content
            return redirect(url_for('upload'))
        else:
            flash("Please attach a file","danger")
            return redirect(url_for('upload'))
    return render_template("upload.html")
if __name__ == "__main__":
    app.run(debug=True)