from flask import Blueprint, render_template, url_for, redirect, flash, session 
from flask_login import login_user, login_required, logout_user
from forms import LoginForm, Registration
from flask_login import LoginManager, current_user
from app import User, db
from flask_session import Session
from flask_login import AnonymousUserMixin
auth = Blueprint(
        'auth',
        __name__,
        template_folder='templates/auth',
        url_prefix="/auth"
        )

login_manager= LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'



@auth.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    if loginform.validate():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user != None and user.verify_password(loginform.password.data):
            login_user(user, loginform.remember_me.data)
            return redirect(url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html', loginform=loginform)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))



@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
    
@auth.route('/register', methods=['GET', 'POST'])
def register():
    registrationform = Registration()
    if registrationform.validate():
        user = User(email=registrationform.email.data, username=registrationform.username.data, password=registrationform.password.data)
        db.session.add(user)
        flash('Now you can login')
        return redirect(url_for('auth.login'))
    flash('Oops something gone wrong')
    return render_template('register.html', registrationform=registrationform)