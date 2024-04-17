from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import LoginForm, RegistrationForm
from ..models import User

users = Blueprint('users', __name__)

""" *** User view functions *** """

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('players.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()

        # Automatically log in user
        login_user(user)
        flash('Successfully registered!', 'success')
        return redirect(url_for('players.index'))
    
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('players.index'))
    
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.objects(username=form.username.data).first()
            password_match = user is not None and bcrypt.check_password_hash(user.password, form.password.data)

            if user is not None and password_match:
                login_user(user)
                return redirect(url_for('players.index'))
            else:
                flash('Username or password is incorrect.', 'error')
                return redirect(url_for('users.login'))

    return render_template('login.html', title='Login', form=form) 

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('players.index'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return 'account'