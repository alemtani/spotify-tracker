from flask import Blueprint, render_template
from flask_login import current_user
from hashlib import md5
from mongoengine.errors import ValidationError

from ..models import User
from ..utils import custom_404

players = Blueprint('players', __name__)

""" *** Player view functions *** """

@players.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@players.route('/search', methods=['GET'])
def search():
    return 'search'

@players.route('/player/<player_id>', methods=['GET', 'POST'])
def player_detail(player_id):
    return f'player {player_id}'

@players.route('/player/<player_id>/reviews')
def player_reviews(player_id):
    return f'player {player_id} reviews'

""" ** User view functions (no-auth) *** """

@players.route('/user/<user_id>')
def user_profile(user_id):
    try:
        user = User.objects(id=user_id).first()
        if not user:
            raise ValidationError(f'User with id {user_id} does not exist.')
        b64_img = user.get_b64_img()
        image = f'data:image/png;base64,{b64_img}' if b64_img \
            else f"https://www.gravatar.com/avatar/{md5(user.email.encode('utf-8')).hexdigest()}"
        return render_template('user_profile.html', image=image, user=user)
    except ValidationError as e:
        return custom_404(e)

@players.route('/user/<user_id>/library')
def user_library(user_id):
    return f'user {user_id} library'

@players.route('/user/<user_id>/reviews')
def user_reviews(user_id):
    return f'user {user_id} reviews'
