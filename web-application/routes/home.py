from flask import render_template

from app import app


@app.route('/')
def index():
    name = 'John'

    return render_template('index.html', name=name)
