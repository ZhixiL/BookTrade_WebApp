from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from inpforms import signinForm, signupForm
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

#SECRET_KEY = os.urandom(32)
#app.config['SECRET_KEY'] = SECRET_KEY


class Account(wadb.Model):  # This will be a model/table mappping within our wadb(web app database)
    __tablename__ = 'account'  # table name will generally be lower case
    # When Refer back to this table, use the lower case table name
    # Other table use this key to refer back to this table.
    id = wadb.Column(wadb.Integer, primary_key=True)
    firstname = wadb.Column(wadb.String(30), nullable=False)# (!nullable)name can't be empty
    lastname = wadb.Column(wadb.String(30), nullable=False)
    username = wadb.Column(wadb.String(30), nullable=False, unique=True)# unique because every user need their own username to login
    avatar = wadb.Column(wadb.String(30), default='///templates/images/default_avatar.jpg', nullable=False)
    password = wadb.Column(wadb.String(15), nullable=False)
    email = wadb.Column(wadb.String(100), nullable=False, unique=True)
    fsuid = wadb.Column(wadb.String(10), default='None', nullable=False)
    num_of_posts = wadb.Column(wadb.Integer, default=0, nullable=True) # number of posts by the unique user


class Post(wadb.Model):  # relation model with the model/table Account to let the user post listing on the site
    __tablename__ = 'post'
    id = wadb.Column(wadb.Integer, primary_key=True)
    creator = wadb.Column(wadb.Integer, wadb.ForeignKey('account.id'))# this will connect back to the account through account's
    header = wadb.Column(wadb.String(30), nullable=False)# User must input a Title of their post
    body = wadb.Column(wadb.String(100), nullable=True)# User is able to put a body to their post


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/msg', methods = ['POST', 'GET'])
def msg(): 
    if request.method == 'POST':
        try: 
            usr = request.form['username']
            pas = request.form['password']
            print(usr,pas)a
        except:
            msg = "Failed in signin due to some errors"
        finally:
            print(Account.query.filter(username=='zacklin'))
            return render_template("message.html", msg = msg)
    else:#This is the situation where user access /revrec directly without "submit" on /addrev page
        msg="Error, do not access this page directly!"
        return render_template("message.html", msg = msg)


if __name__ == '__main__':
    app.run(debug=True)
