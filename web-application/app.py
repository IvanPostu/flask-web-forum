from flask import Flask

from posts.posts_blueprint import posts

app = Flask(__name__)

app.register_blueprint(posts, url_prefix='/blog')
