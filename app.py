from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
#from inpforms import signinForm, signupForm #This API has been abandoned
import datetime
import time
import os
'''
--- DATABASE EXPLAIN ---
The models below will be declared using SQLAlchemy ORM
and utilizes SQlite3(Temporary, can be updated) as local
database to store info for Account & Book Post.
Object Relation Tutorial for SQLAlchemy: https://docs.sqlalchemy.org/en/13/orm/tutorial.html
More Reference avaliable on above link.
*Since we're using sqlite3, when declaring model with attribute String, specify the size.
--- comment by Zhixi Lin ---
'''

app = Flask(__name__, static_folder='templates')
# linking with local SQLite3 database named webapp.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webapp.db'
wadb = SQLAlchemy(app)  # Web app database, referencing

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class Account(wadb.Model):  # This will be a model/table mappping within our wadb(web app database)
    __tablename__ = 'account'  # table name will generally be lower case
    # When Refer back to this table, use the lower case table name
    # Other table use this key to refer back to this table.
    id = wadb.Column(wadb.Integer, primary_key=True)
    # (!nullable)name can't be empty
    firstname = wadb.Column(wadb.String(30), nullable=False)
    lastname = wadb.Column(wadb.String(30), nullable=False)
    # unique because every user need their own username to login
    username = wadb.Column(wadb.String(30), nullable=False, unique=True)
    avatar = wadb.Column(wadb.String(
        30), default='///templates/images/default_avatar.jpg', nullable=False)
    password = wadb.Column(wadb.String(15), nullable=False)
    email = wadb.Column(wadb.String(100), nullable=False, unique=True)
    fsuid = wadb.Column(wadb.String(10), default='None', nullable=False)
    # number of posts by the unique user
    num_of_posts = wadb.Column(wadb.Integer, default=0, nullable=True)


class Post(wadb.Model):  # relation model with the model/table Account to let the user post listing on the site
    __tablename__ = 'post'
    id = wadb.Column(wadb.Integer, primary_key=True)
    time = wadb.Column(wadb.Date, nullable=False) 
    #Keep track of time when listing are posted ^^
    creator = wadb.Column(wadb.Integer, wadb.ForeignKey('account.id'))
    # this will connect back to the account through account's ^^
    bookname = wadb.Column(wadb.String(30), nullable=False)
    # User must input a Title of their post^^
    price = wadb.Column(wadb.Float, nullable=False, default = 0)
    # User has to input the price of their listing with up to 2 decimals ^^
    stat = wadb.Column(wadb.String(30), nullable=False, default = "New")
    # Status example: "New", "Some wear", "Teared pages", etc.^^
    category = wadb.Column(wadb.String(30), nullable=False)
    # User must state what category the book is in to better situate the listing ^^
    picture = wadb.Column(wadb.String(30), default='///templates/images/default_book.jpg', nullable=False)
    # Allows user to input an image, and has a default in case user does not input a picture ^^
    description = wadb.Column(wadb.String(100), nullable=True)
    # User is able to put a body to their post^^
    # Assumption that body is the same as description in post.html


@app.route("/")
@app.route("/index")
def index():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    else:
        return render_template('index.html', user='offline')


@app.route("/signout")
def signout():
    session.pop('user', None)
    return redirect("/")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':  # Here's the POST request part
        try:  # this will make sure all the extraneous situation gets reported as failed
            usr = str(request.form['User'])
            pas = str(request.form['Pass'])
            temp = Account.query.filter_by(username=usr).first()  # search for user info
            if temp == None:  # this is the case where temp matches with no account
                flash('Username does not exist!')
            elif temp.password == pas:  # temp has matched an account, veryfing the password
                session['user'] = usr  # set up the session, keep track of user
                flash('Sign in successful!')
            else:  # This is the case where password doesnt match the account
                flash('Wrong Password!')
        except:
            flash('Failed to sign in due to some errors')
        finally:
            if 'user' in session:  # This is the case where user successfully signed in.
                return redirect("/")
            else:  # This is the case where user failed to sign in
                return render_template('login.html')
    else:  # here's the GET request part
        if 'user' in session:  # user already signed in
            return redirect(url_for('index'))
        else:  # user didn't signed in
            return render_template('login.html')


@app.route("/post", methods=['POST', 'GET'])
def post():
    name_of_book = request.form.get('Book Name')
    post_price = request.form.get('Price')
    status = request.form.get('Status')
    category = request.form.get('Category')
    picture = request.form.get('file')
    return render_template('post.html')


@app.route('/msg', methods=['POST', 'GET'])
def msg():
    return render_template("message.html", msg="placeholder")


@app.route('/booklist', methods=['GET'])
def booklist():
    if 'user' in session:
        user = session['user']
    else:
        user = 'offline
    return render_template("booklist.html", user = user, booktitle="none")

if __name__ == '__main__':
    app.run(debug=True)
