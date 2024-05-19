from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo, Email

class ResetPasswordForm(FlaskForm):
    password = PasswordField(('Password'), validators=[DataRequired()])
    password2 = PasswordField(('Repeat Password'), validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField(('Request Password Reset'))

class ResetPasswordRequestForm(FlaskForm):
    #Credit goes to MiguelGrinberg chapter 10: email server
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

##Refer to https://github.com/miguelgrinberg/microblog/tree/v0.15/app/auth