"""
project.config
----------------
Defines configuration classes
"""

import os
import logging
from . import BASE_PATH

class Config:
    APP_MAIL_SUBJECT_PREFIX = '[PROJECT]'
    APP_MAIL_SENDER = 'Project Name <project@example.org>'
    APP_ADMINS = ['Admin <admin@example.org>']
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some_secure_random_string'
    FORCE_SSL = False
    AUTH_TOKEN_TTL = 3600
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    CACHE_TYPE = 'simple'
    CACHE_NO_NULL_WARNING = True
    CACHE_DEFAULT_TIMEOUT = 30
    MAIL_SERVER = 'smtp.example.org'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    LOG_SYSLOG_LEVEL = logging.INFO
    LOG_SMTP_LEVEL = None
    LOG_FILE_PATH = None
    LOG_FILE_LEVEL = None
    PROXY_LAYERS = 1

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_SYSLOG_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(BASE_PATH, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(BASE_PATH, 'data-test.sqlite')

class ProductionConfig(Config):
    FORCE_SSL = True
    CACHE_NO_NULL_WARNING = False
    LOG_SMTP_LEVEL = logging.ERROR
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(BASE_PATH, 'data.sqlite')

env_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

__all__ = ('Config', 'DevelopmentConfig', 'TestingConfig', 'ProductionConfig', 'env_config')
