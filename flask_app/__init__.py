from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

# Create a new Spotify client
from .client import SpotifyClient

CLIENT_ID = '7dc4ccd94bfc45c7946f8d937867df4b'
CLIENT_SECRET = '061d96a2988f4726a2f84ee62690854c'

spotify_client = SpotifyClient(CLIENT_ID, CLIENT_SECRET)

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

    app.config.from_pyfile('config.py', silent=False)
    if test_config is not None:
        app.config.update(test_config)
    
    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(users)
    app.register_blueprint(players)
    app.register_error_handler(404, custom_404)

    login_manager.login_view = 'users.login'
    
    return app