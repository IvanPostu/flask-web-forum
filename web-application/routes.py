from flask import render_template, request, \
    redirect, url_for
from flask_security.utils import hash_password


from app import app, db


@app.route('/')
def index():
    return redirect(url_for('home.index'))


# @app.route('/signup', methods=['POST', 'GET'])
# def signup():

#     if request.method == 'POST':
#         email: str = request.form.get('email')
#         password: str = request.form.get('password')

#         user_datastore.create_user(
#             email=email, password=hash_password(password))
#         db.session.commit()

#         return redirect(url_for('index'))

#     return render_template('security/signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
