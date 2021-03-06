"""
  paver.ext.release
  ~~~~~~~~~~~~~~~~~

  automate release deployments.


  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
# from paver.easy import sh
from paver.easy import options as opts
from paver.ext import git


__all__ = ["version_tag_id", "dist_version_id"]


def version_tag_id():
  """
    :returns: string version number of the newest git tag
  """
  tags = git.tags()
  if len(tags) < 1:
    rv = "0.0.0"
  else:
    rv = tags[-1].strip()
  return rv


def dist_version_id():
  """
  gets the version number from git, and modifies to convert from float string
  to a string, so it can be used as part of a subdomain.

    :returns: string
  """
  rv = git.current_branch()
  # todo: move this list to project.yaml
  if rv not in ["develop", "master", "testing"]:
    return rv
  return "v" + version_tag_id().replace(".", "-")


def write_ver_id(ver_id):
  """
  writes the current version identifier (branch name for branch
  deployments, last tag for qa/prod) to app/__init__.py
  """
  ver_file = open(opts.proj.dirs.dist / "app" / "version.py", "w+")
  ver_file.write("__version__ = \"{}\"\n".format(ver_id))
