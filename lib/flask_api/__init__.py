"""
  flask.ext.api
  ~~~~~~~~~~~~~

  making rest api's in flask applications easier.

  there's no need to be so verbose in building rest api services for internal
  apps.


  :copyright: (c) 2016 by gregorynicholas.
"""
from __future__ import unicode_literals
__import__("pkg_resources").declare_namespace(__name__)


#: alias core extension modules + objects for "convenience"..
from flask_wtf import Form
from wtforms import fields
from wtforms import ValidationError
from wtforms import validators

# TODO: list imports..
from wtforms.fields import *
from wtforms.validators import *
from wtforms.widgets import *

#: loads the `register` method
from flask.ext.api.endpoints import *
from flask.ext.api.endpoints import discover_endpoints
from flask.ext.api.exceptions import FieldValidationError


__all__ = [
  "Form", "ValidationError", "FieldValidationError", "fields", "validators",
]

__all__ += [
  'discover_endpoints',
]
