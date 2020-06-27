from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from werkzeug.security import check_password_hash, generate_password_hash

import os
import uuid
import base64

from app import db, app
from models import User, Role
from face_id.face_id import compare_faces_from_imagefiles, FacesNotFoundException

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

            flash('User has been registrated !!!', 'success')
            return redirect(url_for('auth.sign_in'))

    return render_template('auth/sign-up.html')


@auth.route('/sign-in', methods=['POST', 'GET'])
@auth.route('/', methods=['POST', 'GET'])
def sign_in():

    if request.method == 'POST':
        email: str = request.form.get('email')
        password: str = request.form.get('password')
        imgdata: str = request.form.get('imgdata')
        validation_errors = []

        # First step validation
        # Check if all form fields filled.
        if not email:
            validation_errors.append('Please fill login fild.')
        if not password:
            validation_errors.append('Please fill password fild.')
        if not imgdata:
            validation_errors.append('Please take a screen of your face.')

        if len(validation_errors) > 0:
            for err in validation_errors:
                flash(err, 'warning')
            return render_template('auth/sign-in.html')

        user_from_db: User = User.query.filter_by(email=email).first()

        # Second step validation
        # Find user by email and compare password from front. with pass. from db.
        if not user_from_db or not check_password_hash(user_from_db.password, password):
            flash('Login or password is not correct.', 'warning')
            return render_template('auth/sign-in.html')

        # Thrid step validation, if all is well then authenticate the user.
        # Create temp face image file, and compare it with user image,
        # after delete temp.
        temp_face_image_from_ui: str = os.path.join(app.config['UPLOAD_FOLDER'],
                                                    'temp_' + str(uuid.uuid4())) + '.jpeg'
        usr_image_path: str = user_from_db.face_image_location

        imgdata = imgdata.replace('data:image/jpeg;base64,', '')
        with open(temp_face_image_from_ui, 'wb') as fh:
            fh.write(base64.decodebytes(imgdata.encode()))

        the_same_person: bool = False

        try:
            the_same_person: bool = compare_faces_from_imagefiles(
                usr_image_path, temp_face_image_from_ui)
        except FacesNotFoundException:
            # Delete temp image file from disk.
            os.remove(temp_face_image_from_ui)
            flash('Face not recognized.', 'danger')
            return render_template('auth/sign-in.html')

        # Delete temp image file from disk.
        os.remove(temp_face_image_from_ui)

        if the_same_person:
            login_user(user_from_db)
            return redirect(url_for('home.index'))
        else:
            flash('The face is not recognized.', 'danger')
            return render_template('auth/sign-in.html')

    return render_template('auth/sign-in.html')


@auth.route('/sign-out', methods=['GET', 'POST'])
def sign_out():
    logout_user()
    return redirect(url_for('index'))
