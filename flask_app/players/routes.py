from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from hashlib import md5
from mongoengine.errors import ValidationError

from .. import spotify_client
from ..forms import AddPlayerForm, DeletePlayerForm, EditAlbumPlayerForm, EditTrackPlayerForm
from ..models import Tracker, User
from ..utils import current_time

players = Blueprint('players', __name__)

""" *** Player view functions *** """

@players.route('/')
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
    add_form = AddPlayerForm()
    delete_form = DeletePlayerForm()

    try:
        item = request.args.get('item')
        if item not in ['album', 'track']:
            raise ValueError(f'A player must be an album or track')
        player = spotify_client.get_player_by_id(item, player_id)
        tracker = Tracker.objects(spotify_id=player_id, user=current_user).first() \
            if current_user.is_authenticated else None

        if request.method == 'POST':
            if add_form.submit_add.data and add_form.validate_on_submit():
                if item == 'album':
                    tracker = Tracker(
                        user = current_user,
                        last_updated = current_time(),
                        type = 'album',
                        spotify_id = player_id,
                        title = player.name,
                        artists = player.get_artists_list(),
                        image = player.get_image(),
                        release_date = player.release_year,
                        total_tracks = player.total_tracks,
                        listened_tracks = 0
                    )
                else:
                    tracker = Tracker(
                        user = current_user,
                        last_updated = current_time(),
                        type = 'track',
                        spotify_id = player_id,
                        title = player.name,
                        artists = player.get_artists_list(),
                        image = player.get_image(),
                        album = player.album.name,
                        duration = player.duration_ms
                    )
                tracker.save()
                flash('Successfully added tracker!', 'success')
                return redirect(url_for('players.player_detail', player_id=player_id, item=item))
            
            if delete_form.submit_delete.data and delete_form.validate_on_submit():
                tracker.delete()
                flash('Successfully deleted tracker!', 'success')
                return redirect(url_for('players.player_detail', player_id=player_id, item=item))

        return render_template('player.html', player=player, add_form=add_form, delete_form=delete_form, tracker=tracker)
    
    except ValueError as e:
        abort(404, e)

@players.route('/player/<player_id>/reviews')
def player_reviews(player_id):
    return f'player {player_id} reviews'

@players.route('/player/<player_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tracker(player_id):
    try:
        tracker = Tracker.objects(spotify_id=player_id, user=current_user).first()
        if not tracker:
            raise ValidationError(f'Could not find tracker for Spotify player')
        
        form = EditAlbumPlayerForm(obj=tracker) if tracker.type == 'album' \
            else EditTrackPlayerForm(obj=tracker)
        if request.method == 'POST':
            if form.validate_on_submit():
                if tracker.type == 'album':
                    tracker.modify(listened_tracks=form.listened_tracks.data)
                tracker.modify(status=form.status.data, last_updated=current_time())
                tracker.save()
                flash('Successfully updated tracker!', 'success')
                return redirect(url_for('players.player_detail', player_id=player_id, item=tracker.type))

        if tracker.type == 'album':
            return render_template('edit_tracker.html', title=tracker.title, type=tracker.type, form=form, listened_tracks=tracker.listened_tracks, total_tracks=tracker.total_tracks)
        else:
            return render_template('edit_tracker.html', title=tracker.title, type=tracker.type, form=form)
    
    except ValidationError as e:
        abort(404, e)

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
    return render_template('library.html', user_id=user_id)

@players.route('/user/<user_id>/trackers')
def user_tracks(user_id):
    user = User.objects(id=user_id).first()
    if not user:
        raise ValidationError(f'User with id {user_id} does not exist')
    item = request.args.get('item')
    if not item:
        return jsonify(data=[])
    trackers = Tracker.objects(user=user, type=item)
    return jsonify(data=trackers, type=item)

@players.route('/user/<user_id>/reviews')
def user_reviews(user_id):
    return f'user {user_id} reviews'
