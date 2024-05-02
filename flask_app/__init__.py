from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

import os

# Create a new Spotify client
from .client import SpotifyClient

spotify_client = SpotifyClient()

bcrypt = Bcrypt()
bootstrap = Bootstrap5()
login_manager = LoginManager()
db = MongoEngine()

# Import blueprints
from .users.routes import users
from .players.routes import players

def custom_404(e):
    return render_template('404.html', error=str(e)), 404

def create_app(test_config=None):
    app = Flask(__name__)

    # Load environment variables into config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
    app.config['MONGODB_HOST'] = os.environ.get('MONGODB_HOST', 'default_mongodb_host')
    app.config['CLIENT_ID'] = os.environ.get('CLIENT_ID', 'default_client_id')
    app.config['CLIENT_SECRET'] = os.environ.get('CLIENT_SECRET', 'default_client_secret')

    if test_config is not None:
        app.config.update(test_config)
    
    spotify_client.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(users)
    app.register_blueprint(players)
    app.register_error_handler(404, custom_404)

    login_manager.login_view = 'users.login'
    
    return app