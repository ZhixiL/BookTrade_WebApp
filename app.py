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

#Following are the code by Wesley & Zhixi Lin (Zack)
class Post(wadb.Model):  # relation model with the model/table Account to let the user post listing on the site
    __tablename__ = 'post'
    id = wadb.Column(wadb.Integer, primary_key=True)
    time = wadb.Column(wadb.DateTime, nullable=False)
    # Keep track of time when listing are posted ^^
    by = wadb.Column(wadb.Integer, wadb.ForeignKey('account.username'))
    # this will connect back to the account through account's ^^
    bookname = wadb.Column(wadb.String(30), nullable=False)
    # User must input a Title of their post^^
    author = wadb.Column(wadb.String(30), nullable=False, default = "Author Not Specified")
    # Storing the author of the textbook^
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
#End Wesley & Zack

#Following are the code by Zhixi Lin (Zack)
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

    else:  #This is the case for search
        key = str(request.form['keywords'])
        bklist = list(Post.query.filter(Post.bookname.contains(key)).order_by(Post.time).limit(12))
        if not bklist:  # This is the case for nothing found
            flash('Nothing was found!')
            return render_template('booklist.html', user=user, booktitle="none", bklist=bklist)
        else:
            return render_template("booklist.html", user=user, booktitle="none", bklist=bklist)

@app.route('/bookdetail', methods=['POST', 'GET']) #Still developing, postponed to iteration 2
def bookdetail():
    if 'user' in session:
        user = Account.query.filter_by(username=session['user']).first(
        ).firstname + ' ' + Account.query.filter_by(username=session['user']).first().lastname
    else:
        user = 'offline'
    if request.method == 'GET':
        return render_template(listdetail.html, user=user)
        #return redirect(url_for('index')) #This page is not allowed to be accessed directly
    else: #post request
        pass
#End Zack


#following are the code by Hanyan Zhang (Yuki), Zhixi Lin (Zack)
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
    return render_template("index.html", user=user, booktitle="none", bklist=bklist)
#End Yuki & Zack


#Following are the code by Yuanyuan Bao, Wesley White, Zhixi Lin
@app.route("/post", methods=['POST', 'GET'])
def post():
    if 'user' in session:
        user = Account.query.filter_by(username=session['user']).first(
        ).firstname + ' ' + Account.query.filter_by(username=session['user']).first().lastname
    else:
        flash('Please Sign in Before Posting!')
        return render_template('login.html')
        #User are not allowed to enter new post without signed in.

    if request.method == 'GET':
        return render_template('post.html', user=user)
    else: #Separation of post & get
        post_by = session['user']
        name_of_book = request.form.get('BookName')
        post_price = float(round(request.form.get('Price'),2)) #ensure pricing is precisely round to 2 decimal place.
        status = request.form.get('status')
        category = request.form.get('category')
        picture = request.form.get('file')
        return render_template('post.html', user=user)
#End Yuanyuan, Wesley, Zhixi Lin


#Following are the code by Dennis Majanos, Wesley White
@app.route('/createAccPage', methods=['POST', 'GET'])
def createAcc():
    if request.method == 'GET':
        return render_template("createAccount.html")
    if request.method == 'POST':
        #this variable determines if we can update the database or recollect
        #data
        updateDatabase = False

        #getting info from webpage for creating an account
        user = str(request.form['username'])
        pwd = str(request.form['pwd1'])
        firstName = str(request.form['firstName'])
        lastName = str(request.form['lastName'])
        mail = str(request.form['emailAddress'])
        fsuid = str(request.form['fsuId'])
         
        #checking if username already exsists
        condition1 = Account.query.filter_by(username = user)
        #checking if email already exsists
        condition2 = Account.query.filter_by(email = mail)
        
        #validating all the user input
        if (len(firstName) > 30 or len(firstName) == 0):
            flash("FirstName must be between 0 and 30 characters long")
            updateDatabase = False
        elif (len(lastName) > 30 or len(lastName) == 0):
            flash("LastName must be between 0 and 30 characters long")
            updateDatabase = False
        elif (len(user) > 30 or len(user) == 0):
            flash("Username must be between 0 and 30 characters long")
            updateDatabase = False
        elif (len(pwd) > 15 or len(pwd) == 0):
            flash("Password must be between 0 and 15 characters long")
            updateDatabase = False
        elif (len(mail) > 100 or len(mail) == 0):
            flash("Email must be between 0 and 100 characters long")
            updateDatabase = False
        elif (len(fsuid) > 10 or len(fsuid) == 0):
            flash("Fsuid must be between 0 and 10 characters long")
            updateDatabase = False
        elif condition1 != None:
            flash("Username already exsists")
            updateDatabase = False
        elif condition2 != None:
            flash("Email already exsists")
            updateDatabase = False
        else:
            updateDatabase = True 
        
        userInput = (firstName, lastName, user, pwd, mail, fsuid)
        
        try:
            #if updateDatabase == true:
                #add variable input into the database
            k = 1 # dummy variable, can remove after implementation
        except:
            # rollback if data go through to database
            i = 1  # dummy variable, can remove after implementing rollback
        finally:
            if updateDatabase == True:
                return redirect("/")
            elif updateDatabase == False:
                return render_template("createAccount.html", inp = userInput)
#End Dennis, Wesley

if __name__ == '__main__':
    app.run(debug=True)
