from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('rememberme', default=False)


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                           Email()])
    username = StringField('username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[\u4e00-\u9fa5]|[a-z]|[A-Z][0-9_.]*', 0,
                                          'Username must start with charater or letter!')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Password does not match!')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email address is already taken!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already taken!')

# Change password form
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Password does not match!')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
