from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)  # creates the application object (of class Flask)
app.config.from_object('config')

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.init_app(app)

# Views module needs to import the app variable defined in this script.
# That's why we import app here, not in the beginning
from microblog import views, models

@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))
