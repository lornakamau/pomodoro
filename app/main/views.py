from flask import render_template,abort,redirect,url_for,request,flash,abort
from . import main
from ..models import User, Task
from .forms import LoginForm, SignUpForm, UpdateProfile
from .. import db,photos
from flask_login import login_required, current_user, login_user, logout_user
from ..email import mail_message 

@main.route('/signup', methods = ["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        mail_message("Welcome to Pitch","email/welcome_user",user.email,user=user)

        return redirect(url_for('auth.login'))
    title = "New Account | Pomodoro"
    return render_template('main/signup.html', signup_form = form, title=title)

@main.route('/', methods = ["GET", "POST"])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password', 'danger')
    
    title = "Login | Pomodoro"
    return render_template('login.html', login_form = form, title=title)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    
    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/tasks/<user_id>')
@login_required
def tasks(user_id):
    user = User.query.filter_by(user_id = user_id).first()
    if user is None:
        abort(404)
    tasks = Task.get_user_tasks(user_id)
    title = current_user.username + " | Tasks"
    return render_template('tasks.html',tasks=tasks, title=title, user=user)
