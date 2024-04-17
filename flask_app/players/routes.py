from flask import Blueprint

players = Blueprint('players', __name__)

""" *** Player view functions *** """

@players.route('/', methods=['GET', 'POST'])
def index():
    return 'index'

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
    return f'user {user_id}'

@players.route('/user/<user_id>/library')
def user_library(user_id):
    return f'user {user_id} library'

@players.route('/user/<user_id>/reviews')
def user_reviews(user_id):
    return f'user {user_id} reviews'
