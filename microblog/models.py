from flask_login import UserMixin
from microblog import db, lm
from hashlib import md5


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(500))
    last_seen = db.Column(db.DateTime)

    # The first argument to db.relationship indicates the "many" class of this relationship
    # The backref defines a field that will be added to the objects of the "many" class
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.nickname)

    def avatar(self, size):
        try:
            return 'http://www.gravatar.com/avatar/{0}?d=identicon&s={1}'.format(md5(self.email.encode('utf-8')).hexdigest(),
                                                                      size)
        except:
            return 'http://www.gravatar.com/avatar/{0}?d=identicon&s={1}'.format(md5(self.nickname.encode('utf-8')).hexdigest(),
                                                                          size)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(2000))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
