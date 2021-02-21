from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
# from inpforms import signinForm, signupForm #This API has been abandoned
import datetime
import time
import os
'''
--- DATABASE EXPLAIN ---
The models below will be declared using SQLAlchemy ORM
and utilizes SQlite3(Temporary, can be updated) as local
database to store info for Account & Book Post.
Object Relation Tutorial for SQLAlchemy: https://docs.sqlalchemy.org/en/13/orm/tutorial.html
Flask-SQLAlchemy reference:https://flask-sqlalchemy.palletsprojects.com/en/2.x/
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
    # (!nullable)name can't be empty
    firstname = wadb.Column(wadb.String(30), nullable=False)
    lastname = wadb.Column(wadb.String(30), nullable=False)
    # unique because every user need their own username to login
    username = wadb.Column(wadb.String(30), nullable=False,
                           unique=True, primary_key=True)
    # The username will also served as the primary key for other table to reference back.
    avatar = wadb.Column(wadb.String(
        30), default='///templates/images/default_avatar.jpg', nullable=False)
    password = wadb.Column(wadb.String(15), nullable=False)
    email = wadb.Column(wadb.String(100), nullable=False, unique=True)
    fsuid = wadb.Column(wadb.String(10), default='None', nullable=False)
    # number of posts by the unique user
    num_of_posts = wadb.Column(wadb.Integer, default=0, nullable=True)

    def __repr__(self):  # Important, for when you cann the object, it returns tuple
        return 'Account({firstname},{lastname},{username},{avatar},{email},{fsuid})'.format(
            firstname=self.firstname, lastname=self.lastname, username=self.username,
            avatar=self.avatar, email=self.email, fsuid=self.fsuid)


class Post(wadb.Model):  # relation model with the model/table Account to let the user post listing on the site
    __tablename__ = 'post'
    id = wadb.Column(wadb.Integer, primary_key=True)
    time = wadb.Column(wadb.DateTime, nullable=False)
    # Keep track of time when listing are posted ^^
    by = wadb.Column(wadb.Integer, wadb.ForeignKey('account.username'))
    # this will connect back to the account through account's ^^
    bookname = wadb.Column(wadb.String(30), nullable=False)
    # User must input a Title of their post^^
    price = wadb.Column(wadb.Float, nullable=False, default=0)
    # User has to input the price of their listing with up to 2 decimals ^^
    stat = wadb.Column(wadb.String(30), nullable=False, default="New")
    # Status example: "New", "Some wear", "Teared pages", etc.^^
    college = wadb.Column(wadb.String(30), nullable=False)
    # User must state what college the book is belong to ^^
    picture = wadb.Column(wadb.String(
        30), default='///templates/images/default_book.jpg', nullable=False)
    # Allows user to input an image, and has a default in case user does not input a picture ^^
    description = wadb.Column(wadb.String(100), nullable=True)
    # User is able to put a body to their post^^
    # Assumption that body is the same as description in post.html

    def __repr__(self):
        return 'Account({time},{by},{bookname},{price},{stat},{college},{picture},{description})'.format(
            time=self.time, by=self.by, bookname=self.bookname, price=self.price, stat=self.stat, college=self.college,
            picture=self.picture, description=self.description)


@app.route("/", methods=['POST', 'GET'])
@app.route("/index", methods=['POST', 'GET'])
def index():
    if 'user' in session:  # Ensure the user's full name is send to post.html
        user = Account.query.filter_by(username=session['user']).first(
        ).firstname + ' ' + Account.query.filter_by(username=session['user']).first().lastname
    else:
        user = 'offline'

    if request.method == 'GET':
        bklist = Post.query.order_by(Post.time).limit(
            12).all()  # 12 most recently posted books
        return render_template("index.html", user=user, booktitle="none", bklist=bklist)
    else:  # this is POST request, from search.
        key = str(request.form['keywords'])
        bklist = Post.query.filter(
            Post.bookname.contains(key)).order_by(Post.time).all()
        if not bklist:  # This is the case for nothing found
            return redirect(url_for('index'))
        else:
            return render_template("index.html", user=user, booktitle="none", bklist=bklist)


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
            temp = Account.query.filter_by(
                username=usr).first()  # search for user info
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
    if 'user' in session:
        user = Account.query.filter_by(username=session['user']).first(
        ).firstname + ' ' + Account.query.filter_by(username=session['user']).first().lastname
    else:
        user = 'offline'
    name_of_book = request.form.get('Book Name')
    post_price = request.form.get('Price')
    status = request.form.get('Status')
    category = request.form.get('Category')
    picture = request.form.get('file')
    return render_template('post.html', user=user)


@app.route('/msg', methods=['POST', 'GET'])
def msg():
    return render_template("message.html", msg="placeholder")


@app.route('/booklist', methods=['GET', 'POST'])
def booklist():
    if 'user' in session:
        user = Account.query.filter_by(username=session['user']).first(
        ).firstname + ' ' + Account.query.filter_by(username=session['user']).first().lastname
    else:
        user = 'offline'

    if request.method == 'GET':
        # in default order by post time
        bklist = Post.query.order_by(Post.time).all()
        return render_template("booklist.html", user=user, booktitle="none", bklist=bklist)

    else:  # this is POST request, from search.
        key = str(request.form['keywords'])
        bklist = Post.query.filter(
            Post.bookname.contains(key)).order_by(Post.time).all()
        if not bklist:  # This is the case for nothing found
            return redirect(url_for('index'))
        else:
            return render_template("booklist.html", user=user, booktitle="none", bklist=bklist)


@app.route('/createAccPage')
def createAccPage():
    return render_template("createAccount.html")


@app.route('/createAcc', methods=['POST', 'GET'])
def createAcc():
    if request.method == 'POST':
        try:
            username = request.form['username']
            pwd = request.form['pwd1']
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            email = request.form['emailAddress']
            fsuid = request.form['fsuId']
        except:
            # rollback if data go through to database
            i = 1  # dummy variable
        finally:
            return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
