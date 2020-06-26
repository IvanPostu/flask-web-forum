import os
from dotenv import load_dotenv
# Load all from .env file.

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


class Configuration(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        'SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')

    # On migrate uncomment and set lines below
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://jonny:h3lloW0rld@localhost/app_database'
    # SQLALCHEMY_TRACK_MODIFICATIONS = '0'
