"""
  app.main
  ~~~~~~~~

  the main entry point into the application.


  :copyright: (c) 2016 by gregorynicholas.
"""
from __future__ import unicode_literals

# logging setup..
import logging
logging.basicConfig(level=logging.INFO)
logging.logMultiprocessing = 0
log = logging.getLogger()
log.setLevel(logging.INFO)

# add lib/ dir to the system include paths..
import app.include_paths
from flask import Flask
from app.config import config

log.info("starting application.")
log.info("config: %s, SERVER_NAME: %s.", config, config.SERVER_NAME)

# setup signals namespace..
from blinker import Namespace
signals = Namespace()
app_setup_signal = signals.signal("app-setup")

from google.appengine.ext import ndb
ndb.utils.DEBUG = False  # stfu ndb.

#: the variable `flaskapp` is the entry point from uwsgi.
#: NOTE: the `template_folder` arg is relative to the location of
#  the file containing the flask app instantiation
flaskapp = Flask(__name__, template_folder="web/templates")

# intitialize the authentication extension. note: this is exec'd before the
# config of the flask application is done
from app.web.auth import Auth
auth = Auth(flaskapp)

flaskapp.debug = config.DEBUG
flaskapp.config.from_object(config)
flaskapp.secret_key = config.flask_secret_key
flaskapp.config.update(
  SESSION_COOKIE_SECURE=config.flask_session_cookie_secure,
  REMEMBER_COOKIE_DOMAIN=config.SESSION_COOKIE_DOMAIN,
  REMEMBER_COOKIE_NAME=config.flask_remember_cookie_name,
)

# if config.env_id == "local":
#   try:
#     from flask.ext.gae_mini_profiler import GAEMiniProfiler
#     GAEMiniProfiler(flaskapp)
#   except:
#     pass

from app import models
models.init(flaskapp)

app_setup_signal.send(flaskapp)

# sentry configuration
if config.sentry_dsn and config.sentry_dsn != '':
  from raven.contrib.flask import Sentry
  sentry = Sentry(dsn=config.sentry_dsn)
  sentry.init_app(flaskapp)
  log.info("sentry initialized with config {}".format(config.sentry_dsn))

# import routes module to instantiate the web routes..
from app.web import errors
from app.web import views
from app.web.api import Api
api = Api(flaskapp)
