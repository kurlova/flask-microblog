from datetime import datetime
from functools import wraps
from flask import g, request, render_template, flash, redirect, url_for
from flask_login import logout_user, current_user
from microblog import app, db
from .forms import LoginForm, EditForm
from .models import User


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


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


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/user/<nickname>')
@login_required
def user_profile(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User {} not found.'.format(nickname))

        return redirect(url_for('index'))

    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]

    return render_template('user.html',
                           user=user,
                           posts=posts)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes will be saved')

        return redirect(url_for('index'))

    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me

        return render_template('edit.html', form=form)
