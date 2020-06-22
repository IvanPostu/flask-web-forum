from flask import Flask
from posts.blueprint import posts

app = Flask(__name__)
app.register_blueprint(posts, url_prefix='/blog')

from routes import home  # noqa: E402
__all__ = ['home']
