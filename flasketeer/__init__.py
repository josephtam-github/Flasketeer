from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_login import LoginManager

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasketeer.db'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOADED_PHOTOS_DEST'] = 'flasketeer/static/img/'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login_page'
login_manager.login_message = 'You need to login to be able to post'
login_manager.login_message_category = 'info'

from flasketeer import routes
