"""
  paver.ext.project
  ~~~~~~~~~~~~~~~~~

  load project settings.


  :copyright: (c) 2016 by gregorynicholas.
"""
from __future__ import unicode_literals
from os import environ
from paver.ext.utils import yaml_load
from paver.ext.utils import rbunch
from paver.ext.utils import rpath
from paver.easy import Bunch
from paver.easy import path as pth
from paver.easy import options as opts


__all__ = ["proj"]


def load(config_path):
  """
  initialize the project config from yaml definition.

    :param config_path:
  """
  p = yaml_load(config_path)["project"]
  rv = Bunch(**rbunch(p))
  rv.dirs = Bunch(**rpath(p["dirs"]))
  # add virtualenv paths..
  rv.dirs.venv = pth(environ.get("VIRTUAL_ENV", ".virtualenvs/" + p['virtualenv_id']))
  return rv


#: shorthanded to `proj`
proj = load("build/project.yaml")

# set the `proj` var in the paver environment..
opts(proj=proj)
