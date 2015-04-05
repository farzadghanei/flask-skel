'''
project.models
----------------
Defines data model classes
'''

from ..extensions import db

class ModelMixin(object):
    id = db.Column(db.Integer, primary_key=True)

    def save(self, commit=False):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

__all__ = ('ModelMixin', 'user')
