from flask import render_template, request, Blueprint, flash, redirect,url_for
from trophy.main.forms import SearchForm
from trophy.models import User, Post

main = Blueprint('main',__name__)

#Keeping this above the Home Page Route returns the same page!
@main.route('/')

#Takes user to the same page as the above Route
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
@main.route('/search', methods=['GET','POST'])
def search():
	print ("search")
	form = SearchForm()
	if form.validate_on_submit() and request.method == 'POST':
		#Get username that was inputted into the form
		user = form.username.data
		#Get all users that have the username within theirs
		users = User.query.filter(User.username.contains(str(user))).all()
		#If users were found, send this information to the search_results template
		if users:
			return render_template('search_results.html', title='Search Results', form=form, users=users)
		#Else, no users were found, display error message and redirect to search page
		else:
			flash(f'No Results Found','danger')
			return redirect(url_for('main.search'))

	#Else, user has not submitted the form, so display search page
	return render_template('search.html', title='Search', form=form)	
