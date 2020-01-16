#Imports from init file ( "app = Flask(__name__)" )
from trophy import create_app

#Run the create app function w/ default parameter
app = create_app()

#Only true if this script is run directly (>python flaskblog.py)
if __name__ == '__main__':
	app.run(debug=True)