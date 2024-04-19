from flask import Blueprint, abort, jsonify, render_template, request
from hashlib import md5
from mongoengine.errors import ValidationError

from .. import spotify_client
from ..models import User

players = Blueprint('players', __name__)

""" *** Player view functions *** """

@players.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@players.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    item = request.args.get('item')
    offset = request.args.get('offset', 0, type=int)
    if not q or not item:
        return jsonify(data=[])
    result = spotify_client.search_for_item(q, item, offset=offset)
    data = list(map(lambda player: player.toJSON(), result['items']))
    return jsonify(data=data, type=result['type'])

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
            raise ValidationError(f'User with id {user_id} does not exist')
        b64_img = user.get_b64_img()
        image = f'data:image/png;base64,{b64_img}' if b64_img \
            else f"https://www.gravatar.com/avatar/{md5(user.email.encode('utf-8')).hexdigest()}"
        return render_template('user_profile.html', image=image, user=user)
    except ValidationError as e:
        abort(404, e)

@players.route('/user/<user_id>/library')
def user_library(user_id):
    return f'user {user_id} library'

@players.route('/user/<user_id>/reviews')
def user_reviews(user_id):
    return f'user {user_id} reviews'
