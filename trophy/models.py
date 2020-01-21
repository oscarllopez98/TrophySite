from datetime import datetime
from trophy import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

#Database outline for fields a User will always have
class User(db.Model, UserMixin):
	#Unique id for referencing users
	id = db.Column(db.Integer, primary_key=True)
	#Unique username for a  user
	username = db.Column(db.String(20), unique=True, nullable=False)
	#Unique email for a user
	email = db.Column(db.String(20), unique=True, nullable=False)
	#Profile picture for a user
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	#Password for a user
	password = db.Column(db.String(60), nullable=False)
	#Posts by a user
	posts = db.relationship('Post',backref='author', lazy=True)
	#Admin status of a user
	admin = db.Column(db.Integer, nullable=False, default=0)
	#Suspended status of a user
	suspended = db.Column(db.Integer, nullable=False, default=0)
	#Date since a user first activated their account (Displayed to users as yyyy-mm-dd)
	member_since = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	#Verified status of a user (Recognized as a real account by administrators)
	verified = db.Column(db.Integer, nullable=False, default=0)

	#Get a user's reset token if they want to reset their password (Expires in 30 minutes)
	def get_reset_token(self,expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id':self.id}).decode('utf-8')

	#Verify that a user's reset token is valid and unexpired. If successful, return the appropriate User object
	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		#Check if token is valid/is expired
		try:
			user_id = s.loads(token)['user_id']
		#If invalid/expired, return None
		except:
			return None	
		#Return user if token is valid an not expired
		return User.query.get(user_id)

	#When printed out in the command line, show the following details about a User
	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.admin}', '{self.verified}', '{self.suspended}', '{self.member_since}')"

#Database outline for what fields a Post will always have
class Post(db.Model):
	#Unique id of a post
	id = db.Column(db.Integer, primary_key=True)
	#Title of a post
	title = db.Column(db.String(100), nullable=False)
	#Date posted for a post (displayed to users as yyyy-mm-dd)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	#Content (body) of a post
	content = db.Column(db.Text, nullable=False)
	#id of the user who created a post
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	#TODO: COMMENTS, LIKES, 


	#When printed out in the command line, show the following details about a Post
	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"
