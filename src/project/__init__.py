import os

APP_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(APP_PATH)
INSTANCE_FOLDER_PATH = os.path.join(BASE_PATH, 'instance')
ENV = os.environ.get('APP_ENV', 'development')

from .config import env_config

Config = env_config.get(ENV, 'development')

from .factory import AppFactory
app = AppFactory(ENV, INSTANCE_FOLDER_PATH).create_app(Config)

__all__ = (
    'factory', 'models', 'exceptions', 'extensions',
    'APP_PATH', 'BASE_PATH', 'INSTANCE_FOLDER_PATH',
    'Config', 'app'
)
