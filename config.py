import os


basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'microblog.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False  # disable the modification tracking system

WTF_CSRF_ENABLED = True
SECRET_KEY = 'very_reliable_key'
OPENID_PROVIDERS = [
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]