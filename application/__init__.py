from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = '12345rtyh7u89ko0pjgtt54fg34568u3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EAS.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


from application import routes