from app import app
import routes

__all__ = ['routes']

from posts.posts_blueprint import posts
app.register_blueprint(posts, url_prefix='/blog')

if __name__ == '__main__':
    app.run()
