from flask import render_template,abort,redirect,url_for,request,flash,abort
from . import main
from ..models import User, Task
from .forms import LoginForm, SignUpForm, UpdateProfile, TaskForm
from .. import db,photos
from flask_login import login_required, current_user, login_user, logout_user
from ..email import mail_message
import datetime



@main.route('/signup', methods = ["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        mail_message("Welcome to Pomodoro","email/welcome_user",user.email,user=user)

        return redirect(url_for('main.home'))
    title = "New Account | Pomodoro"
    return render_template('signup.html', signup_form = form, title=title)

@main.route('/', methods = ["GET", "POST"])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(url_for('main.tasks', user_id=user.id))
        flash('Invalid username or password', 'danger')
    
    title = "Login | Pomodoro"
    return render_template('login.html', login_form = form, title=title)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))

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

@main.route('/tasks/<user_id>', methods=['GET', 'POST'])
@login_required
def tasks(user_id):
    user = User.query.filter_by(id = user_id).first()
    if user is None:
        abort(404)
    form=TaskForm()
    if form.validate_on_submit():
        title = form.task_title.data
        task_desc = form.task_description.data
        task_dur = form.task_duration.data
        break_desc = form.break_description.data
        break_dur = form.break_duration.data

        # Updated task instance
        this_task = Task(task_title=title, task_description=task_desc, task_duration=int(task_dur), break_description=break_desc, break_duration=int(break_dur), user=current_user)

        # save task method
        this_task.save_task()
        return redirect(url_for('.tasks',user_id=current_user.id))
        
    title = current_user.username + " | Tasks"
    task=Task.query.filter_by(user_id=user_id).order_by(Task.task_start_time.desc()).first()
    if task is not None:
        t=str(task.task_start_time)
        ts=t[11:16]
        task_endtime=datetime.datetime.strptime(ts, '%I:%M') + datetime.timedelta(minutes=task.task_duration)    
    
        return render_template('tasks.html',task=task, task_endtime=task_endtime, title=title, user=user, task_form=form)

    return render_template('tasks.html',title=title, user=user, task_form=form )

