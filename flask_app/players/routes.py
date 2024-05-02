from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from hashlib import md5
from mongoengine.errors import ValidationError

from .. import spotify_client
from ..forms import AddPlayerForm, DeletePlayerForm, EditAlbumPlayerForm, EditTrackPlayerForm, ReviewForm
from ..models import Review, Tracker, User
from ..utils import current_time, str2datetime

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
    data = list(map(lambda player: player.to_json(), result['items']))
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
        tracker = Tracker.objects(spotify_id=player_id, user=current_user).first() if current_user.is_authenticated else None
        user_review = Review.objects(spotify_id=player_id, user=current_user).first() if current_user.is_authenticated else None
        reviews = Review.objects(spotify_id=player_id)
        rating = round(reviews.average('rating'), 1)

        # Sort reviews
        reviews = list(reviews)
        reviews.sort(key=lambda review: str2datetime(review.last_updated), reverse=True)

        # Track reviews (will look good)
        track_ids = list(map(lambda track: track.id, player.tracks)) if item == 'album' else []
        track_reviews = Review.objects(spotify_id__in=track_ids)
        track_ratings = {}
        counts = {}
        for review in track_reviews:
            track_ratings[review.spotify_id] = track_ratings.get(review.spotify_id, 0) + review.rating
            counts[review.spotify_id] = counts.get(review.spotify_id, 0) + 1
        for spotify_id in track_ratings:
            track_ratings[spotify_id] = round(track_ratings[spotify_id] / counts[spotify_id], 1)

        review_form = ReviewForm(obj=user_review)

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
            
            if review_form.submit.data and review_form.validate_on_submit():
                if not user_review:
                    user_review = Review(
                        user = current_user, 
                        last_updated = current_time(),
                        rating = review_form.rating.data,
                        comment = review_form.comment.data,
                        spotify_id = player_id,
                        title = player.name,
                        type = item
                    )
                else:
                    user_review.modify(
                        last_updated = current_time(),
                        rating = review_form.rating.data,
                        comment = review_form.comment.data
                    )
                user_review.save()
                flash('Successfully created review!', 'success')
                return redirect(url_for('players.player_detail', player_id=player_id, item=item))
        
        return render_template('player.html', player=player, add_form=add_form, delete_form=delete_form, \
                               review_form=review_form, tracker=tracker, rating=rating, reviews=reviews, \
                                user_review=user_review, track_ratings=track_ratings)
    
    except ValueError as e:
        abort(404, e)

@players.route('/player/<player_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tracker(player_id):
    try:
        tracker = Tracker.objects(spotify_id=player_id, user=current_user).first()
        if not tracker:
            raise ValidationError(f'Could not find tracker for Spotify player')
        
        form = EditAlbumPlayerForm(obj=tracker) if tracker.type == 'album' else EditTrackPlayerForm(obj=tracker)
        if request.method == 'POST':
            if form.validate_on_submit():
                if tracker.type == 'album':
                    listened_tracks = form.listened_tracks.data
                    if form.status.data == 'done':
                        listened_tracks = tracker.total_tracks
                    if form.status.data == 'added':
                        listened_tracks = 0
                    tracker.modify(listened_tracks=listened_tracks)
                tracker.modify(status=form.status.data, last_updated=current_time())
                tracker.save()
                flash('Successfully updated tracker!', 'success')
                return redirect(url_for('players.player_detail', player_id=player_id, item=tracker.type))

        if tracker.type == 'album':
            return render_template('edit_tracker.html', title=f'Edit Tracker for {tracker.title}', \
                                   type=tracker.type, form=form, player_id=player_id, total_tracks=tracker.total_tracks)
        else:
            return render_template('edit_tracker.html', title=f'Edit Tracker for {tracker.title}', \
                                   type=tracker.type, form=form, player_id=player_id)
    
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
    try:
        user = User.objects(id=user_id).first()
        if not user:
            raise ValidationError(f'User with id {user_id} does not exist')
        return render_template('library.html', user_id=user_id)
    except ValidationError as e:
        abort(404, e)

@players.route('/user/<user_id>/trackers')
def user_tracks(user_id):
    user = User.objects(id=user_id).first()
    if not user:
        raise ValidationError(f'User with id {user_id} does not exist')
    item = request.args.get('item')
    status = request.args.get('status')
    if not item or not status:
        return jsonify(data=[])
    status = status.split(',')
    trackers = Tracker.objects(user=user, type=item, status__in=status)
    data = list(map(lambda tracker: tracker.get_player_json(), trackers))
    return jsonify(data=data, type=item)

@players.route('/user/<user_id>/reviews')
def user_reviews(user_id):
    try:
        user = User.objects(id=user_id).first()
        if not user:
            raise ValidationError(f'User with id {user_id} does not exist')
        reviews = Review.objects(user=user)
        reviews = list(reviews)
        reviews.sort(key=lambda review: str2datetime(review.last_updated), reverse=True)
        return render_template('reviews.html', reviews=reviews, user=user)
    except ValidationError as e:
        abort(404, e)
