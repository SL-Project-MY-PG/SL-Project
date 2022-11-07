from flask import Flask,render_template,request,session,flash,redirect,url_for,send_from_directory,flash
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import random, copy
import smtplib
import requests
import string
import random
# from werkzeug.utils import secure_filename
import os
from database import db,User,Faculty,Project
# from flask_mail import Mail


app=Flask(__name__)
app.secret_key='mypg'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://euagmhwjjvvmlz:07ac7058827bcbb66f09f61807631b71da95537b8b2840d0a40b0ceca1b77b88@ec2-54-163-34-107.compute-1.amazonaws.com:5432/dj5uolrhsug0j'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config.update(
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = '465',
#     MAIL_USE_SSL = True,
#     MAIL_USERNAME = "psp51790@gmail.com",
#     MAIL_PASSWORD=  "ps*123456"
# )
# mail = Mail(app)


db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/",methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/signinStudent", methods = ['GET'])
def signinStudent():
    return render_template("signinstud.html")

@app.route("/nav", methods = ['GET'])
def nav():
    return render_template("nav.html")

@app.route("/signupStudent", methods = ['GET'])
def signupStudent():
    return render_template("signupstud.html")

@app.route("/signinFaculty", methods = ['GET'])
def signinFaculty():
    return render_template("signinfac.html")

@app.route("/signupFaculty", methods = ['GET'])
def signupFaculty():
    return render_template("signupfac.html")

@app.route("/devs", methods = ['GET'])
def devs():
    return render_template("devs.html")

@app.route("/loginStudent", methods = ['POST'])
def loginStudent():
    if(request.method=='POST'):
        email = request.form.get('exampleInputEmail1')
        passw = request.form.get('exampleInputPassword1')
        getinfo = db.session.query(User).filter_by(email=email,passw=passw).count()
        if getinfo==1:
            session['logged_in'] = True
            getprojinfo=db.session.query(Project).all()
            return render_template('studashboard.html', projects=getprojinfo)
        else:
            return render_template('signinstud.html', message="Username/Password Incorrect")

@app.route("/signupS", methods = ['POST'])
def signupS():
    if(request.method=='POST'):
        name=request.form.get('name')
        academicdiv=request.form.get('academicdivision')
        sem1marks=request.form.get('sem1')
        sem2marks=request.form.get('sem2')
        sem3marks=request.form.get('sem3')
        sem4marks=request.form.get('sem4')
        sem5marks=request.form.get('sem5')
        sem6marks=request.form.get('sem6')
        sem7marks=request.form.get('sem7')
        sem8marks=request.form.get('sem8')
        sem9marks=request.form.get('sem9')
        sem10marks=request.form.get('sem10')
        skills=request.form.get('skills')
        email=request.form.get('exampleInputEmail1')
        passw = request.form.get('exampleInputPassword1')
        user=User(passw=passw,name=name,ema=email,academic=academicdiv,sem1=sem1marks,sem2=sem2marks,sem3=sem3marks,sem4=sem4marks,sem5=sem5marks,sem6=sem6marks,sem7=sem7marks,sem8=sem8marks,sem9=sem9marks,sem10=sem10marks,skills=skills)
        db.session.add(user)
        db.session.commit()
        return render_template("signinstud.html",message="Account created. Now you can Login")
        
@app.route("/loginFaculty", methods = ['POST'])
def loginFaculty():
    if(request.method=='POST'):
        email = request.form.get('exampleInputEmail1')
        passw = request.form.get('exampleInputPassword1')
        getinfo = db.session.query(Faculty).filter_by(email=email,passw=passw).count()
        if getinfo==1:
            session['logged_in'] = True
            return render_template('facdashboard.html')
        else:
            return render_template('signinfac.html', message="Username/Password Incorrect")

@app.route("/signupF", methods = ['POST'])
def signupF():
    if(request.method=='POST'):
        name=request.form.get('name')
        academicdiv=request.form.get('academicdivision')
        email=request.form.get('exampleInputEmail1')
        passw = request.form.get('exampleInputPassword1')
        faculty=Faculty(passw=passw,name=name,email=email,academic=academicdiv)
        db.session.add(faculty)
        db.session.commit()
        return render_template("signinfac.html",message="Account created. Now you can Login")

@app.route("/submitProject", methods = ['POST'])
def submitProject():
    if(request.method=='POST'):
        title=request.form.get('proj.title')
        stream=request.form.get('proj.stream')
        description=request.form.get('proj.description')
        maxstu = request.form.get('proj.maxnostu')
        prereq = request.form.get('proj.requisites')
        facu= request.form.get('proj.facultyname')
        pro=Project(ptitle=title,desc=description,stream=stream,facultyname=facu,maxnostu=maxstu,requisites=prereq)
        db.session.add(pro)
        db.session.commit()
        return render_template("facdashboard.html")
    else:
        return render_template("index.html")

# @app.route("/signup", methods = ['GET', 'POST'])
# def signup():
#     if(request.method=='POST'):
#         uname = request.form.get('uname')
#         name = request.form.get('name')
#         passw = request.form.get('passw')
#         rpassw = request.form.get('rpassw')
#         email= request.form.get('email')
#         phno = request.form.get('phno')
#         if passw==rpassw:
#             user1=User(passw=passw,uName=uname,name=name,cont=phno,ema=email,descrp="Hi There I am using Fake Book")
#             db.session.add(user1)
#             db.session.commit()

#         return "HEllo"

# @app.route("/forget",methods = ['GET', 'POST'])
# def forget():
#     return render_template("forget.html")
    
# @app.route("/reset",methods = ['GET', 'POST'])  
# def reset():
#     uname=request.form.get('uname')
#     email = request.form.get('email')
#     getinfo = db.session.query(User).filter_by(uname=uname,email=email)
#     smail="psp51790@gmail.com"
#     if getinfo.count()==1:
#         pas=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
#         getinfo.passw=pas
#         message="Hello There %s .<br>Your Password has been generated .<br>Your password is <strong>%s</strong>.<br>Please login with this password to change password"%(uname,pas)
#         #msg=MIMEText(message,'html')
#         db.session.commit()
#         mail.send_message(subject="Password Generated",html=message,sender=smail,recipients = [email])
#         return "Hello"
#     else:
#         return "Hi"        

if __name__=="__main__":
    app.run(debug=True)

