"""
  app.web.errors
  ~~~~~~~~~~~~~~

  defines global flask exception handling, and binds error routes + views to
  the flask application.


  :copyright: (c) 2016 by gregorynicholas.
"""
from __future__ import unicode_literals
import traceback
from logging import getLogger
from pprint import pformat
from flask import Response, request
from jinja2 import TemplateNotFound
from app.main import flaskapp
from app.web.views import render_template_with_session


log = getLogger(__name__)
log.debug('Starting error handler.')


@flaskapp.errorhandler(404)
def page_not_found(error=None):
  """
  404 error handler.
  """
  log.warning(
    "page not found: %s %s %s %s %s",
    request.url,
    request.method,
    request.endpoint,
    request.url_rule,
    pformat(request.data))
  return render_template_with_session("404.html"), 404


@flaskapp.errorhandler(500)
def server_error_500(server_error):
  """
  500 error handler. if request is from ajax than return empty page.
  otherwise render template.
  """
  log.exception(traceback.format_exc())
  if request.is_xhr:
    return Response(status=500)
  else:
    return render_template_with_session("500.html"), 500


@flaskapp.errorhandler(TemplateNotFound)
def template_not_found(server_error):
  log.exception(traceback.format_exc())
  return Response("please fix your shit.", status=500)
