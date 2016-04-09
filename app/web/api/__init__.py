"""
  app.web.api
  ~~~~~~~~~~~

  rest-api package, services internal apps.


  :copyright: (c) 2016 by gregorynicholas.
"""
from __future__ import unicode_literals
from logging import getLogger
import flask_api
import wtforms_json


__all__ = ["Api"]


log = getLogger(__name__)
wtforms_json.init()
_endpoints = flask_api.discover_endpoints(__file__, __package__)
log.info("starting web api: %s", _endpoints)


class Api(object):
  """
  initializes the web api interface.
  """

  def __init__(self, flaskapp):
    """
    attaches api endpoints (`flask.Blueprint`s) to the flask application.

      :param flaskapp: instance of a `flask.Flask` app
    """
    [flaskapp.register_blueprint(**_) for _ in _endpoints]
    log.info("registered api blueprints: %s", flaskapp)
