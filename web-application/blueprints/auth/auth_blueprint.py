from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from werkzeug.security import check_password_hash, generate_password_hash

import os
import uuid
import base64

from app import db, app
from models import User, Role

auth = Blueprint('auth', __name__, template_folder='templates',
                 static_folder='static')


@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():

    if request.method == 'POST':
        email: str = request.form.get('email')
        password: str = request.form.get('password')
        password_repeat: str = request.form.get('password2')
        firstname: str = request.form.get('firstname')
        lastname: str = request.form.get('lastname')
        imgdata: str = request.form.get('imgdata')

        if not (email or password or password_repeat or firstname or lastname):
            flash('Please fill all fields!')
        elif password != password_repeat:
            flash('Passwords are not equal!')
        elif not imgdata:
            flash('Take a photo of the face.')
        else:
            face_img_filename: str = os.path.join(
                app.config['UPLOAD_FOLDER'], str(uuid.uuid4())) + '.jpeg'

            imgdata = imgdata.replace('data:image/jpeg;base64,', '')
            with open(face_img_filename, 'wb') as fh:
                fh.write(base64.decodebytes(imgdata.encode()))

            usr_role = Role.query.filter_by(name=Role.user().name).first()
            new_user = User(email=email, password=generate_password_hash(
                password), active=True, lastname=lastname, firstname=firstname,
                face_image_location=face_img_filename, roles=[usr_role])
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth.sign_in'))

    return render_template('auth/sign-up.html')


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

    return render_template('auth/sign-in.html')


@auth.route('/sign-out', methods=['GET', 'POST'])
def sign_out():
    logout_user()
    return redirect(url_for('index'))
