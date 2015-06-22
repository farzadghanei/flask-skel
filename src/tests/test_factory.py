import logging
import unittest
import flask

from project import factory

class TestConfig(object):
    SECRET_KEY = 'some_secrecy_is_ok'
    CACHE_TYPE = 'simple'
    SOME_KEY = 'some_value'

class TestApp (unittest.TestCase):
    def test_create_app(self):
        test_app = factory.AppFactory('testing').create_app(TestConfig)
        self.assertIsInstance(test_app, flask.Flask)
        self.assertEqual(test_app.env, 'testing')
        self.assertEqual(test_app.config['SECRET_KEY'], 'some_secrecy_is_ok')
        self.assertEqual(test_app.config['CACHE_TYPE'], 'simple')

    def test_configure_app(self):
        app = flask.Flask(__name__)
        fact = factory.AppFactory('testing')
        fact.configure_app(app, TestConfig)
        self.assertTrue('SOME_KEY' in app.config)
        self.assertEqual(app.config['SOME_KEY'], 'some_value')
        self.assertTrue('CACHE_TYPE' in app.config)
        self.assertEqual(app.config['CACHE_TYPE'], 'simple')
        self.assertTrue('SECRET_KEY' in app.config)
        self.assertEqual(app.config['SECRET_KEY'], 'some_secrecy_is_ok')

    def test_configure_logging(self):
        app = flask.Flask(__name__)
        app.debug = True
        fact = factory.AppFactory('testing')
        fact.configure_logging(app, True)
        self.assertEqual(app.logger.level, logging.DEBUG)
        self.assertEqual(app.logger.handlers, [])

        app.debug = False
        app.config['LOG_SYSLOG_LEVEL'] = logging.WARNING
        fact.configure_logging(app, True)
        self.assertEqual(len(app.logger.handlers), 1)

        app.config['LOG_SMTP_LEVEL'] = logging.FATAL
        self.assertRaises(KeyError, fact.configure_logging, app, True)
        app.config['APP_MAIL_SUBJECT_PREFIX'] = 'Tests'
        app.config['APP_MAIL_SENDER'] = 'Project <project@example.org>'
        app.config['APP_ADMINS'] = ['project@example.org']
        app.config['MAIL_SERVER'] = 'smtp.example.org'
        app.config['MAIL_PORT'] = 25
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USERNAME'] = 'test_email'
        app.config['MAIL_PASSWORD'] = 'test_password'

        app.config['LOG_SYSLOG_LEVEL'] = logging.WARNING
        app.config['LOG_SMTP_LEVEL'] = logging.FATAL
        fact.configure_logging(app, True)
        self.assertEqual(len(app.logger.handlers), 2)

        app.testing = True
        fact.configure_logging(app)
        self.assertEqual(app.logger.level, logging.DEBUG)
        self.assertEqual(len(app.logger.handlers), 4, "won't clear previous handlers unless requested")



