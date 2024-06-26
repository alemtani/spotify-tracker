from enum import Enum
from flask_login import UserMixin
from io import BytesIO
from werkzeug.utils import secure_filename

import base64

from . import db, login_manager
from .utils import get_duration

choices = ['added', 'listening', 'done']

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True, min_length=1, max_length=40)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    about = db.StringField()
    profile_pic = db.ImageField()
    
    def get_id(self):
        return str(self.id)
    
    def set_profile_pic(self, img):        
        filename = secure_filename(img.filename)
        content_type = f'images/{filename[-3:]}'

        if self.profile_pic.get():
            self.profile_pic.replace(img.stream, content_type=content_type)
        else:
            self.profile_pic.put(img.stream, content_type=content_type)
    
    def get_b64_img(self):
        bytes_im = BytesIO(self.profile_pic.read())
        image = base64.b64encode(bytes_im.getvalue()).decode()
        return image
    
class Tracker(db.Document):
    # Every tracker needs these fields
    user = db.ReferenceField(document_type=User, required=True)
    last_updated = db.StringField(required=True)
    type = db.StringField(required=True)
    status = db.StringField(required=True, default='added', choices=choices)

    # We do this to "cache" the state, i.e. not call Spotify API to fetch library
    spotify_id = db.StringField(required=True, min_length=22, max_length=22)
    title = db.StringField(required=True)
    artists = db.ListField(db_field='artists', required=True)
    image = db.StringField(required=True)

    # Non-required fields (for track)
    album = db.StringField()
    duration = db.IntField()

    # Non-required fields (for album)
    release_date = db.IntField()
    total_tracks = db.IntField()
    listened_tracks = db.IntField()

    def get_id(self):
        return str(self.id)

    def get_player_json(self):
        return {
            'id': self.spotify_id,
            'name': self.title,
            'artists': self.artists,
            'image': self.image,
            'release_date': self.release_date if self.type == 'album' else None,
            'album': self.album if self.type == 'track' else None,
            'duration': get_duration(self.duration, 'track') if self.type == 'track' else None
        }

class Review(db.Document):
    user = db.ReferenceField(document_type=User, required=True)
    last_updated = db.StringField(required=True)
    rating = db.IntField(required=True, min_value=1, max_value=10)
    type = db.StringField(required=True)
    comment = db.StringField()

    # We do this to "cache" the state, i.e. not call Spotify API to fetch reviews
    spotify_id = db.StringField(required=True, min_length=22, max_length=22)
    title = db.StringField(required=True)

    def get_id(self):
        return self(str.id)