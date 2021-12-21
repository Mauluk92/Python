from flask import Flask, render_template, Blueprint
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from auth import *
from flask_login import current_user, UserMixin, AnonymousUserMixin
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)
basedir = "\\C:Users\\Nicola\\Documents\\Python\\WhiteRose_Library"
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql:///data'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '4982hr2hfu2bf'
csrf = CSRFProtect(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True

class Role(db.Model):
    __tablename__="roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, default='regular_user')
    users = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %r>' %self.name

class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    borrowers = db.relationship('Book', backref='user')
    password_hash = db.Column(db.String(128))

    
    def __repr__(self):
        return '<User %r>' %self.username
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)
    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

class Book(db.Model):
    __tablename__="books"
    id = db.Column(db.Float, primary_key=True)
    availability = db.Column(db.Boolean, unique=True)
    borrower = db.Column(db.String(64),db.ForeignKey('users.username'), unique=True, nullable=True)
    title = db.Column(db.String(64), unique=True)
    date_of_borrow = db.Column(db.Date, unique=True, nullable=True)
    author= db.Column(db.String(64))

    def __repr__(self):
        return '<Title %r, Author %r, Availability %r, Lended on %r>' %self.title, author, self.availability, self.date_of_borrow

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/explore')
def explore():
    return render_template('explore.html')

if __name__=='__main__':
    login_manager.init_app(app)
    app.register_blueprint(auth)
    manager.run()
