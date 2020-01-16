#Importing Flask class
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from trophy.config import Config

#Initialize database
db = SQLAlchemy()
#Initialize encryption
bcrypt = Bcrypt()
#Initialize login manager
login_manager = LoginManager()
#How login manager knows how to redirect us when a page requires a login
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

#Initialize Mail
mail = Mail()

#Default param of Config class
def create_app(config_class=Config):
	#Creating var equal to an instance of Flask class
	#__ (Double underscore)is used for the name of the module (__name__)
	app = Flask(__name__)
	app.config.from_object(Config)

	#Done here so app isn't bound to specific config class(?)
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	#Import user, posts, and main routes
	from trophy.users.routes import users
	from trophy.posts.routes import posts
	from trophy.main.routes import main
	from trophy.errors.handlers import errors

	#Register those blueprints (Blueprints help for maintainability)
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)


	#Return the created application
	return app