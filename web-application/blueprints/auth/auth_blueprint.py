from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from models import User

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():

    if request.method == 'POST':
        email: str = request.form.get('email')
        password: str = request.form.get('password')
        # password_repeat: str = request.form.get('password2')
        # name: str = request.form.get('name')

        new_user = User(email=email, password=generate_password_hash(
            password), active=True)
        db.session.add(new_user)
        db.session.commit()

        print(new_user)

        return redirect(url_for('index'))

    return render_template('sign-up.html')


@auth.route('/sign-in', methods=['POST', 'GET'])
@auth.route('/', methods=['POST', 'GET'])
def sign_in():
    email: str = request.form.get('email')
    password: str = request.form.get('password')

    if request.method == 'POST' and email and password:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home.index'))
        else:
            flash('Login or password is not correct.')

    elif request.method == 'POST':
        flash('Please fill login and password fields.')

    return render_template('sign-in.html')


@auth.route('/sign-out', methods=['GET', 'POST'])
def sign_out():
    logout_user()
    return redirect(url_for('index'))
