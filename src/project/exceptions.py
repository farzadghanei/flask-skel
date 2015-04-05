'''
project.exceptions
--------------------
Define application specific exception classes
'''

class AppError(Exception):
    pass

class ValidationError(AppError, ValueError):
    pass

__all__ = ('AppError', 'ValidationError')
