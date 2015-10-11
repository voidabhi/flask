__author__ = 'ABHIJEET'

import sys
from random import randint

from app import app, db, mail
from app.models import User
from app.utils import hash_password, verify_password
from app.forms import LoginForm,RegisterForm,RecoveryForm,NewPasswordForm
from flask import render_template, redirect, flash, url_for, current_app, session, request, abort, Markup
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.principal import AnonymousIdentity, Identity, UserNeed, identity_changed, identity_loaded, Permission, RoleNeed, PermissionDenied
from sqlalchemy import func

@app.route('/', methods=['GET'])
def index():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        remember_me = login_form.remember_me.data
        user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
        if login_user(user, remember_me):
            flash("You were logged in.", "success")
            if user.invitations.count():
                flash(Markup('You have %s team invitations - click <a href="%s">here</a> to view them.' % (user.invitations.count(), url_for("invitations"))), "info")
            return redirect(request.args.get("next") or url_for('index'))

            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
        else:
            flash("Login failed, user not validated", "error")
            return redirect(url_for("verify_status", username=username))

    elif register_form.validate_on_submit():
        username = register_form.username.data.strip()
        password = register_form.password.data
        email = register_form.email.data

        new_user = User(username, password, email)

        body = render_template("verification.txt", recipient = new_user, email_changed = False)
        mail.send_message(subject="Welcome to " + app.config["LONG_NAME"] + ", " + username, recipients=[new_user.email], body=body)

        db.session.add(new_user)
        db.session.commit()

        flash("Your account has been created, confirm your email to verify.", "success")
        return redirect(url_for('verify_status', username = username))
    return render_template('login.html', login_form = login_form, register_form = register_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(url_for('index'))

# we need this so Flask Principal knows what to do when a user is loaded
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'is_admin'):
        if current_user.is_admin:
            identity.provides.add(RoleNeed('admin'))

@app.route('/reset', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated():
        flash("You are already logged in.", "info")
        return redirect(url_for("index"))
    error = None
    form = RecoveryForm()
    if form.validate_on_submit():
        # thanks to the UsernameValidator we cam assume the username exists
        user = User.query.filter_by(username=form.username.data).first()
        user.token = randint(0, sys.maxint)
        db.session.commit()

        body = render_template("emails/account/reset_password.txt", recipient=user)
        mail.send_message(subject=app.config["LONG_NAME"] + ": Reset your password", recipients=[user.email], body=body)

        flash("Your password has been reset, check your email.", "success")
    return render_template('account/reset_request.html', form=form, error=error)

@app.route('/reset/<username>/<token>', methods=['GET', 'POST'])
def reset_verify(username, token):
    user = User.query.filter_by(username=username).first_or_404()
    if user.token == None:
        flash("%s's account has not requested a password reset." % user.username.capitalize(), "error")
        return redirect(url_for('index'))
    if user.getResetToken() != token:
        flash("This does not seem to be a valid reset link, if you reset your account multiple times make sure you are using the link in the last email you received!", "error")
        return redirect(url_for('index'))
    form = NewPasswordForm()
    error = None
    if form.validate_on_submit():
        # null the reset token
        user.token = None
        # set the new password
        user.password = hash_password(form.password.data)
        db.session.commit()
        flash("Your password was updated and you can login with it now.", "success")
        return redirect(url_for('login'))
    return render_template('account/reset_newpassword.html', user = user, form = form, error = error)


@app.route('/verify/', methods=["POST", "GET"])
def verify_send():
    if request.method == 'GET':
        return redirect(url_for('index'))

    username = request.form.get('username', "")
    user = User.query.filter_by(username = username).first_or_404()

    if user.is_verified:
        flash("%s's account is already validated." % user.username.capitalize(), "info")
        return redirect(url_for('index'))

    body=render_template("emails/account/verification.txt", recipient=user)
    mail.send_message(subject="Welcome to " + app.config["LONG_NAME"] + ", " + username, recipients=[user.new_email], body=body)

    flash("Verification has been resent, check your email", "success")
    return redirect(url_for('verify_status', username=username))

@app.route('/verify/<username>', methods=["GET"])
def verify_status(username):
    submitted = request.args.get('submitted', None)
    user = User.query.filter_by(username = username).first_or_404()

    if user.is_verified:
        flash("%s's account is already validated." % user.username.capitalize(), "info")
        return redirect(url_for('index'))

    return render_template('misc/verify_status.html', submitted=submitted, username=username)

@app.route('/verify/<username>/<verification>', methods=["GET"])
def verify(username, verification):
    user = User.query.filter_by(username = username).first_or_404()

    # check if user is verified
    if user.is_verified:
        flash("%s's account is already validated." % user.username.capitalize(), "success")
        return redirect(url_for('index'))

    # verification success
    if verification == user.getVerificationHash():
        user.is_verified = True
        user.email = user.new_email
        db.session.commit()

        flash("Your email has been confirmed, you may now login")
        return redirect(url_for('login'))

    # verification failure
    else:
        return redirect(url_for('verify_status', username=username, submitted=True))
