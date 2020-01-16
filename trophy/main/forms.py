from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, SubmitField
from trophy.models import User

#Search form for searching existing users
class SearchForm(FlaskForm):
	#Username of the individual(s) to search
	username = StringField('Username',
		validators=[DataRequired(), Length(min=2,max=20)])
	#Submit button
	submit = SubmitField('Search')
