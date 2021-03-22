from flask import Flask, render_template, url_for, flash, redirect, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from dataclasses import dataclass
# from marshmallow import Schema, fields
import datetime
import time
import os
import re
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
# Contribution: The name on each section on app.py is ordered by contribution: Most -> Least

app = Flask(__name__, static_folder='templates')
# linking with local SQLite3 database named webapp.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webapp.db'
# Allowing access from angular
CORS(app)
cors = CORS(app, resources={"/login": {"origins": "http://localhost:4200"}})
wadb = SQLAlchemy(app)  # Web app database, referencing

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Following are the code by Wesley, Yuki, Zhixi Lin (Zack)


@dataclass
class Post(wadb.Model):  # relation model with the model/table Account to let the user post listing on the site
    id: int
    time: str
    by: int
    bookname: str
    author: str
    price: float
    stat: str
    college: str
    picture: str
    description: str

    __tablename__ = 'post'
    id = wadb.Column(wadb.Integer, primary_key=True)
    time = wadb.Column(wadb.DateTime, nullable=False)
    # Keep track of time when listing are posted ^^
    by = wadb.Column(wadb.Integer, wadb.ForeignKey('account.username'))
    # this will connect back to the account through account's ^^
    bookname = wadb.Column(wadb.String(30), nullable=False)
    # User must input a Title of their post^^
    author = wadb.Column(wadb.String(30), nullable=False,
                         default="Author Not Specified")
    # Storing the author of the textbook^
    price = wadb.Column(wadb.Float, nullable=False, default=0)
    # User has to input the price of their listing with up to 2 decimals ^^
    stat = wadb.Column(wadb.String(30), nullable=False, default="New")
    # Status example: "New", "Some wear", "Teared pages", etc.^^
    college = wadb.Column(wadb.String(30), nullable=False)
    # User must state what college the book is belong to ^^
    picture = wadb.Column(wadb.String(
        30), default='../../assets/images/default_book.jpg', nullable=False)
    # Allows user to input an image, and has a default in case user does not input a picture ^^
    description = wadb.Column(wadb.String(100), nullable=True)
    # User is able to put a body to their post^^

    def __repr__(self):
        return 'Account({time},{by},{bookname},{price},{stat},{college},{picture},{description})'.format(
            time=self.time, by=self.by, bookname=self.bookname, price=self.price, stat=self.stat, college=self.college,
            picture=self.picture, description=self.description)
# End Wesley, Yuki, Zack


# class PostSchema(Schema):
#     author = fields.Str()
#     bookname = fields.Str()
#     by = fields.Str()
#     college = fields.Str()
#     description = fields.Str()
#     id = fields.Int()
#     picture = fields.Str()
#     price = fields.Int()
#     stat = fields.Str()
#     time = fields.Str()

# Following are the code by Zhixi Lin (Zack), Hanyan Zhang (Yuki)
@dataclass
class Account(wadb.Model):  # This will be a model/table mappping within our wadb(web app database)
    firstname: str
    lastname: str
    username: str
    avatar: str
    password: str
    email: str
    fsuid: str
    num_of_posts: int
    # book: Post

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
    # book = wadb.relationship(Post)

    def __repr__(self):  # Important, for when you cann the object, it returns tuple
        return 'Account({firstname},{lastname},{username},{avatar},{email},{fsuid})'.format(
            firstname=self.firstname, lastname=self.lastname, username=self.username,
            avatar=self.avatar, email=self.email, fsuid=self.fsuid)


@app.route("/signout")
def signout():
    session.pop('user', None)
    return redirect("/")


@app.route("/login", methods=['POST', 'GET'])
def login():
    form_data = request.get_json()
    userName = form_data["usern"]
    # passWord = form_data["pass"]
    return "userName+passWord"
    # if request.method == 'POST':  # Here's the POST request part
    #     try:  # this will make sure all the extraneous situation gets reported as failed
    #         usr = str(request.form['User'])
    #         pas = str(request.form['Pass'])
    #         temp = Account.query.filter_by(
    #             username=usr).first()  # search for user info
    #         if temp == None:  # this is the case where temp matches with no account
    #             flash('Username does not exist!')
    #         elif temp.password == pas:  # temp has matched an account, veryfing the password
    #             session['user'] = usr  # set up the session, keep track of user
    #         else:  # This is the case where password doesnt match the account
    #             flash('Wrong Password!')
    #     except:
    #         flash('Failed to sign in due to some errors')
    #     finally:
    #         if 'user' in session:  # This is the case where user successfully signed in.
    #             return redirect("/")
    #         else:  # This is the case where user failed to sign in
    #             return render_template('login.html')
    # else:  # here's the GET request part
    #     if 'user' in session:  # user already signed in
    #         return redirect(url_for('index'))
    #     else:  # user didn't signed in
    #         return render_template('login.html')


@app.route('/msg', methods=['POST', 'GET'])
def msg():
    return render_template("message.html", msg="placeholder")


@app.route('/usernamedata', methods=['GET'])
def usernamedata():
    username = str()
    if 'user' in session:  # Ensure the user's full name is send to post.html
        username = Account.query.filter_by(username=session['user']).first(
        ).firstname + ' ' + Account.query.filter_by(username=session['user']).first().lastname
    else:
        username = 'offline'
    jsUser = {
        "usernamedata": [{
            "username": username
        }]
    }
    return jsonify([jsUser])


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # if 'user' in session:
    userlist = Account.query.filter_by(username="zacklin").first()
    jsonDataUser = {
        "userdata": [
            userlist
        ]
    }

    return jsonify([jsonDataUser])
    # else:
    #     return "not found"


@app.route('/profilebook', methods=['GET', 'POST'])
def profileBook():
    tbooklist = Post.query.filter_by(
        by="zacklin").order_by(Post.time).limit(8).all()
    jsonDataBook = {
        "bookdata": tbooklist
    }
    return jsonify([jsonDataBook])

# removing later
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

    else:  # This is the case for search
        key = str(request.form['keywords'])
        bklist = list(Post.query.filter(
            Post.bookname.contains(key)).order_by(Post.time).limit(12))
        if not bklist:  # This is the case for nothing found
            flash('Nothing was found!')
            return render_template('booklist.html', user=user, booktitle="none", bklist=bklist)
        else:
            return render_template("booklist.html", user=user, booktitle="none", bklist=bklist)


@app.route('/booklistbrief', methods=['GET'])
def booklistbrief():
    bklist = Post.query.order_by(Post.time.desc()).limit(
        12).all()  # 12 most recently posted books
    jsonData = {
        "bookdata": bklist
    }
    return jsonify([jsonData])


@app.route('/booklistall', methods=['GET'])
def booklistall():
    bklist = Post.query.order_by(Post.time.desc()).all()
    # get all books
    jsonData = {
        "bookdata": bklist
    }
    return jsonify([jsonData])

# removing later
@app.route('/bookdetail', methods=['POST', 'GET'])
def bookdetail():
    if 'user' in session:
        user = Account.query.filter_by(username=session['user']).first(
        ).firstname + ' ' + Account.query.filter_by(username=session['user']).first().lastname
    else:
        user = 'offline'
    if request.method == 'GET':
        return render_template(listdetail.html, user=user)
        # return redirect(url_for('index')) #This page is not allowed to be accessed directly
    else:  # post request
        pass

# removing this route later
@app.route("/", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    if 'user' in session:  # Ensure the user's full name is send to post.html
        user = Account.query.filter_by(username=session['user']).first(
        ).firstname + ' ' + Account.query.filter_by(username=session['user']).first().lastname
    else:
        user = 'offline'

    bklist = Post.query.order_by(Post.time).limit(
        12).all()  # 12 most recently posted books
    # post_schema = PostSchema()
    # post_schema.dump(bklist)
    jsonData = {
        "bookdata": bklist
    }
    # return render_template("index.html", user=user, booktitle="none", bklist=bklist)
    return jsonify([jsonData])
# End Yuki & Zack


# Following are the code by Zhixi Lin, Wesley White, Yuanyuan Bao
@app.route("/post", methods=['POST', 'GET'])
def post():
    if 'user' in session:
        user = Account.query.filter_by(username=session['user']).first(
        ).firstname + ' ' + Account.query.filter_by(username=session['user']).first().lastname
    else:
        flash('Please Sign in Before Posting!')
        return redirect(url_for('login'))
        # User are not allowed to enter new post without signed in.

    if request.method == 'GET':
        return render_template('post.html', user=user)
    else:  # Separation of post & get
        post_by = session['user']
        bkname = request.form.get('BookName')
        aut = request.form.get('Author')
        # ensure pricing is precisely round to 2 decimal place.
        post_price = round(float(request.form.get('Price')), 2)
        stat = request.form.get('status')
        coll = request.form.get('college')
        ava = request.form.get('file')
        descrip = request.form.get('description')

        flag = True  # Simple validation mechanism

        # Basically loop every single char in book title to check if character is contained
        if not any(namechar.isalpha() for namechar in bkname):
            flash("Book title with no letter is not allowed!")
            flag = False
        if not any(autchar.isalpha() for autchar in aut):
            flash("Author name with no letter is not allowed!")
            flag = False
        if flag == True:
            try:
                post = Post(by=post_by, bookname=bkname, author=aut, price=post_price, stat=stat,
                            college=coll, description=descrip, time=datetime.datetime.now())
                if ava != None:  # We haven't developed picture uploading function
                    post.avatar = ava
                if descrip != None:
                    post.description = descrip
                wadb.session.add(post)
                wadb.session.commit()
                flash("Successfully uploaded!")
            except:
                flash("An Exception has occured!")
        return render_template('post.html', user=user)
# End Zhixi Lin, Yuanyuan, Wesley


# Following are the code by Dennis Majanos, Hanyan Zhang (Yuki), Zhixi Lin (Zack)
@app.route('/createAccPage', methods=['POST', 'GET'])
def createAcc():
    if request.method == 'GET':
        return render_template("createAccount.html")
    if request.method == 'POST':
        # this variable determines if we can update the database or recollect
        # data
        updateDatabase = False

        # getting info from webpage for creating an account
        user = str(request.form['username'])
        pwd = str(request.form['pwd1'])
        conf_pwd = str(request.form['pwd2'])
        firstName = str(request.form['firstName'])
        lastName = str(request.form['lastName'])
        mail = str(request.form['emailAddress'])
        FSUid = str(request.form['fsuId'])

        updateDatabase = True

        # Validation of the user input:
        # If filter returns a result, it means the user or email already exist
        if bool(Account.query.filter_by(username=user).all()):
            flash("Username already exsists")
            updateDatabase = False
        if bool(Account.query.filter_by(email=mail).all()):
            flash("Email already exsists")
            updateDatabase = False
        if pwd != conf_pwd:
            flash("Password and confirm password doesn't match!")
            updateDatabase = False

        if (len(firstName) > 30 or len(firstName) == 0):
            flash("FirstName must be between 1 and 30 characters long")
            updateDatabase = False
        if (len(lastName) > 30 or len(lastName) == 0):
            flash("LastName must be between 1 and 30 characters long")
            updateDatabase = False
        if (len(user) > 30 or len(user) == 0):
            flash("Username must be between 1 and 30 characters long")
            updateDatabase = False
        if (len(pwd) > 15 or len(pwd) == 0):
            flash("Password must be between 1 and 15 characters long")
            updateDatabase = False
        if (len(mail) > 100 or len(mail) == 0):
            flash("Email must be between 1 and 100 characters long")
            updateDatabase = False
        if (len(FSUid) > 10 or len(FSUid) == 0):
            flash("Fsuid must be between 1 and 10 characters long")
            updateDatabase = False

        userInput = (firstName, lastName, user, pwd, mail, FSUid)
        if updateDatabase == True:
            try:
                # add variable input into the database
                # if wadb.session.query(Account).filter_by(email=mail).count() < 1:
                userinfo = Account(firstname=firstName, lastname=lastName, username=user,
                                   password=pwd, email=mail, fsuid=FSUid)
                wadb.session.add(userinfo)
                wadb.session.commit()
                # Ensure the account can be found on database, so there's nothing wrong with input to database.
                session['user'] = str(Account.query.filter_by(
                    username=user).first().username)
                return redirect("/")
            except:
                # flash alert message and stay on register page
                flash("An Exception has occurred!")
                return render_template("createAccount.html", inp=userInput)
            # finally:
            #     if updateDatabase == True:
            #         return redirect("/")
            #     elif updateDatabase == False:
            #         return render_template("createAccount.html", inp = userInput)
        else:  # if invalid data is entered, allow users to enter again
            return render_template("createAccount.html", inp=userInput)
# End Dennis, Yuki, Zack


if __name__ == '__main__':
    app.run(debug=True)
