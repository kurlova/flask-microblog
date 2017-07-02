from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD


app = Flask(__name__)  # creates the application object (of class Flask)
app.config.from_object('config')

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.init_app(app)
mail = Mail(app)

# Views module needs to import the app variable defined in this script.
# That's why we import app here, not in the beginning
from microblog import views, models, oauth_routes, error_routes

@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))

if not app.debug:
    msg = Message('flask microblog message',
                  sender=(MAIL_USERNAME, MAIL_PASSWORD),
                  recipients=ADMINS
                  )
    msg.body = 'App is working!'
    with app.app_context():
        mail.send(msg)
