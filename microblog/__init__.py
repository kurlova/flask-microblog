import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import logdir


app = Flask(__name__)  # creates the application object (of class Flask)
app.config.from_object('config')

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.init_app(app)

# Views module needs to import the app variable defined in this script.
# That's why we import app here, not in the beginning
from microblog import views, models, oauth_routes, error_routes

@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))

# configuring logging
if not os.path.exists(logdir):
    os.makedirs(logdir)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1*1024*1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s: %(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')