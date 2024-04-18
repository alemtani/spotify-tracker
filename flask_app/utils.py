from datetime import datetime
from io import BytesIO

import base64

from .models import User

def current_time():
    return datetime.now().strftime('%B %d, %Y at %H:%M:%S')

def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image