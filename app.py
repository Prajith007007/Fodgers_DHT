from flask import Flask,render_template,request,session,logging,url_for,redirect,flash,jsonify,json
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
from functools import wraps

import requests
import os

import glob

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.user_sqlite3'

db = SQLAlchemy(app)

URL = "http://pj007.pythonanywhere.com/"

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(300), nullable=False)

app.config['SECRET_KEY'] = '1234567DHTCONSOLE'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

db.init_app(app)
db.create_all()
    
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
              

                test_response = requests.post(URL+'registerNetwork', json={'email_field': email, 'host_url_field': request.url_root})   
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
                test_response = requests.post(URL+'updateNetwork', json={'email_field': user.email, 'host_url_field': request.url_root})   
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
    email = request.form['email']
    print(request.files)
    print(request)
    print(email)
    print(user_image)
    target = os.path.join(APP_ROOT, 'images/')

    if not os.path.isdir(target):
        os.mkdir(target)
    target = os.path.join(APP_ROOT, 'images/'+email+'/')

    if not os.path.isdir(target):
        os.mkdir(target)

    if 'file' not in request.files:
        print('No file part') #return error response code
        file = request.files['user_image']
        destination = "/".join([target, file.filename])
        file.save(destination)
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

@app.route("/saveFiles", methods=["POST"])
def saveFiles():
    target = os.path.join(APP_ROOT, 'fetchedShards/')
    if not os.path.isdir(target):
        os.mkdir(target)
    
    file = request.files['fetched_image']
    destination = "/".join([target, file.filename])
    file.save(destination)
    
    return "SuccessFull"


@app.route("/fetchAllData", methods=["GET"])
def fetchAllData():
    email = request.args.get('email')
    nodeRequest = request.args.get('node')
    if((checkPathExist(email) == False)):
        return "Your Data is not in this node"
    else:
        sendFilesAsResponse(email,nodeRequest)
    
    return "Successful" #needs send reponse inside sendFilesAsResponse

def checkPathExist(email):
    print(email)
    target =  os.path.join(APP_ROOT,'images/'+email)
    print(str(target))
    if not os.path.isdir(target):
        return False
    return True

def sendFilesAsResponse(email, node):
    target = os.path.join(APP_ROOT,'images/'+email)
    if not os.path.isdir(target):
        os.mkdir(target)
    shardList = glob.glob(target+"/"+"*.fec")
    print(shardList)
    for i in range(len(shardList)):
        file = open(shardList[i])
        files = {'fetched_image': open(file.name, 'rb')}

        # flash("File Uploaded", "success")
         #url=node+'imageUpdate'
        #print(url)
  
        #data.append({'email':email})
        print(node+'saveFiles')
        test_response = requests.post(node+'saveFiles', files=files)
        print(node+'saveFiles')
        if test_response.ok:
            print("Shard send successfully to "+str(node))
        else:
            print("Sending shard to "+ str(node) +" has failed "+test_response.response)
        

@app.route("/isOnline", methods=["GET"])
def isOnline():
    res=[]
    res.append(({"host":"online"}))
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
