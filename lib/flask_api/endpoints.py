"""
  flask.ext.api.endpoints
  ~~~~~~~~~~~~~~~~~~~~~~~

  there's no need to be so verbose in building rest api services for internal
  apps.


  :copyright: (c) 2016 by gregorynicholas.
"""
from __future__ import unicode_literals
from os import listdir
from os import path as ospath
from flask import Blueprint
from flask.ext.api.wtf import form_endpoint
from logging import getLogger


__all__ = [
  "Endpoints", "register", "discover_endpoints",
  "form_endpoint",
]

logger = getLogger(__name__)


class Endpoints(Blueprint):
  """
  represents an api Endpoints blueprint. functions exactly like a
  `flask.blueprints.Blueprint`, except that it's designed to work with wtfforms
  extension.
  """

  def __init__(self, name, import_name, **kw):
    self.logger = getLogger(import_name)
    Blueprint.__init__(self, name=name, import_name=import_name, **kw)

  def endpoint(self, *args, **kw):
    """
    flask route decorator for api endpoints.
    """
    methods = kw.pop("methods", ["POST", "GET"])
    return self.route(*args, methods=methods, **kw)

  def form(self, form, *args, **kw):
    """
    flask route decorator for wtform enabled api endpoints.
    """
    return form_endpoint(form_class=form, *args, **kw)

  def remote_endpoint(self, *args, **kw):
    """
    flask route decorator for api endpoints that allows for CORS requests.
    """
    methods = kw.pop("methods", ["POST", "GET", "OPTIONS"])
    return self.route(*args, methods=methods, **kw)


def register(endpoints_blueprint, url_prefix, subdomains=None):
  """
  registers a dict for the arguments required to instantiate + register api
  `flask.Blueprint` endpoints to a `flask.Flask` application.

    :param endpoints_blueprint:
    :param url_prefix:
    :param subdomain:
  """
  rv = []

  if subdomains:
    for subdomain in subdomains:
      rv.append(dict(
        blueprint=endpoints_blueprint,
        url_prefix=url_prefix,
        subdomain=subdomain))
      logger.info("appending the subdomain-based blueprint: %s", rv)

  else:
    # register the api blueprint sans subdomain
    # fixes issues between using localhost and appengine subdomains..
    rv.append(dict(
      blueprint=endpoints_blueprint,
      url_prefix=url_prefix))
    logger.info("appending the sans-subdomain blueprint: %s", rv)

  return rv


def discover_endpoints(file, pkg):
  """
  scans a directory of modules and gets a list of the `flask.ext.api.Endpoints`
  defined in each. for automatically registering as blueprints onto a flask
  application.

  on gae, this scan + lookup will be cached on initial module import.

    :param file:
    :param pkg:
    :returns: list of dicts for the `flask.ext.api.Endpoints`
  """
  api_module_suffix = "_api"
  mods = listdir(ospath.dirname(file))
  rv = []
  for modname in [_ for _ in mods if _.endswith(api_module_suffix + ".py")]:
    mod = __import__(
      "{}.{}".format(pkg, modname[:-3]), globals(), locals(), ["endpoints"])
    if hasattr(mod, "endpoints"):
      rv.extend(mod.endpoints)
  return rv
