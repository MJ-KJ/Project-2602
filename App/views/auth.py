from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired

from App.models import User
from App.views import application

from App.controllers import (
    create_user,
    jwt_authenticate,
    jwt_required
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')



'''
Form Class
'''
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Please enter your username")])
    password = PasswordField('Password', validators=[InputRequired()])
    login = SubmitField("Login")

'''
Page/Action Routes
'''


@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('login.html', users=users)


@auth_views.route('/identify', methods=['GET'])
@login_required
def identify_page():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Get the submitted username and password
        username = form.username.data
        password = form.password.data

        # Authenticate the user
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth_views.login'))

        # Log the user in using Flask-Login
        login_user(user)

        # Redirect to the home page
        return redirect(url_for('application_views.home'))

    return render_template('login.html', form=form)

@auth_views.route('/logout', methods=['GET'])
@login_required
def logout_action():
    logout_user()
    return redirect(url_for('index_views.index_page'))

'''
API Routes
'''

@auth_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@auth_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['username'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = jwt_authenticate(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  return jsonify(access_token=token)

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {jwt_current_user.username}, id : {jwt_current_user.id}"})