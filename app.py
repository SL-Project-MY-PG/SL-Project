'''importing necessary modules'''

from flask import Flask,render_template,request,session,flash,redirect,url_for,send_from_directory
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import random, copy
import smtplib
import requests
import string
from email.mime.text import MIMEText
from flask_mail import Mail
import random
import os
from database import db,User,Faculty,Project,projectdetails
import re


'''setting configuration for flask app'''
app=Flask(__name__)
app.secret_key='mypg'

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://euagmhwjjvvmlz:07ac7058827bcbb66f09f61807631b71da95537b8b2840d0a40b0ceca1b77b88@ec2-54-163-34-107.compute-1.amazonaws.com:5432/dj5uolrhsug0j'
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:mypg@localhost/mypg'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config['MAIL_SERVER']='smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'sllab123@outlook.com'
app.config['MAIL_PASSWORD'] = 'LAN@Spider'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


''' initializing flask mail object'''
mail = Mail(app)


''' creating database '''
db.init_app(app)
with app.app_context():
    db.create_all()


''' rendering pages using flask '''
@app.route("/",methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/static/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsoft.icon')

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


''' url for student to sign in'''
@app.route("/loginStudent", methods = ['POST'])
def loginStudent():
    if(request.method=='POST'):
        email = request.form.get('exampleInputEmail1')
        passw = request.form.get('exampleInputPassword1')
        getinfo = db.session.query(User).filter_by(email=email,passw=passw).count()

        if getinfo==1:
            session['logged_in'] = True
            getprojinfo=db.session.query(Project).all()
            # import pdb;pdb.set_trace()
            a = db.session.query(User).filter_by(email=email,passw=passw).first()
            for i in range(len(a.projects)):
                if a.projects[i] in getprojinfo:
                    getprojinfo.remove(a.projects[i])
            sopsarray=dict()
            for projects in a.projects:
                sops=db.session.query(projectdetails).filter_by(project_id=projects.pid).all()
                for i in sops:
                    sopsarray[(i[0],i[1])]=sopsarray[(i[0],i[1])]=[i[2],i[3]]
            return render_template('studashboard.html', projects=getprojinfo,stud=a,soparray=sopsarray)

        else:
            return render_template('signinstud.html', message="Username/Password Incorrect")


''' url for student sign up'''
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
        # calculating the length
        lengthbit = len(passw) < 8

        # searching for digits
        digitbit = re.search(r"\d",passw ) is None
        print(digitbit)
        # searching for uppercase
        uppercasebit = re.search(r"[A-Z]", passw) is None
        print(uppercasebit)
        # searching for lowercase
        lowercasebit = re.search(r"[a-z]", passw) is None
        print(lowercasebit)
        # searching for symbols
        symbolbit = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~@"+r'"]', passw) is None
        print(symbolbit)
        # overall result
        overallbit = not ( lengthbit or digitbit or uppercasebit or lowercasebit or symbolbit )
        print(overallbit)
        if  overallbit:
            user=User(passw=passw,name=name,ema=email,academic=academicdiv,sem1=sem1marks,sem2=sem2marks,sem3=sem3marks,sem4=sem4marks,sem5=sem5marks,sem6=sem6marks,sem7=sem7marks,sem8=sem8marks,sem9=sem9marks,sem10=sem10marks,skills=skills)
            db.session.add(user)
            db.session.commit()
            return render_template("signinstud.html",message="Account created. Now you can Login")
        else:
            return render_template("signinstud.html",message="Password too weak! Cannot create account")


'''url for faculty sign in '''
@app.route("/loginFaculty", methods = ['POST'])
def loginFaculty():
    if(request.method=='POST'):
        email = request.form.get('exampleInputEmail1')
        passw = request.form.get('exampleInputPassword1')
        getinfo = db.session.query(Faculty).filter_by(email=email,passw=passw).count()

        if getinfo==1:
            session['logged_in'] = True
            ab=db.session.query(Faculty).filter_by(email=email,passw=passw).first()
            sopsarray=dict()
            for projects in ab.proid:       #For each project of faculty we extract student.
                sops=db.session.query(projectdetails).filter_by(project_id=projects.pid).all()
                for i in sops:
                    sopsarray[(i[0],i[1])]=[i[2],i[3]]
            return render_template('facdashboard.html',facid=ab,soparray=sopsarray)
        else:
            return render_template('signinfac.html', message="Username/Password Incorrect")


''' url for faculty sign up'''
@app.route("/signupF", methods = ['POST'])
def signupF():
    if(request.method=='POST'):
        name=request.form.get('name')
        academicdiv=request.form.get('academicdivision')
        email=request.form.get('exampleInputEmail1')
        passw = request.form.get('exampleInputPassword1')

        # calculating the length
        lengthbit = len(passw) < 8

        # searching for digits
        digitbit = re.search(r"\d",passw ) is None

        # searching for uppercase
        uppercasebit = re.search(r"[A-Z]", passw) is None
    
        # searching for lowercase
        lowercasebit = re.search(r"[a-z]", passw) is None
    
        # searching for symbols
        symbolbit = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~@"+r'"]', passw) is None

        # overall result
        overallbit = not ( lengthbit or digitbit or uppercasebit or lowercasebit or symbolbit )

        if  overallbit:
            faculty=Faculty(passw=passw,name=name,email=email,academic=academicdiv)
            db.session.add(faculty)
            db.session.commit()
            return render_template("signinfac.html",message="Account created. Now you can Login")
        else:
            return render_template("signinfac.html",message="Password too weak! Cannot create account")


''' url for faculty to create a new project'''
@app.route("/submitProject", methods = ['POST'])
def submitProject():
    if(request.method=='POST'):
        faci=request.form.get('facid')
        title=request.form.get('proj.title')
        stream=request.form.get('proj.stream')
        description=request.form.get('proj.description')
        maxstu = request.form.get('proj.maxnostu')
        prereq = request.form.get('proj.requisites')
        facu= request.form.get('proj.facultyname')
        pro=Project(ptitle=title,desc=description,stream=stream,facultyname=facu,maxnostu=maxstu,requisites=prereq,fac=faci)
        db.session.add(pro)
        db.session.commit()
        ab=db.session.query(Faculty).filter_by(userid=faci).first()
        sopsarray=dict()

        for projects in ab.proid:       #For each project of faculty we extract student.
            sops=db.session.query(projectdetails).filter_by(project_id=projects.pid).all()
            for i in sops:
                sopsarray[(i[0],i[1])]=[i[2],i[3]]
        return render_template('facdashboard.html',facid=ab,soparray=sopsarray)
    else:
        return render_template("index.html")


''' url for student to apply to a project'''
@app.route("/applyforProject/<data>", methods = ['POST'])
def applyforProject(data):
    if(request.method=='POST'):
        sop=request.form.get('sop')
        proid = request.form.get('projectid')
        #import pdb;pdb.set_trace()
        userobject=db.session.query(User).filter_by(userid=data).first()
        projectobject=db.session.query(Project).filter_by(pid=proid).first()
        application = projectdetails.insert().values(project_id = proid,user_id = data ,SOP = sop, Shortlisted=0)
        db.session.execute(application)
        db.session.commit()
        getprojinfo=db.session.query(Project).all()
        a = db.session.query(User).filter_by(userid=data).first()

        for i in range(len(a.projects)):
            if a.projects[i] in getprojinfo:
                getprojinfo.remove(a.projects[i])

        sopsarray=dict()

        for projects in a.projects:       #For each project of student we extract shortlisting.
            sops=db.session.query(projectdetails).filter_by(project_id=projects.pid).all()
            for i in sops:
                sopsarray[(i[0],i[1])]=sopsarray[(i[0],i[1])]=[i[2],i[3]]
        return render_template('studashboard.html', projects=getprojinfo,stud=a,soparray=sopsarray)
    else:
        return render_template("index.html")


''' url for faculty to shortlist a student '''
@app.route("/shortlist_student",methods=["POST"])
def shortlist_student():
    if request.method=='POST':
        studid=request.form.get("studid")
        proid=request.form.get("projectid")
        faci=request.form.get("facid")
        short=db.session.query(projectdetails).filter_by(project_id=proid,user_id=studid).update(dict(Shortlisted=1))
        #db.session.add(short)
        db.session.commit()
        print(studid,proid,faci)
        ab=db.session.query(Faculty).filter_by(userid=faci).first()
        sopsarray=dict()

        for projects in ab.proid:       #For each project of faculty we extract student.
            sops=db.session.query(projectdetails).filter_by(project_id=projects.pid).all()
            for i in sops:
                sopsarray[(i[0],i[1])]=sopsarray[(i[0],i[1])]=[i[2],i[3]]
        return render_template('facdashboard.html',facid=ab,soparray=sopsarray)


''' url for forget password functionality '''
@app.route("/forget/<role>",methods = ['GET', 'POST'])
def forget(role):
    return render_template("forget.html",role=role)


''' url to reset and send the password to user email '''
@app.route("/reset",methods = ['GET', 'POST'])  
def reset():
    email = request.form.get('email')
    role=request.form.get('role')

    if role=="0":
        getinfo = db.session.query(User).filter_by(email=email)
    elif role=="1":
        getinfo = db.session.query(Faculty).filter_by(email=email)
    else:
        return render_template('signinstud.html', message="Some error occured!")

    smail="sllab123@outlook.com"
    if getinfo.count()==1:
        pas=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        getinfo.update(dict(passw=pas))
        message="Hello There .<br>Your Password has been generated .<br>Your password is <strong>%s</strong>.<br>Please login with this password to change password"%(pas)
        #db.session.add(getinfo)
        db.session.commit()
        mail.send_message(subject="Password Generated",html=message,sender=smail,recipients = [email])
        if role=="0":
            return render_template('signinstud.html', message="A new password has been sent to your email ID")
        if role=="1":
            return render_template('signinfac.html', message="A new password has been sent to your email ID")
    else:
        if role=="0":
            return render_template('signinstud.html', message="Some error occured!")
        else:
            return render_template('signinfac.html', message="Some error occured!")

''' main function'''
if __name__=="__main__":
    app.run(debug=True)

