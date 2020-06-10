from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model): #db.Model helps connect our class to our database
    __tablename__ = 'users' #gives tables in our database proper names
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    tasks = db.relationship('Task', backref='user',lazy="dynamic")

    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute') #raises an attribute error when we try to access the password

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)

    def __repr__(self): #defines how the user object will be constructed when the class is called
        return f'{self.username}'

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer,primary_key = True)
    task_title = db.Column(db.String())    
    task_description = db.Column(db.String())
    break_description = db.Column(db.String())
    task_duration = db.Column(db.Integer())
    break_duration = db.Column(db.Integer())
    task_start_time = db.Column(db.DateTime,default=datetime.utcnow)    
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_task(self):
            db.session.add(self)
            db.session.commit()

    def __repr__(self):
        return f'{self.task_title}'