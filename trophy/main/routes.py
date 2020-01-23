from flask import render_template, request, Blueprint, flash, redirect, url_for, abort
from flask_login import current_user, login_required
from trophy.main.forms import SearchForm
from trophy.models import User, Post
from trophy import db

main = Blueprint('main',__name__)

#Keeping this above the Home Page Route returns the same page!
@main.route('/')
@main.route('/home')
def home():
	page = request.args.get('page', 1,type=int)
	post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
	#Uses render_template to render our home page template
	return render_template('home.html', posts=post)

#Takes user to the About Page
@main.route('/about')
def about():
    return render_template('about.html', title='About')

#Takes user to the Search Page
@main.route('/search/', methods=['GET','POST'])
def search():
	form = SearchForm()
	if form.validate_on_submit() and request.method == 'POST':
		#Query all the users that have a username which contains the entered value in the form
		users = User.query.filter(User.username.contains(str(form.username.data))).all()

		#If users were found in query, send to search results page for the searched user
		if users:
			return redirect(url_for('main.search_users', username=form.username.data))
		#If users were not found in query, display warning message and reload page
		else:
			flash(f'No Results Found','danger')
			return redirect(url_for('main.search'))

	#If a get request was made and the form was not submitted, then just show the default search page
	return render_template('search.html', title='Search', form=form)


#Takes user to the searched user results, if any were found
@main.route('/search/<string:username>', methods=['GET','POST'])
def search_users(username):

	#Get the users that contain the searched username within their username
	users = User.query.filter(User.username.contains(str(username))).all()

	#If users were found and a POST request was made, follow the changes
	if users and request.method == 'POST':

		print (request.form)
		#Check is current user is an admin and if selected user is being verified/unverified or suspended/unsuspended
		if current_user.admin == True and request.form.get('VERIFY') is not None:
			print ("verify user")
			user = User.query.filter_by(username=request.form.get('VERIFY')).first()
			user.verified = 1
		elif current_user.admin == True and request.form.get('UNVERIFY') is not None:
			print ("unverify user")
			user = User.query.filter_by(username=request.form.get('UNVERIFY')).first()
			user.verified = 0
		elif current_user.admin == True and request.form.get('SUSPEND') is not None:
			print ("suspend user")
			user = User.query.filter_by(username=request.form.get('SUSPEND')).first()
			user.suspended = 1
		elif current_user.admin == True and request.form.get('UNSUSPEND') is not None:
			print ("unsuspend user")
			user = User.query.filter_by(username=request.form.get('UNSUSPEND')).first()
			user.suspended = 0
		db.session.commit()
		print (user)

	return render_template('search_results.html', title='Search Results', users=users, username=username)


#Takes user to the Admin Page
@main.route('/admin', methods=['GET','POST'])
@login_required
def admin():

	#If user is not an Admin, send the user to Forbidden Access page
	if current_user.admin == False:
		abort(403)

	return render_template('admin.html', title='Admin')