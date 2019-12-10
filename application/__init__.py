from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = '12345rtyh7u89ko0pjgtt54fg34568u3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EAS.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from application import routes