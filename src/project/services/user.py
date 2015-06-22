'''
project.services.user
'''

from . import BaseService
from ..models.user import User

class UserService(BaseService):
    def generate_auth_token(self, user, expires_in=None):
        self.logger.debug(
            "Generating authentication token for user {} <{}>".format(
                user.id,
                user.email
            )
        )
        secret_key = self.config.get('SECRET_KEY')
        if not secret_key:
            raise Exception("Can not generate authenticate token. Secret key is not configured")
        return user.generate_auth_token(
            secret_key,
            expires_in if expires_in is not None else self.config.get('AUTH_TOKEN_TTL', 3600)
        )

    def authenticate(self, email_or_token, password=''):
        if password == '':
            self.logger.debug("Authenticating token '{}' ...".format(email_or_token))
            secret_key = self.config.get('SECRET_KEY')
            if not secret_key:
                raise Exception("Can not authenticate by token. Secret key is not configured")
            return User.verify_auth_token(secret_key, email_or_token)
        self.logger.debug("Authenticating by password for {} ...".format(email_or_token))
        user = User.query.filter_by(email=email_or_token).first()
        if user and user.verify_password(password):
            return user
        return None
