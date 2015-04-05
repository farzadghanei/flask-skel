import os
import unittest
import flask
import project

try:
    from importlib import reload
except ImportError:
    pass

class TestAppInit (unittest.TestCase):
    def test_app(self):
        os.environ['APP_ENV'] = 'testing'
        reload(project)
        self.assertIsInstance(project.app, flask.Flask)
        self.assertEqual(project.app.env, 'testing')
        self.assertTrue(project.app.testing)
        self.assertTrue(project.app.config['TESTING'])
        os.environ['APP_ENV'] = 'development'
        reload(project)
        self.assertIsInstance(project.app, flask.Flask)
        self.assertEqual(project.app.env, 'development')
        self.assertTrue(project.app.debug)
        os.environ['APP_ENV'] = 'production'
        reload(project)
        self.assertIsInstance(project.app, flask.Flask)
        self.assertEqual(project.app.env, 'production')
        self.assertFalse(project.app.debug)
        self.assertFalse(project.app.testing)