#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import unittest
import coverage
from werkzeug.contrib.profiler import ProfilerMiddleware

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
COVERAGE_ENV = 'APP_COVERAGE'

app_test_cover = None
if os.environ.get(COVERAGE_ENV):
    app_test_cover = coverage.coverage(branch=True, include=os.path.join(BASE_PATH, 'project/*'))
    app_test_cover.start()

if os.path.exists('.env'):
    print('Importing environment from .env ...')
    with open('.env') as dot_env:
        for line in dot_env:
            key, val  = [v.strip() for v in line.strip().split('=', 1)]
            os.environ[key] = val

from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from project import app
from project.models import *
from project.extensions import db

manager = Manager(app)
migrate = Migrate(app)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('migrate', MigrateCommand)

@manager.command
def coverage(verbosity=2):
    if not os.environ.get(COVERAGE_ENV):
        os.environ[COVERAGE_ENV] = 'coverage'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    tests = unittest.defaultTestLoader.discover(os.path.join(BASE_PATH, 'tests'))
    unittest.TextTestRunner(verbosity=verbosity).run(tests)
    if app_test_cover:
        app_test_cover.stop()
        app_test_cover.save()
        print('Coverage Report')
        app_test_cover.report()
        coverage_path = os.path.join(BASE_PATH, os.path.join('tmp', 'coverage'))
        app_test_cover.html_report(directory=coverage_path)
        print('HTML version: file://{0}/index.html'.format(coverage_path))
        app_test_cover.erase()

@manager.command
def profile(length=25, profile_dir=None):
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                    profile_dir=profile_dir)
    app.run()

if __name__ == '__main__':
    manager.run()
