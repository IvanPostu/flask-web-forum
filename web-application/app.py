from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get(
    'SQLALCHEMY_TRACK_MODIFICATIONS')

db: SQLAlchemy = SQLAlchemy(app)
