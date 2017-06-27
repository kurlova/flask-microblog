from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from microblog import app, db
from .forms import LoginForm
from .oauth import OAuthSignIn
from .models import User


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Yelena'}
    posts = [
        {
            'author': {'nikcname': 'John'},
            'body': 'Good day in London!'
        },
        {
            'author': {'nickname': 'Randy'},
            'body': 'Breakfast is awesome <3'
        }

    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="{0}", remember_me={1}'.format(form.openid.data,
                                                                         str(form.remember_me.data)))

        return redirect('/index')

    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


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


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('index'))

