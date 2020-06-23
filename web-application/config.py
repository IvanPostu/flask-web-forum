class Configuration(object):
    FLASK_APP = './web-application/main.py'
    FLASK_ENV = 'development'
    FLASK_DEBUG = 1
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://jonny:h3lloW0rld@localhost/app_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
