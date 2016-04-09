"""
  app.models.user
  ~~~~~~~~~~~~~~~

  :copyright: (c) 2016 by gregorynicholas.
"""
from __future__ import unicode_literals
from app.models import db


__all__ = ['User']


class User(db.Document):
  """
  User model.
  """

  key = db.StringField()
  active = db.BooleanField(default=True)
  roles = db.ListField(db.StringField())

  @classmethod
  def find_by_email(cls, email):
    result = cls()
    result.update({
      'key': 'abc123',  #: TODO
      'active': True,
      'name': 'testing',
      'email': 'test@test.com'})
    return result

  @classmethod
  def get_by_id(cls, id):
    result = cls()
    result.save(**{
      'key': 'abc123',  #: TODO
      'active': True,
      'name': 'testing',
      'email': 'test@test.com'})
    return result

  def is_in_role(self, role):
    return True
