from flask import render_template

from app import app


@app.route('/')
def index():
    name = 'Ivan'
    return render_template('index.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
