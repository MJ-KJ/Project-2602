import os
import importlib
from datetime import timedelta

# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY,TWILIO_AUTH_TOKEN,TWILIO_ID
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        config['TWILIO_AUTH_TOKEN'] = TWILIO_AUTH_TOKEN
        config['TWILIO_ID'] = TWILIO_ID
        delta = JWT_ACCESS_TOKEN_EXPIRES
    else:
        config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
        config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        config['RAWG_TOKEN'] = os.environ.get('RAWG_TOKEN')
        config['TWILIO_AUTH_TOKEN'] = os.environ.get('TWILIO_AUTH_TOKEN')
        config['TWILIO_ID']  = os.environ.get('TWILIO_ID')
        config['DEBUG'] = config['ENV'].upper() != 'PRODUCTION'
        delta = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 7))


    config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=int(delta))
    config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    config['TEMPLATES_AUTO_RELOAD'] = True
    config['SEVER_NAME'] = '0.0.0.0'
    config['PREFERRED_URL_SCHEME'] = 'https'
    config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    config["JWT_TOKEN_LOCATION"] = ["headers"]
    return config

config = load_config()