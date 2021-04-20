from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from nittanybookstore.forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b971f3a241822da6c85d7954f8a0b146'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from nittanybookstore import routes