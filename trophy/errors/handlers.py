from flask import Blueprint, render_template

#Create errors blueprint
errors = Blueprint('errors', __name__)

#app_errorhandler is used so we can handle errors throughout entire application

#Error handler for our 404 error
@errors.app_errorhandler(404)
def error_404(error):
	#404 is the status code returned (default is 200, so we need to specify)
	return render_template('errors/404.html'), 404

#Error handler for our 403 error
@errors.app_errorhandler(403)
def error_403(error):
	#403 is the status code returned (default is 200, so we need to specify)
	return render_template('errors/403.html'), 403

#Error handler for our 500 error
@errors.app_errorhandler(500)
def error_500(error):
	#500 is the status code returned (default is 200, so we need to specify)
	return render_template('errors/500.html'), 500