from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

UPLOAD_FOLDER = './toolbox/uploads'
DATAFRAME_DB = './toolbox/data/dataframe_db'

# Specify the application's root so Python may know where to look for templates, and static files.
app = Flask(__name__)

# This secret key is used to sercurely sign CSRF protection tokens. Although FlaskForm already have CSRF protection by default, this prepares the application for future implementation of AJAX
app.config['SECRET_KEY'] = 'R3YU9hssXvaBWT9R'
# Specifying the upload folder for uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# specifying the dataframe_db folder for dataframe type x-referencing
app.config['DATAFRAME_DB'] = DATAFRAME_DB
# Max file size is 25 MB
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
# Create an SQLalchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Initializing CSRF protection, password hashing with bcrypt, and database with SQLalchemy globally for the app
csrf = CSRFProtect(app)
# Instancing Bcrypt to allow password hashing
bcrypt = Bcrypt(app)
# Instancing SQLAlchemy to allow sessions, creating, and querying of databases
db = SQLAlchemy(app)
# Login_manager allows us to deal with user authentication easily
login_manager = LoginManager(app)
# Passing login function name from the routes so login_manager knows where login info is coming from
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from toolbox import routes