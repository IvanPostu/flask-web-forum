from app import app
import routes

__all__ = ['routes']

from blueprints.forum.forum_blueprint import forum
from blueprints.home.home_blueprint import home
from blueprints.auth.auth_blueprint import auth

app.register_blueprint(forum, url_prefix='/forum')
app.register_blueprint(home, url_prefix='/home')
app.register_blueprint(auth, url_prefix='/auth')
