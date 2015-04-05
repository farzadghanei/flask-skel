'''
project.services
'''

class BaseService(object):
    def __init__(self, logger, config={}):
        self.logger = logger
        self.config = config

__all__ = (
    'user',
    'BaseService'
)