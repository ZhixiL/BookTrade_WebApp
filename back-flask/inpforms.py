'''
This folder utilizes the API WTForms to create forms for gatering
input from user, specifically for Account & Posts, and validate them.
Specifically the validators will be used here, to ensure the entered
info is correctly formatted.
Followed are the references if needed:
https://wtforms.readthedocs.io/en/2.3.x/validators/#built-in-validators
https://flask-wtf.readthedocs.io/en/stable/

DataRequried() checks for that there need to be something entered
Email() check for correctly formatted email input
Length(min, max) specify the allowed length of input
EqualTo() checks if input is equal to given value
-- comment & code by Zhixi Lin --
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class signupForm(FlaskForm):
    firstname = StringField('FirstName', validators=[DataRequired(), Length(min=1,max=30)])
    lastname = StringField('LastName', validators=[DataRequired(), Length(min=1,max=30)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5,max=15)])
    #Can add password requirement that forces use of num & letter later
    password_again = PasswordField('Enter Password Again', validators=[EqualTo('password')])
    #ensure password is entered correctly
    fsuid = StringField('FSUID', validators=[DataRequired(), Length(max=10)]) #This will also served as email, by appending @my.fsu.edu
    signup = SubmitField('Sign up')

class signinForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5,max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5,max=15)])
    #keeplogin = BooleanField() can be added later for "Remembre for 30 days" Feature
    signin = SubmitField('Sign in')