from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from inpforms import signinForm, signupForm

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

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webapp.db'#linking with local SQLite3 database named webapp.db
wadb = SQLAlchemy(app) #Web app database, referencing 

class Account(wadb.Model): #This will be a model/table mappping within our wadb(web app database)
    __tablename__ = 'account' #table name will generally be lower case
    #When Refer back to this table, use the lower case table name
    id = wadb.Column(wadb.Integer, primary_key=True) #Other table use this key to refer back to this table.
    firstname = wadb.Column(wadb.String(30), nullable=False)#(!nullable)name can't be empty
    lastname = wadb.Column(wadb.String(30), nullable=False)
    username = wadb.Column(wadb.String(30), nullable=False, unique=True) #unique because every user need their own username to login
    avatar = wadb.Column(wadb.String(30),default='///templates/images/default_avatar.jpg',nullable=False)
    password = wadb.Column(wadb.String(15),nullable=False)
    email = wadb.Column(wadb.String(100), nullable=False, unique=True)
    num_of_posts = wadb.Column(wadb.Integer, default=0, nullable=True) #number of posts by the unique user,

class Post(Account, wadb.Model): #derived model from the model/table Account to let the user post listing on the site
        __tablename__ =  'post'
        header = wadb.Column(wadb.String(30), nullable=False) # User must input a Title of their post
        body = wadb.Column(wadb.String(100), nullable=True) # User is able to put a body to their post

if __name__ == '__main__':
    app.run(debug=True)
