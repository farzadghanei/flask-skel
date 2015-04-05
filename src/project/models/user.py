'''
project.models.user
-------------------
Defines a user model class
'''

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from flask.ext.login import UserMixin

from ..extensions import db
from . import ModelMixin

class User(UserMixin, ModelMixin, db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User {} {} <{}>>'.format(self.name, self.surname, self.email)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, secret_key, expiration=3600):
        return Serializer(secret_key, expiration).dumps({'confirm': self.id})

    def confirm(self, secret_key, token):
        serializer = Serializer(secret_key)
        try:
            data = serializer.loads(token)
        except (ValueError, SignatureExpired, BadSignature):
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        return True

    def generate_reset_token(self, secret_key, expiration=3600):
        return Serializer(secret_key, expiration).dumps({'reset': self.id})

    def reset_password(self, secret_key, token, new_password):
        serializer = Serializer(secret_key)
        try:
            data = serializer.loads(token)
        except (ValueError, SignatureExpired, BadSignature):
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        return True

    def generate_auth_token(self, secret_key, expires_in):
        return Serializer(secret_key, expires_in=expires_in).dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(secret_key, token):
        serializer = Serializer(secret_key)
        try:
            data = serializer.loads(token)
        except (ValueError, SignatureExpired, BadSignature):
            return None
        return User.query.get(data['id'])

__all__ = ('User',)
