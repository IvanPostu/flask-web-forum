from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from werkzeug.security import check_password_hash, generate_password_hash

import os
import uuid

from app import db, app
from models import User, Role

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():

    if request.method == 'POST':
        email: str = request.form.get('email')
        password: str = request.form.get('password')
        password_repeat: str = request.form.get('password2')
        face_imagefile = request.files['face_image']
        firstname: str = request.form.get('firstname')
        lastname: str = request.form.get('lastname')

        if not (email or password or password_repeat or firstname or lastname):
            flash('Please fill all fields!')
        elif password != password_repeat:
            flash('Passwords are not equal!')
        elif 'face_image' not in request.files:
            flash('No face image file part.')
        elif face_imagefile.filename == '':
            flash('No selected file.')
        else:
            face_img_filename: str = str(
                uuid.uuid4()) + '_' + face_imagefile.filename
            os_path_toFile = os.path.join(
                app.config['UPLOAD_FOLDER'], face_img_filename)
            face_imagefile.save(os_path_toFile)
            usr_role = Role.query.filter_by(name=Role.user().name).first()
            new_user = User(email=email, password=generate_password_hash(
                password), active=True, lastname=lastname, firstname=firstname,
                face_image_location=os_path_toFile, roles=[usr_role])
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
