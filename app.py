from enum import unique
from flask import Flask,request,jsonify,session
from flask.helpers import url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import url
from werkzeug.utils import redirect
import jwt
from functools import wraps
import uuid
from flask_ckeditor import CKEditor
from wtforms import Form,StringField,TextAreaField,PasswordField,validators




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/cenkg/OneDrive/Masaüstü/pylinkdn/linkedn.db"
app.secret_key = "ajsdjadjasjdasdjasdjajsdjasdjasd"
db = SQLAlchemy(app)
ckeditor = CKEditor(app)


#token required decorator

def login_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        if "username" in session:
            return f(*args,**kwargs)
        return redirect(url_for("login"))
    return decorated



@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    else:
        email = request.form.get("email")
        password = request.form.get("password") 
        
        db_user = User.query.filter_by(email = email,password=password).first()
        if db_user:
            session["username"] = db_user.email
            
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login"))

    

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    email = request.form.get("email")
    password = request.form.get("password")
    public_id = str(uuid.uuid4())
    user = User(public_id = public_id,email = email,password=password)
  
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("login"))
    
    



@app.route("/jobs/")
@login_required
def jobs():
    #we should get all the jobs data 

    jobs = Job.query.all()

    return render_template("jobs.html",jobs = jobs)


@app.route("/job/<int:id>")
@login_required
def job_by_id(id):
    job = Job.query.filter_by(id=id).first()
    return render_template("job_by_id.html",job=job)


@app.route("/job/")
@login_required
def job_redirect():

    return redirect(url_for("jobs"))


@app.route("/advert",methods=["POST","GET"])
@login_required
def advert():
   
    if request.method == "GET":
        return render_template("advert.html")

    title = request.form.get("title")
    content = request.form.get("ckeditor")
    public_id = str(uuid.uuid4())

    job = Job(public_id = public_id, title = title, content = content)

    db.session.add(job)
    db.session.commit()
    return redirect(url_for("jobs"))



@app.route("/news")
@login_required
def news():
    return render_template("news.html")



@app.route("/profile")
@login_required
def show_profile():
    return render_template("profile.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))



class Job(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    public_id = db.Column(db.String(50),unique=True)
    title = db.Column(db.String(15))
    content = db.Column(db.String(50))



class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    public_id = db.Column(db.String(50),unique=True)
    email= db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(6),nullable=False)
    

if __name__ == "__main__":
    db.create_all()
    
    app.run(debug=True)