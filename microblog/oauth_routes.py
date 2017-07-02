from flask import flash, redirect, url_for
from flask_login import current_user, login_user
from microblog import app, db
from .oauth import OAuthSignIn
from .models import User


# ensures that the user is not logged in
# obtains the OAuthSignIn subclass appropriate for the given provider
@app.route('/autorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:

        return redirect(url_for('index'))

    oauth = OAuthSignIn.get_provider(provider)

    return oauth.authorize()


# the OAuth provider redirects back to the application after the user authenticates
# and gives permission to share information
@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:

        return redirect(url_for('index'))

    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed')

        return redirect(url_for('index'))

    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        print(user.nickname)
        db.session.add(user)
        db.session.commit()

    login_user(user, True)
    print('user is logged in!')

    return redirect(url_for('index'))