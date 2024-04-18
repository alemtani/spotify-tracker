from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import LoginForm, RegistrationForm, UpdateAccountForm, UpdatePasswordForm, UpdateProfilePicForm
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
            user = User.objects(email=form.email.data).first()
            password_match = user is not None and bcrypt.check_password_hash(user.password, form.password.data)

            if user is not None and password_match:
                login_user(user)
                flash('Successfully logged in!', 'success')
                return redirect(url_for('players.index'))
            else:
                flash('Email or password is incorrect.', 'error')
                return redirect(url_for('users.login'))

    return render_template('login.html', title='Log In', form=form) 

@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('players.index'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    update_account_form = UpdateAccountForm(obj=current_user)
    update_profile_pic_form = UpdateProfilePicForm()
    update_password_form = UpdatePasswordForm()

    if request.method == 'POST':
        if update_account_form.submit_account.data and update_account_form.validate_on_submit():
            # Check if new username is taken
            if current_user.username != update_account_form.username.data:
                new_user = User.objects(username=update_account_form.username.data).first()
                if new_user is not None:
                    flash('Username is taken.', 'error')
                    return redirect(url_for('users.account'))
            
            current_user.modify(
                username=update_account_form.username.data,
                about=update_account_form.about.data
            )
            current_user.save()

            flash('Successfully updated account!', 'success')
            return redirect(url_for('players.user_profile', user_id=current_user.get_id()))
        
        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate_on_submit():
            current_user.set_profile_pic(update_profile_pic_form.picture.data)
            current_user.save()
            flash('Successfully updated profile picture!', 'success')
            return redirect(url_for('players.user_profile', user_id=current_user.get_id()))
        
        if update_password_form.submit_password.data and update_password_form.validate_on_submit():
            password_match = bcrypt.check_password_hash(current_user.password, update_password_form.old_password.data)

            if password_match:
                hashed = bcrypt.generate_password_hash(update_password_form.new_password.data).decode('utf-8')
                current_user.modify(password=hashed)
                flash('Successfully updated password!', 'success')
                return redirect(url_for('players.user_profile', user_id=current_user.get_id()))
            else:
                flash('Old password is incorrect.', 'error')
                return redirect(url_for('users.account'))
    
    return render_template('account.html', title='Account Settings', \
                        update_account_form=update_account_form, \
                        update_profile_pic_form=update_profile_pic_form, \
                        update_password_form=update_password_form)