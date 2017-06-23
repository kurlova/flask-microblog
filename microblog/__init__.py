from flask import Flask


app = Flask(__name__)  # creates the application object (of class Flask)
app.config.from_object('config')

# Views module needs to import the app variable defined in this script.
# That's why we import app here, not in the beginning
from microblog import views
