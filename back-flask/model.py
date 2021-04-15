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
class Order_List(wadb.Model):
    id: int
    time: str
    by: int
    bookname: str
    author: str
    price: float
    stat: str
    college: str

    __tablename__ = 'order_list'
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
