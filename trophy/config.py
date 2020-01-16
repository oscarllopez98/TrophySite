import os

class Config:
	#Retrieved using secrets library and set to Environment variable
	SECRET_KEY = os.environ.get('SECRET_KEY')

	#Set to Environment Variable
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

	#Configure email info so Trophy is able to send people emails
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

