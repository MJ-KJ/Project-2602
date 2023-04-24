from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user
from App.config import config
import os
from twilio.rest import Client

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')


@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_user("bob", "bobbers", "bob", "bob@gmail.com", "1111111","bobpass")
    create_user("tam", "tammers", "tam", "tam@gmail.com", "2222222", "tampass")

    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/sms', methods=['GET'])
def sms(phone):
    client = Client(config['TWILIO_ID'],config['TWILIO_AUTH_TOKEN'])
    message = client.messages.create(
        from_="+16813773924",
        body="Hello from Twilio",
        to="+1868"+phone
    )
    return jsonify({'id': config['TWILIO_ID']})

@index_views.route('/whats', methods=['GET'])
def whats(phone):
    client = Client(config['TWILIO_ID'],config['TWILIO_AUTH_TOKEN'])
    message = client.messages.create(
        from_="+16813773924",
        body="Hello from Twilio",
        to="whatsapp:+186"+phone
    )
    return jsonify({'id': config['TWILIO_ID']})