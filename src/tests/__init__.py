import sys
import os

os.environ['APP_ENV'] = 'testing'
TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
BASE_PATH = os.path.dirname(TESTS_PATH)
APP_PATH = os.path.join(BASE_PATH, 'project')

sys.path.insert(0, APP_PATH)
sys.path.insert(0, BASE_PATH)
sys.path.insert(0, TESTS_PATH)

from . import models

__all__ = ['test_factory', 'test_app_init']
__all__.extend(['tests.models.' + name for name in models.__all__])