from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError,BooleanField,TextAreaField, SelectField
from wtforms.validators import Required,Email,EqualTo,Length,NumberRange
from ..models import User
from email_validator import validate_email, EmailNotValidError

class SignUpForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    username = StringField('Enter your username',validators = [Required(),Length(min=2,max=20)])
    password = PasswordField('Password',validators = [Required()])
    password_confirm = PasswordField('Confirm Passwords',validators = [Required(), EqualTo('password',message = 'Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
            if User.query.filter_by(email =data_field.data).first():
                raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')

class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    password = PasswordField('Password',validators =[Required()])
    remember = BooleanField('Remember Me') #confirms if user wants to be logged out after session
    submit = SubmitField('Sign In')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class TaskForm(FlaskForm):
    task_title = StringField("Task Title", validators = [Required()])
    task_description=TextAreaField('Task Description', validators=[Required()],render_kw={'class': 'form-control', 'rows': 6})
    task_duration=SelectField("Task Duration", choices=[('10', "10 mins"), ('20', "20 mins"), ('30', "30 mins"), ('40', "40 mins"), ('50', "50 mins"),('60', "60 mins")],validators=[Required()])
    break_description=TextAreaField('Break Description', validators=[Required()],render_kw={'class': 'form-control', 'rows': 3})
    break_duration=SelectField("Break Duration", choices=[('5', "5 mins"), ('6', "6 mins"), ('7', "7 mins"), ('8', "8 mins"), ('9', "9 mins"),('10', "10 mins")],validators=[Required()])
    submit = SubmitField('Create task')


