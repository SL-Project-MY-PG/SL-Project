from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
# follows=db.Table('follows',db.Column('uid_who',db.Integer,db.ForeignKey('user.uid'),primary_key=True),db.Column('uid_whom',db.Integer,db.ForeignKey('user.uid'),primary_key=True))
projectdetails=db.Table('project application',db.Column('project id',db.Integer,db.ForeignKey('project.pid'),primary_key=True),db.Column('faculty id',db.Integer,db.ForeignKey('faculty.userid'),primary_key=True),db.Column('user id',db.Integer,db.ForeignKey('user.userid'),primary_key=True),db.Column('SOP',db.String(2000),db.ForeignKey('faculty.userid')))
class User(db.Model):
    __tablename__="user"
    userid=db.Column(db.Integer,primary_key=True, unique=True,autoincrement=True)
    name=db.Column(db.String(120), nullable=False)
    email=db.Column(db.String(120), nullable=False)
    passw=db.Column(db.String(120), nullable=False)
    academicdiv=db.Column(db.String(256))
    sem1marks=db.Column(db.String(5))
    sem2marks=db.Column(db.String(5))
    sem3marks=db.Column(db.String(5))
    sem4marks=db.Column(db.String(5))
    sem5marks=db.Column(db.String(5))
    sem6marks=db.Column(db.String(5))
    sem7marks=db.Column(db.String(5))
    sem8marks=db.Column(db.String(5))
    sem9marks=db.Column(db.String(5))
    sem10marks=db.Column(db.String(5))
    skills=db.Column(db.String(1024))
    pid = db.relationship("projectdetails", backref=backref("project application", uselist=False))

    def __init__(self,passw,name,ema,academic,sem1,sem2,sem3,sem4,sem5,sem6,sem7,sem8,sem9,sem10,skills):
        self.name=name
        self.email=ema
        self.passw=passw
        self.academicdiv=academic
        self.sem1marks=sem1
        self.sem2marks=sem2
        self.sem3marks=sem3
        self.sem4marks=sem4
        self.sem5marks=sem5
        self.sem6marks=sem6
        self.sem7marks=sem7
        self.sem8marks=sem8
        self.sem9marks=sem9
        self.sem10marks=sem10
        self.skills=skills

        
class Faculty(db.Model):
    __tablename__="faculty"
    userid=db.Column(db.Integer,primary_key=True, unique=True,autoincrement=True)
    name=db.Column(db.String(120), nullable=False)
    email=db.Column(db.String(120), nullable=False)
    passw=db.Column(db.String(120), nullable=False)
    academicdiv=db.Column(db.String(256))
    #posts=db.relationship('Post',backref='user')
    pid = db.relationship("projectdetails", backref=backref("project application", uselist=False))


    def __init__(self,passw,name,email,academic):
        self.name=name
        self.email=email
        self.passw=passw
        self.academicdi=academic
        
class Project(db.Model):
    __tablename__="project"
    pid=db.Column(db.Integer,primary_key=True, unique=True,autoincrement=True)
    title=db.Column(db.String(120),nullable=False)
    description=db.Column(db.String(5000))
    stream=db.Column(db.String(120))
    facultyname=db.Column(db.String(120))
    maxnostu=db.Column(db.String(5))
    requisites=db.Column(db.String(512))
    # likes=db.Column(db.Integer)
    # active=db.Column(db.Integer)
    #uid=db.Column(db.Integer,db.ForeignKey('user.uid'),nullable=False)
    #lik=db.relationship('user',secondary=liketab)
    pid = db.relationship("projectdetails", backref=backref("project application", uselist=False))


    def __init__(self, ptitle,desc,stream,facultyname,maxnostu,requisites):
        self.title=ptitle
        self.description=desc
        self.stream=stream
        self.facultyname=facultyname
        self.maxnostu=maxnostu
        self.requisites=requisites



    