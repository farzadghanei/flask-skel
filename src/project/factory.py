'''
project.factory
-----------------
provides factory classes
'''

import logging
from logging.handlers import SMTPHandler

from flask import Flask, request, render_template
from flask.ext.sslify import SSLify
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.babel import Babel

from .models.user import User
from .frontend import frontend
from .api_v1 import api_v1
from .extensions import db, mail, cache, login_manager

class AppFactory(object):
    @staticmethod
    def default_blueprints():
        return (
            frontend,
            api_v1
        )

    def __init__(self, env='development', instance_path=None):
        self.env = env
        self.instance_path = instance_path

    def create_app(self, config=None, app_name=None, blueprints=None):
        if app_name is None:
            app_name = 'project name'
        if blueprints is None:
            blueprints = self.default_blueprints()

        app = Flask(app_name, instance_path=self.instance_path, instance_relative_config=True)
        app.env = self.env
        self.configure_app(app, config)
        self.configure_blueprints(app, blueprints)
        self.configure_extensions(app)
        self.configure_logging(app)
        self.configure_template_filters(app)
        self.configure_error_handlers(app)
        self.configure_web_settings(app)
        return app

    @staticmethod
    def configure_app(app, config=None):
        if config is not None:
            app.config.from_object(config)
        # load config from instance path if any
        app.config.from_pyfile('production.cfg', silent=True)

    @staticmethod
    def configure_extensions(app):
        db.init_app(app)
        mail.init_app(app)
        cache.init_app(app)
        babel = Babel(app)

        @babel.localeselector
        def get_locale():
            accept_languages = app.config.get('ACCEPT_LANGUAGES')
            return request.accept_languages.best_match(accept_languages)

        @login_manager.user_loader
        def load_user(id):
            return User.query.get(id)

        login_manager.setup_app(app)

    @staticmethod
    def configure_blueprints(app, blueprints):
        for blueprint in blueprints:
            app.register_blueprint(blueprint)

    @staticmethod
    def configure_logging(app, clear_handlers=False):
        conf = app.config
        if clear_handlers:
            for handler in app.logger.handlers:
                app.logger.removeHandler(handler)
        if app.debug or app.testing:
            app.logger.setLevel(logging.DEBUG)
        else:
            app.logger.setLevel(logging.INFO)
        if 'LOG_SYSLOG_LEVEL' in conf and conf['LOG_SYSLOG_LEVEL'] is not None:
            handler = logging.handlers.SysLogHandler()
            handler.setLevel(conf['LOG_SYSLOG_LEVEL'])
            app.logger.addHandler(handler)

        if 'LOG_FILE_PATH' in conf and conf['LOG_FILE_PATH'] is not None \
                and 'LOG_FILE_LEVEL' in conf and conf['LOG_FILE_LEVEL'] is not None:
            handler = logging.handlers.RotatingFileHandler(
                conf['LOG_FILE_PATH'],
                maxBytes=conf.get('LOG_FILE_MAX_BYTES', 100000),
                backupCount=conf.get('LOG_FILE_BACKUP_COUNT', 10)
            )
            handler.setLevel(conf.get('LOG_FILE_LEVEL', logging.INFO))
            handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]')
            )
            app.logger.addHandler(handler)

        if 'LOG_SMTP_LEVEL' in conf and conf.get('LOG_SMTP_LEVEL') is not None:
            handler = SMTPHandler(app.config['MAIL_SERVER'],
                                  app.config['APP_MAIL_SENDER'],
                                  app.config['APP_ADMINS'],
                                  app.config['APP_MAIL_SUBJECT_PREFIX'] + ' Error',
                                  (app.config['MAIL_USERNAME'],
                                   app.config['MAIL_PASSWORD']))
            handler.setLevel(conf['LOG_SMTP_LEVEL'])
            handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]')
            )
            app.logger.addHandler(handler)

    @staticmethod
    def configure_error_handlers(app):
        @app.errorhandler(403)
        def forbidden_page(error):
            return render_template("errors/403.html"), 403

        @app.errorhandler(404)
        def page_not_found(error):
            return render_template("errors/404.html"), 404

        @app.errorhandler(500)
        def server_error_page(error):
            return render_template("errors/500.html"), 500

    @staticmethod
    def configure_web_settings(app):
        conf = app.config
        if 'PROXY_LAYERS' in conf and conf['PROXY_LAYERS']:
            app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=conf['PROXY_LAYERS'])

        if not app.debug and not app.testing and conf.get('FORCE_SSL'):
            sslify_config = {}
            if 'SSL_AGE' in conf:
                sslify_config['age'] = conf['SSL_AGE']
            if 'SSL_SUBDOMAINS' in conf:
                sslify_config['subdomains'] = conf['SSL_SUBDOMAINS']
            sslify = SSLify(app, **sslify_config)

__all__ = ('AppFactory',)