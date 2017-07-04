import os
import unittest

from config import basedir
from microblog import app, db
from microblog.models import User


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(nickname='TestUser', email='test@email.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/93942e96f5acd83e2e047ad8fe03114d?d=identicon&s=128'
        assert avatar[0:len(expected)] == expected

    def test_make_unique_nickname(self):
        u = User(nickname='TestUser', email='test@email.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('TestUser')
        assert nickname != 'TestUser'

        u = User(nickname=nickname, email='test2@email.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('TestUser')
        assert nickname2 != 'TestUser'
        assert nickname2 != nickname


if __name__ == '__main__':
    unittest.main()
