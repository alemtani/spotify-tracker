from flask import Flask
from flask_login import LoginManager
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Create a new Mongo client and connect to the database
uri = 'mongodb+srv://mongodb:mongodb@cluster0.gy12rxn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

mongo_client = MongoClient(uri, server_api=ServerApi('1'))
db = mongo_client.trackers

# Create a new Spotify client
from .client import SpotifyClient

CLIENT_ID = '7dc4ccd94bfc45c7946f8d937867df4b'
CLIENT_SECRET = '061d96a2988f4726a2f84ee62690854c'

spotify_client = SpotifyClient(CLIENT_ID, CLIENT_SECRET)

login_manager = LoginManager()

# Import blueprints
from .users.routes import users
from .players.routes import players

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile('config.py', silent=False)
    if test_config is not None:
        app.config.update(test_config)
    
    login_manager.init_app(app)
    
    # Register blueprints
    app.register_blueprint(users)
    app.register_blueprint(players)

    login_manager.login_view = 'users.login'
    
    return app