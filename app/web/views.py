"""
  app.web.views
  ~~~~~~~~~~~~~

  this is the base module that will serve the app's views.


  :copyright: (c) 2016 by gregorynicholas.
"""
from __future__ import unicode_literals
from logging import getLogger
from json import dumps
from flask import render_template, redirect, Response, session, request
from flask.ext import login
from flask.ext import login_auth
from flask.ext import templated
from app.main import flaskapp
from app.web import auth
from app.web import jinjaenv
# from app import models
from app.models import user


log = getLogger(__name__)
log.info("starting views.")

# jinja2 template configuration
jinjaenv.register_filters(flaskapp)
jinjaenv.register_globals(flaskapp)


def render_template_with_session(template, **kw):
  if login.current_user.is_authenticated():
    _session = login.current_user.session_dict()
  else:
    _session = flaskapp.jinja_env.globals["_session"]
  flaskapp.jinja_env.globals["_session"] = dumps(_session)
  return render_template(template, **kw)


@flaskapp.route("/", subdomain="<subdomain>", methods=["GET"])
@templated.render("index.html")
def index_get(subdomain=None):
  log.info('request: %s', request)
  return {}


@flaskapp.route("/favicon.ico", subdomain="<subdomain>", methods=["GET"])
def favicon(subdomain=None):
  return Response("", 200)


@flaskapp.route("/login", methods=["GET"])
@templated.render("login.html")
def login_get():
  if login.current_user.is_authenticated():
    return redirect("/")
  return {}


@flaskapp.route("/logout", methods=["GET"])
def logout_get():
  login.logout_user()
  sess = session._get_current_object()
  sess["remember"] = "clear"
  sess.regenerate()
  return redirect("/")


@flaskapp.route("/admin", methods=["GET"])
@login_auth.required
@login_auth.requires_roles("admin")
@templated.render("login.html")
def admin_get():
  if login.current_user.is_authenticated():
    return redirect("/")
  return {}


@flaskapp.route("/test_signin", methods=["GET"])
def test_signin_get():
  u = user.User.get_by_id("testing")  # todo
  u.roles = ["admin"]
  flask_user = auth.FlaskUser(u)
  rv = login.login_user(flask_user, remember=True)
  return Response(rv)


# appengine fix for serving .MP4 files
# see: http://stackoverflow.com/questions/19242670/google-app-engine-cannot-serve-some-of-mp4-files
# see: http://stackoverflow.com/questions/3811595/flask-werkzeug-how-to-attach-http-content-length-header-to-file-download
@flaskapp.after_request
def after_request(response):
  if 'HTTP_RANGE' in request.headers:
    response.headers['X-AppEngine-BlobRange'] = request.headers['HTTP_RANGE']

  response.headers.add(str('Access-Control-Allow-Origin'), '*')
  return response
