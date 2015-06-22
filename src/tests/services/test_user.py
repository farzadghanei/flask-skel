#!/usr/bin/env python

import unittest
from project.models.user import User
from project.services.user import UserService
import mock

class TestUser(unittest.TestCase):
    @mock.patch.object(User, "verify_auth_token")
    @mock.patch("project.models.user.db.session")
    def test_authenticate_token(self, mock_session, mock_verify_auth):
        user = User(email='test@example.org', name='myname', surname='is test', id=1)
        mock_verify_auth.return_value = user
        logger = mock.MagicMock()
        secret_key = 'this key is secret'
        config = {'SECRET_KEY': secret_key}
        service = UserService(logger, config)
        token = service.generate_auth_token(user)
        auth_user = service.authenticate(token)
        mock_verify_auth.assert_called_with(secret_key, token)
        self.assertEqual(auth_user, user)

    @mock.patch.object(User, "verify_auth_token")
    @mock.patch("project.models.user.db.session")
    def test_authenticate_invalid_token_returns_none(self, mock_db_session, mock_verify_auth):
        mock_verify_auth.return_value = None
        logger = mock.MagicMock()
        secret_key = 'this key is secret'
        config = {'SECRET_KEY': secret_key}
        service = UserService(logger, config)
        user = service.authenticate('this is a token')
        mock_verify_auth.assert_called_with(secret_key, 'this is a token')
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()