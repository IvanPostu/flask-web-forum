class Configuration(object):
    FLASK_APP = './web-application/main.py'
    FLASK_ENV = 'development'
    FLASK_DEBUG = 1
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://jonny:h3lloW0rld@localhost/app_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'abcsdkfpskjgp24g'
    SECURITY_PASSWORD_SALT = 'i2u89u2498u'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
