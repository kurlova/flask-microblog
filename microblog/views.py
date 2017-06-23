from flask import render_template
from microblog import app

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
