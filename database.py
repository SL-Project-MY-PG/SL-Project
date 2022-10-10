from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
# follows=db.Table('follows',db.Column('uid_who',db.Integer,db.ForeignKey('user.uid'),primary_key=True),db.Column('uid_whom',db.Integer,db.ForeignKey('user.uid'),primary_key=True))
# liketab=db.Table('liketab',db.Column('uid_who',db.Integer,db.ForeignKey('user.uid'),primary_key=True),db.Column('pid',db.Integer,db.ForeignKey('post.pid'),primary_key=True),db.Column('like_date',db.DateTime))
class User(db.Model):
    __tablename__="user"
    userid=db.Column(db.Integer,primary_key=True, unique=True,autoincrement=True)
    name=db.Column(db.String(120), nullable=False)
    email=db.Column(db.String(120), nullable=False)
    passw=db.Column(db.String(120), nullable=False)
    academicdiv=db.Column(db.String(256))
    role=db.Column(db.String(128))
    #posts=db.relationship('Post',backref='user')

    def __init__(self,passw,name,email,academic,rol):
        self.name=name
        self.email=ema
        self.passw=passw
        self.academicdi=academic
        self.role=rol
        
# class Post(db.Model):
#     __tablename__="post"
#     pid=db.Column(db.Integer,primary_key=True, unique=True,autoincrement=True)
#     ptitle=db.Column(db.String(120),nullable=False)
#     pdate=db.Column(db.DateTime)
#     pdesc=db.Column(db.String(500))
#     pimgpath=db.Column(db.String(120))
#     likes=db.Column(db.Integer)
#     active=db.Column(db.Integer)
#     #uid=db.Column(db.Integer,db.ForeignKey('user.uid'),nullable=False)
#     #lik=db.relationship('user',secondary=liketab)

#     def __init__(self, pid, ptitle,pdate,desc,uid,img,like=0,act=1):
#         self.pid=pid
#         self.ptitle=ptitle
#         self.pdate=pdate
#         self.pdesc=desc
#         self.pimgpath=img
#         self.likes=like
#         self.active=act
#         self.uid=uid

    