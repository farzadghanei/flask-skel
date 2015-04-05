#!/usr/bin/env python

import unittest
from project.models.user import User
import mock

class TestUser(unittest.TestCase):

    @mock.patch.object(User, "query")
    @mock.patch("project.models.user.db.session")
    def test_verify_auth_token(self, mock_session, mock_query):
        user = User(email="test@example.org", password='password', id = 32)
        key = 'sample_secret_key'
        expire_auth_token = user.generate_auth_token(key, -10)
        self.assertFalse(user.verify_auth_token(key, expire_auth_token))
        auth_token = user.generate_auth_token(key, 3600)
        self.assertIsNone(User.verify_auth_token(key, 'wrong_token'))

        mock_query.get.return_value = user
        auth_user = User.verify_auth_token(key, auth_token)
        mock_query.get.assert_called_with(32)
        self.assertEqual(auth_user, user)

    @mock.patch.object(User, "query")
    @mock.patch("project.models.user.db.session")
    def test_save(self, mock_session, mock_query):
        user = User(name='username', password='password', email='user@email.provider.org')
        user.save(True)
        mock_session.add.assert_called_with(user)
        self.assertTrue(mock_session.commit.called)

    def test_attrs(self):
        user = User(name='username', password='userpassword', email='user@email.provider.org', id=17)
        self.assertEqual('username', user.name)
        self.assertEqual(17, user.id)
        self.assertEqual('user@email.provider.org', user.email)
        self.assertRaises(AttributeError, lambda : user.password)

    def test_verify_password(self):
        user = User(name='username', password='userpassword_20')
        self.assertFalse(user.verify_password('wrong _password'))
        self.assertTrue(user.verify_password('userpassword_20'))

    def test_confirm(self):
        user = User(password='userpassword', id = 103)
        key = 'sample_secret_key'
        expire_confirm_token = user.generate_confirmation_token(key, -10)
        self.assertFalse(user.confirm(key, expire_confirm_token))
        confirm_token = user.generate_confirmation_token(key, 3600)
        self.assertFalse(user.confirm(key, 'wrong_token'))
        self.assertTrue(user.confirm(key, confirm_token))

    def test_reset_password(self):
        user = User(password='userpassword', name='username', id=104)
        key = 'sample_secret_key'
        expire_reset_token = user.generate_reset_token(key, -10)
        self.assertFalse(user.reset_password(key, expire_reset_token, 'new_password'))
        self.assertTrue(user.verify_password('userpassword'))
        reset_token = user.generate_reset_token(key, 3600)
        self.assertTrue(user.reset_password(key, reset_token, 'new_password'))
        self.assertTrue(user.verify_password('new_password'))

if __name__ == '__main__':
    unittest.main()