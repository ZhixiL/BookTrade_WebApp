from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from dataclasses import dataclass
from werkzeug.utils import secure_filename
# from marshmallow import Schema, fields
import datetime
import time
import os
import re
import sys
import jwt
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
app.config['UPLOAD_FOLDER'] = "../front-angular/src/assets/images"
CORS(app)  # Allowing access from angular
cors = CORS(app, resources={"/login": {"origins": "http://localhost:4200"}})
wadb = SQLAlchemy(app)  # Web app database, referencing
wadb.init_app(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


# Following are the code by Yuki, Wesley, Zhixi Lin (Zack)~``
# relation model with the model/table Account to let the user post listing on the site
### MODELS ###
@dataclass
class Post(wadb.Model):
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
# End Yuki, Wesley, Zack

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

    __tablename__ = 'account'  # table name will generally be lower case
    # When Refer back to this table, use the lower case table name
    # (!nullable)name can't be empty
    id = wadb.Column(wadb.Integer, primary_key=True)
    firstname = wadb.Column(wadb.String(30), nullable=False)
    lastname = wadb.Column(wadb.String(30), nullable=False)
    username = wadb.Column(wadb.String(30), nullable=False, unique=True)
    avatar = wadb.Column(wadb.String(
        30), default='///templates/images/default_avatar.jpg', nullable=False)
    password = wadb.Column(wadb.String(15), nullable=False)
    email = wadb.Column(wadb.String(100), nullable=False, unique=True)
    fsuid = wadb.Column(wadb.String(10), default='None', nullable=False)
    num_of_posts = wadb.Column(wadb.Integer, default=0, nullable=True)

    def encode_auth_token(self, user_id, keeplog=False):
        try:
            hour = int()
            if keeplog is True:
                hour = 360
            else:  # if the user explicitly said want to stay logged on,
                # token will last for 30 days or 360 hours
                hour = 12  # else only 12 hours for the current session.
            print(hour, file=sys.stderr)
            payload = {
                # expiration date of the token
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=hour, seconds=5),
                # when is token generated
                'iat': datetime.datetime.utcnow(),
                # the user that token identifies
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, app.config.get(
                'SECRET_KEY'), algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):  # Important, for when you cann the object, it returns tupleap
        return 'Account({firstname},{lastname},{username},{avatar},{email},{fsuid})'.format(
            firstname=self.firstname, lastname=self.lastname, username=self.username,
            avatar=self.avatar, email=self.email, fsuid=self.fsuid)

#The following is a test model based off post class
#We want to differentiate the Buy Order List data 
@dataclass
class Buyorder(wadb.Model):
    id: int
    time: str
    by: int
    bookname: str
    author: str
    price: float
    stat: str
    college: str

    __tablename__ = 'buyorder'
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

    def __repr__(self):
        return 'Account({time},{by},{bookname},{price},{stat},{college})'.format(
            time=self.time, by=self.by, bookname=self.bookname, price=self.price, stat=self.stat, college=self.college)
    
    
class BlacklistToken(wadb.Model):  # Stores JWT tokens
    __tablename__ = 'blacklist_tokens'
    id = wadb.Column(wadb.Integer, primary_key=True, autoincrement=True)
    token = wadb.Column(wadb.String(500), unique=True, nullable=False)
    blacklisted_on = wadb.Column(wadb.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return 'BlacklistToken({token})'.format(token=self.token)

    @staticmethod
    def check_blacklist(token):
        res = BlacklistToken.query.filter_by(token=str(token)).first()
        if res:
            return True
        else:
            return False


### ROUTE CONTROLLERS ###
@app.route("/getAccount", methods=['POST'])
def getAccount():
    form_data = request.get_json(force=True)
    if form_data['token'] is None or BlacklistToken.check_blacklist(form_data['token']):
        # clientside doesn't have a token or token is blacklisted
        response = {
            'status': 'fail',
            'username': 'offline',
            'pic': 'none'
        }
        return response
    accID = Account.decode_auth_token(form_data['token'])
    # print(accID, file=sys.stderr)
    if str(type(accID)) == "<class 'int'>":  # successful retrived id
        user = Account.query.filter_by(id=accID).first()
        response = {
            'status': 'success',
            'username': user.firstname + " " + user.lastname,
            'usern': user.username,
            'pic': user.avatar
        }
        print(user.avatar)
        return response
    else:
        response = {
            'status': 'expired',
            'username': 'offline',
            'pic': 'none'
        }
        return response


@app.route("/signout", methods=['POST'])
def signout():
    form_data = request.get_json(force=True)
    userID = Account.decode_auth_token(form_data['token'])
    if str(type(userID)) == "<class 'int'>":
        blacklist_token = BlacklistToken(token=form_data['token'])
        try:
            wadb.session.add(blacklist_token)
            wadb.session.commit()
            response = {
                'status': 'success',
                'msg': 'Successfully logged out!'
            }
            return jsonify(response)
        except Exception as e:
            response = {
                'status': 'fail',
                'msg': e
            }
            return jsonify(response)
    else:
        response = {
            'status': 'fail',
            'msg': "Session expired, you're not logged in."
        }
        return jsonify(response)


@app.route("/login", methods=['POST', 'GET'])
@cross_origin()
def login():
    if request.method == 'POST':
        form_data = request.get_json(force=True)
        msg = ""
        usr = str(form_data['usern'])
        pas = str(form_data['pass'])
        keeplog = form_data['keeplog']
        temp = Account.query.filter_by(username=usr).first()
        # if form_data['token'] != "nodata":
        #     print(Account.decode_auth_token(form_data['token']), file=sys.stderr)
        if temp == None:  # this is the case where temp matches with no account
            msg = 'Username does not exist!'
        elif temp.password == pas:  # temp has matched an account, veryfing the password
            authToken = temp.encode_auth_token(temp.id, keeplog)
            if authToken:  # ensure authentication token is correctly generated
                response = jsonify({
                    'status': 'success',
                    'msg': 'Successfully logged in.',
                    'auth_token': authToken
                })
                return response  # can switch over to make response later
        else:  # This is the case where password doesnt match the account
            msg = 'Wrong Password!'
        response = jsonify({
            'status': 'fail',
            'msg': msg
        })
        return response
    else:
        return "hello"


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    usrn = ""
    if request.method == 'POST':
        form_data = request.get_json(force=True)
        usrn = str(form_data["usr"])
    print(usrn)
    userlist = Account.query.filter_by(username=usrn).first()
    jsonDataUser = {
        "userdata": [
            userlist
        ]
    }
    return jsonify([jsonDataUser])

@app.route("/changepass", methods=['POST', 'GET'])
@cross_origin()
def changepass():
    if request.method == 'POST':
        form_data = request.get_json(force=True)
        msg = ""
        oldpass = str(form_data['oldp'])
        usern = str(form_data['user'])
        correct = Account.query.filter_by(username=usern).first()
        pass1 = str(form_data['p1'])
        pass2 = str(form_data['p2'])
        print(oldpass, pass1, pass2, usern)

        if correct == None:
            msg = "Your session ended. Please login again."
        elif correct.password != oldpass:
            msg = "Wrong Password. Try Again."
        else:
            if pass1 != pass2:
                msg = "Passwords you entered does not match!"
            else:
                try:
                    correct.password = pass1
                    wadb.session.commit()
                    msg = "Your password is changed!"
                except:
                    msg = "Error changing password!"
        response = jsonify({
            'msg': msg
        })
        return response
    else:
        return "placeholder"


@app.route('/changeava', methods=['POST'])
def changeava():
    form_data = request.get_json(force=True)
    msg = ""
    userid = Account.decode_auth_token(form_data['token'])
    user = Account.query.filter_by(id=userid).first()
    if user == None:
        msg = "Invalid user! Avatar change failed."
    else:
        try:
            user.avatar = form_data['ava']
            wadb.session.commit()
            msg = "Your avatar is changed!"
        except:
            msg = "Some error occured!"
    response = jsonify({
        'msg': msg
    })
    return response

@app.route('/profilebook', methods=['GET', 'POST'])
def profileBook():
    tbooklist = Post.query.filter_by(
        by="zacklin").order_by(Post.time).limit(8).all()
    jsonDataBook = {
        "bookdata": tbooklist
    }
    return jsonify([jsonDataBook])


@app.route('/booklistbrief', methods=['GET'])
def booklistbrief():
    bklist = Post.query.order_by(Post.time.desc()).limit(
        12).all()  # 12 most recently posted books
    jsonData = {
        "bookdata": bklist
    }
    return jsonify([jsonData])


@app.route('/userdataall', methods=['GET'])
def userlistall():
    bklist = Account.query.all()
    # get all users
    jsonData = {
        "userdata": bklist
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


# POST MODIFICATION ROUTES
@app.route('/deletePost',methods=['POST'])
def deletePost():
    form_data = request.get_json(force=True)
    accID = Account.decode_auth_token(form_data['token'])
    bkID = form_data['id']
    bk = Post.query.filter_by(id=bkID).first()
    if(bk.by != Account.query.filter_by(id=accID).first().username):
        response = {'status':'fail','msg':'Unauthorized user!'} #Authenticate the current user
        return response #However this shouldn't happen, since user has to be authorized before delete.
    try:
        wadb.session.delete(bk)
        wadb.session.commit()
        msg = bk.bookname+" has been deleted successfully!"
        return {
            'msg':msg,
            'stat':"success"
        }
    except:
        return {'msg':"Failed to remove from database!", 'stat':"fail"}
    return {
        'status': "fail",
        'msg' : "unknown error"
    }

@app.route('/deletebuyorder',methods=['POST'])
def deletebuyorder():
    form_data = request.get_json(force=True)
    accID = Account.decode_auth_token(form_data['token'])
    buyOrder = Buyorder.query.filter_by(id=int(form_data['bkid'])).first()
    if(buyOrder.by != Account.query.filter_by(id=accID).first().username):
        response = {'status':'fail','msg':'Unauthorized user!'} #Authenticate the current user
        return response
    try:
        wadb.session.delete(buyOrder)
        wadb.session.commit()
        msg = "The buy order "+buyOrder.bookname+" has been deleted successfully!"
        return {
            'msg':msg,
            'stat':"success"
        }
    except:
        return {'msg':"Failed to remove this buy order from database!", 'stat':"fail"}
    return {
        'status': "fail",
        'msg' : "unknown error"
    }

@app.route('/priceChange',methods=['POST'])
def priceChange():
    form_data = request.get_json(force=True)
    accID = Account.decode_auth_token(form_data['token'])
    bkID = form_data['id']
    bk = Post.query.filter_by(id=bkID).first()
    oldPrice = bk.price
    updatedBK = bk
    updatedBK.price = form_data['newP']
    if(bk.by != Account.query.filter_by(id=accID).first().username):
        response = {'status':'fail','msg':'Unauthorized user!'} #Authenticate the current user
        return response #However this shouldn't happen, since user has to be authorized before delete.
    try:
        wadb.session.delete(bk)
        wadb.session.add(updatedBK)
        wadb.session.commit()
        msg = bk.bookname+"'s price has been updated from $"+str(oldPrice)+" to $"+str(updatedBK.price)
        return {
            'msg':msg,
            'stat':"success"
        }
    except:
        return {'msg':"Failed to update post!", 'stat':"fail"}
    return {
        'status': "fail",
        'msg' : "unknown error"
    }

@app.route('/descriptionChange',methods=['POST'])
def descriptionChange():
    form_data = request.get_json(force=True)
    accID = Account.decode_auth_token(form_data['token'])
    bkID = form_data['id']
    bk = Post.query.filter_by(id=bkID).first()
    updatedBK = bk
    updatedBK.description = form_data['newD']
    if(bk.by != Account.query.filter_by(id=accID).first().username):
        response = {'status':'fail','msg':'Unauthorized user!'} #Authenticate the current user
        return response #However this shouldn't happen, since user has to be authorized before delete.
    try:
        wadb.session.delete(bk)
        wadb.session.add(updatedBK)
        wadb.session.commit()
        msg = bk.bookname+"'s description has been updated!"
        return {
            'msg':msg,
            'stat':"success"
        }
    except:
        return {'msg':"Failed to update post!", 'stat':"fail"}
    return {
        'status': "fail",
        'msg' : "unknown error"
    }

# End Zack & Yuki


# Yuanyuan Bao, Zack, Dennis
@app.route("/post", methods=['POST', 'GET'])
def post():
    if request.method == 'POST':
        response = ""
        username = ""
        # pass data from angular to flask
        form_data_all = request.get_json(force=True)
        form_data = form_data_all['bookdata']
        userID = Account.decode_auth_token(form_data_all['token'])
        if str(type(userID)) == "<class 'int'>":
            username = Account.query.filter_by(id=userID).first().username
            print(username, file=sys.stderr)
        else:
            return jsonify(response="Token Error")
        #print(form_data['BookName'], file=sys.stderr)
        post_by = username
        bkname = str(form_data['BookName'])
        aut = str(form_data['Author'])
        post_price = float(form_data['Price'])
        stat = str(form_data['status'])
        coll = str(form_data['college'])

        post = Post(by=post_by, bookname=bkname, author=aut, price=post_price, stat=stat,
                    college=coll, time=datetime.datetime.now())
        wadb.session.add(post)
        wadb.session.commit()
        if post != None:
            response = 'Successfully uploaded!'
        else:
            response = 'An Exception has occured!'
        return jsonify(response=response)
    if request.method == 'GET':
        return "placeholder"
# end of Yuanyuan, Zack, Dennis

# Yuanyuan Bao, Zack Lin
@app.route("/buyorder", methods=['POST', 'GET'])
def buyorder():
    if request.method == 'POST':
        response = ""
        username = ""
        # pass data from angular to flask
        form_data_all = request.get_json(force=True)
        form_data = form_data_all['bookdata']
        userID = Account.decode_auth_token(form_data_all['token'])
        if str(type(userID)) == "<class 'int'>":
            username = Account.query.filter_by(id=userID).first().username
            print(username, file=sys.stderr)
        else:
            return jsonify(responses="Token Error")
        #print(form_data['BookName'], file=sys.stderr)
        post_by = username
        bkname = str(form_data['BookName'])
        aut = str(form_data['Author'])
        post_price = float(form_data['Price'])
        stat = str(form_data['status'])
        coll = str(form_data['college'])

        # need buy_post database~~
        buy_post = Buyorder(by=post_by, bookname=bkname, author=aut, price=post_price, stat=stat,
                           college=coll, time=datetime.datetime.now())
        wadb.session.add(buy_post)
        wadb.session.commit()
        if buy_post != None:
            response = 'Successfully uploaded!'
        else:
            response = 'An Exception has occured!'
        return jsonify(responses=response)
    if request.method == 'GET':
        return "placeholder"


@app.route('/buylist', methods=['GET'])
def buylist():
    bulist = Buyorder.query.order_by(Buyorder.time.desc()).all()
    # get all books
    jsonBData = {
        "bookdatas": bulist
    }
    return jsonify([jsonBData])
#End of Yuanyuan, Zack

#picUrl=""

# Following are the code by Dennis Majano, Hanyan Zhang (Yuki), Zhixi Lin (Zack)
@app.route('/createAccPage', methods=['POST', 'GET'])
@cross_origin()
def createAcc():
    if request.method == 'POST':
        form_data = request.get_json(force=True)
        print(form_data['usern'], file=sys.stderr)
        msg = ""
        user = str(form_data["usern"])
        mail = str(form_data["emaila"])
        FSUid = str(form_data["fsu"])
        firstName = str(form_data["firstn"])
        lastName = str(form_data["lastn"])
        pwd1 = str(form_data["pass1"])
        pwd2 = str(form_data["pass2"])
        picture = str(form_data["pic"])

        # Types of errors that can occur
        error1 = "Username already exists. "
        error2 = "Email already exists. "
        error3 = "FSUID already exists. "
        error4 = "Failed to register data, please try again. "

        # Validation of the user input:
        # If filter returns a result, it means the user or email already exsist
        if bool(Account.query.filter_by(username=user).all()):
            msg += error1
        if bool(Account.query.filter_by(email=mail).all()):
            msg += error2
        if bool(Account.query.filter_by(fsuid=FSUid).all()):
            msg += error3
        if pwd1 != pwd2:
            msg += "Password does not match. "

        if msg == "":
            try:
                # add variable input into the database
                # if wadb.session.query(Account).filter_by(email=mail).count() < 1:
                #print(picUrl)
                userinfo = Account(firstname=firstName, lastname=lastName,
                                   username=user, avatar=picture, password=pwd1, email=mail, fsuid=FSUid)
                #print(userinfo.avatar)
                #print(userinfo.username)
                wadb.session.add(userinfo)
                wadb.session.commit()
                # Ensure the account can be found on database, so there's nothing wrong with input to database.
                # session['user'] = str(Account.query.filter_by(
                #     username=user).first().username)
                # msg = "You have successfully registered!"
                temp = Account.query.filter_by(username=user).first()
                authToken = temp.encode_auth_token(temp.id)
                if authToken:  # ensure authentication token is correctly generated
                    response = jsonify({
                        'status': 'success',
                        'msg': 'Successfully logged in.',
                        'auth_token': authToken
                    })
                
                return response
            except:
                return "Error adding to the database!"
        response = jsonify({
            'status': 'fail',
            'msg': msg
        })
        response.headers.add('Access-Control-Allow-Headers',
                             "Origin, X-Requested-With, Content-Type, Accept, x-auth")
        return response
    else:
        return "Place holder"
    # End Dennis, Yuki, Zack

#Uploads file images
#Folowing code by Dennis Majano
@app.route('/uploadFile', methods=['POST'])
def uploadFile():
    #Assume that the post request has a file part
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print("uploaded",file=sys.stderr)
    return jsonify(
        msg = "Picture Uploaded", 
        picUrl = filename
    )
    #returns the name of the file that is supposed to be uploaded
# end of Dennis        

if __name__ == '__main__':
    app.run(debug=True)
