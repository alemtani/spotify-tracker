from flask_login import UserMixin
from io import BytesIO
from werkzeug.utils import secure_filename

import base64

from . import db, login_manager

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