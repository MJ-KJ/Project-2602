from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired
from App.config import config
import os
from twilio.rest import Client
from App.controllers import *
from App.models import User



application_views = Blueprint('application_views', __name__, template_folder='../templates')

class ChangeUsernameForm(FlaskForm):
    username = StringField('New Username', validators=[InputRequired()])
    submit = SubmitField('Change Username')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[InputRequired()])
    new_password = PasswordField('New Password', validators=[InputRequired()])
    submit2 = SubmitField('Change Password')

class SearchUser(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    submit = SubmitField('Search')


@application_views.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('home.html', name= current_user.firstname )

@application_views.route('/profile', methods=['GET'])
@login_required
def profile():
    change_username_form = ChangeUsernameForm()
    change_password_form = ChangePasswordForm()
    return render_template('profile.html',
                           username=current_user.username,
                           fname=current_user.firstname,
                           lname=current_user.lastname,
                           email=current_user.email,
                           phone=current_user.phone,
                           change_username_form=change_username_form,
                           change_password_form=change_password_form)

@application_views.route('/profile', methods=['POST'])
@login_required
def update_user():
    form = ChangeUsernameForm()
    form2 = ChangePasswordForm()

    if "form-submit" in request.form and form.validate_on_submit():
        new_user = update_username(current_user.id, form.username.data)
        if new_user is not None:
            flash('Your username has been updated!', 'success')
        else:
            flash('Failed to update username', 'error')

    if "form2-submit" in request.form and form2.validate_on_submit():
        new_user = update_password(current_user.id, form2.current_password.data, form2.new_password.data)
        if new_user is not None:
            flash('Your password has been updated!', 'success')
        else:
            flash('Failed to update password', 'error')

    return redirect(url_for('application_views.profile'))


@application_views.route('/friends', methods=['GET'])
@login_required
def friendslist():
    friends_list = get_friends(current_user)
    return render_template('friendlist.html',friends=friends_list)

@application_views.route('/friendss', methods=['GET'])
@login_required
def friendslists():
    friends_list = get_friends(current_user)
    return render_template('friendlists.html',friends=friends_list)

@application_views.route('/search', methods=['GET'])
@login_required
def search():
    form = SearchUser()
    return render_template('search.html',form = form)

@application_views.route('/search', methods=['POST'])
@login_required
def fetch():
    form = SearchUser()
    if form.validate_on_submit():

        user = get_user(get_user_by_username(form.username.data))
        if user:
            return redirect(url_for('user_result', user=user))
        else:
            flash('User Not found', 'error')

    return render_template('search.html', form=form)


@application_views.route('/searchresult', methods=['GET'])
@login_required
def user_result(user):

    return render_template('result.html',username=user.username,
                           fname=user.firstname,
                           lname=user.lastname,
                           email=user.email,
                           phone=user.phone,)

@application_views.route('/alert', methods=['GET'])
@login_required
def alert():
    friends = current_user.get_friends()
    endclient = current_user.firstname
    client = Client(config['TWILIO_ID'], config['TWILIO_AUTH_TOKEN'])
    for friend in friends:

        message = client.messages.create(
            from_="+16813773924",
            body=endclient+" has reached home safely \n Courtesy of Friend Safe",
            to="whatsapp:+186" + friend.phone
        )
        message = client.messages.create(
            from_="+16813773924",
            body=endclient+" has reached home safely \n Courtesy of Friend Safe",
            to="+186" + friend.phone
        )

    return render_template('alertsucces.html' )

@application_views.route('/alerts', methods=['GET'])
@login_required
def alerts():
    endclient = current_user.firstname
    account_sid = 'ACf1cfa1cfec4fe5fce97bee3799a2c4a7'
    auth_token = 'b2f0b1e2607781d9a3627ed64393abbb'
    client = Client(account_sid, auth_token)


    client.messages.create(
            from_="+16813773924",
            body=endclient+" has reached home safely \n Courtesy of Friend Safe",
            to="+18682657767"
    )

    return render_template('alertsuccess.html' )

@application_views.route('/delete', methods=['GET'])
@login_required
def delete_account():
    user = current_user
    if user:
        db.session.delete(user)
        db.session.commit()
        logout_user()
        return render_template('successdelete.html' )
