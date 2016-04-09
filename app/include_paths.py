"""
  app.include_paths
  ~~~~~~~~~~~~~~~~~

  adds the library directory locations to the include path.


  :copyright: (c) 2016 by gregorynicholas.
"""
from __future__ import unicode_literals
import logging
import os
import sys


def insert(path):
  if path not in sys.path:
    logging.info("adding path to system includes path: %s", path)
    sys.path.insert(0, str(path))


# allow unzipped packages to be imported by adding the lib dir to sys.path.
# this inserts the lib directory to the front, so google app engine will
# pickup local 3rd party libraries first.
lib_path = os.path.abspath("lib")
insert(lib_path)
insert("lib")


# install zip archives to path for zipimport..
for f in [f for f in os.listdir(lib_path) if f.endswith((".zip", ".egg"))]:
  insert("lib/{}".format(f))

# https://github.com/russomi/ferris-framework/blob/master/fix_imports.py
# fix jinja2 debugging on local environment
# todo: causing issues with dev_appserver2
# if os.environ.get("SERVER_SOFTWARE", "").upper().startswith("DEV"):
#   logging.info('enabling jinja2 debugging.')
#   from google.appengine.tools.dev_appserver import HardenedModulesHook
#   HardenedModulesHook._WHITE_LIST_C_MODULES += ["_ctypes", "gestalt"]
