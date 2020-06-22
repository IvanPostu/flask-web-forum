from flask import Flask
from flask_sqlalchemy import SQLAlchemy


import os

__all__ = ['home', 'Post']

app = Flask(__name__)

# use variables from .env file
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get(
    "SQLALCHEMY_TRACK_MODIFICATIONS")


db: SQLAlchemy = SQLAlchemy(app)

from routes import home  # noqa: E402
from models import Post  # noqa: E402

db.create_all()
