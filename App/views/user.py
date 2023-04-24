from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, EqualTo


from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
)

'''
Form Class
'''



class RegisterForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired(), Length(min=3, max=25,
                                                                          message="Name must be between 3 and 25 characters")])
    sname = StringField('Surname', validators=[InputRequired(), Length(min=3, max=25,
                                                                       message="Surname must be between 3 and 25 characters")])
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=25,
                                                                           message="Username must be between 3 and 25 characters")])
    email = EmailField('Email', validators=[InputRequired()])

    phone = StringField('Phone Number', validators=[InputRequired(), Length(min=7, max=7,
                                                                          message="Number must be 7 digits long")])
    password = PasswordField(label=('Password'),
                             validators=[InputRequired(),
                                         Length(min=3, message='Password should be at least 3 characters long')])
    password2 = PasswordField(
        label=('Confirm Password'),
        validators=[InputRequired(message='*Required'),
                    EqualTo('password', message='Both password fields must be equal!')])
    register = SubmitField("Register")


user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Get user data from the form
        fname = form.fname.data
        sname = form.sname.data
        username = form.username.data
        email = form.email.data
        phone = form.phone.data
        password = form.password.data

        # Create the user
        create_user(fname,sname,username,email,phone,password)

        return render_template('success.html')
    return render_template('register.html', form=form)


@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('', users=users)


@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)


@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['username'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})


@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))


@user_views.route('/static/users', methods=['GET'])
def static_user_page():
    return send_from_directory('static', 'static-user.html')
