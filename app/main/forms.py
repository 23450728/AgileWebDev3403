from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
import sqlalchemy as sa
from app.models import User
from flask_login import current_user
from app import db

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('This username is already taken.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('This email is already taken.')
        
class PostForm(FlaskForm):
    title = StringField('Your title', validators=[DataRequired(), Length(min=1, max=100)])
    post = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=3000)])
    file = FileField("Image")
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField("Your comment", validators=[DataRequired(), Length(min=1, max=3000)] )
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired(), Length(min=1)])
    submit = SubmitField('Search')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if ((user is not None) and (user.username != current_user.username)):
            raise ValidationError('This username is already taken.')
    
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if ((user is not None) and (user.email != current_user.email)):
            raise ValidationError('This email is already taken.')
    