from flask import Flask

app = Flask(__name__)

from routes import home  # noqa: E402
__all__ = ['home']
