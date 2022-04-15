# importing required packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create application
app = Flask(__name__)

# define application configuration
app.config['SECRET_KEY'] = 'lx7E6161UpH9zwYlg1Mh38kljs987PO6do58OKca'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# adding custom filters to jinja environment
app.jinja_env.filters['zip'] = zip

# define db
db = SQLAlchemy(app)

# import routes
from application import routes
