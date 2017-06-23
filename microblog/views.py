from flask import render_template, flash, redirect
from microblog import app
from .forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    # return "Hello, world!"

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
