"""
  app.models
  ~~~~~~~~~~

  data models package.


  :copyright: (c) 2016 by gregory nicholas.
"""
from __future__ import unicode_literals
from logging import getLogger
log = getLogger(__name__)


# intitialize mongoengine + mongodb..
try:
  from flask.ext.mongoengine import MongoEngine
  from mongoengine.connection import ConnectionError
except Exception:
  # stub the mongoengine packge..
  class ConnectionError(Exception):
    """
    """

  class Namespace(object):
    def __init__(self, *args, **kw):
      pass

  class MongoEngine(object):
    Document = Namespace
    BooleanField = Namespace
    ListField = Namespace
    IntField = Namespace
    ObjectIdField = Namespace
    StringField = Namespace

    def init_app(self, *args, **kw):
      pass
finally:
  db = MongoEngine()


def init(flaskapp):
  """
  only if there's a mongodb connection..
  """
  # try:
  #   db.init_app(flaskapp)
  # except ConnectionError, e:
  #   log.warn("unable to connect to mongo database: %s", e)
