from flask import Blueprint
from flask_login import login_required

users = Blueprint('users', __name__)

""" *** User view functions *** """

@users.route('/register', methods=['GET', 'POST'])
def register():
    return 'register'

@users.route('/login', methods=['GET', 'POST'])
def login():
    return 'login'

@users.route('/logout')
@login_required
def logout():
    return 'logout'

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return 'account'