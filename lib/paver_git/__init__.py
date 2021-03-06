"""
  paver.ext.git
  ~~~~~~~~~~~~~

  paver extension to automate git.


  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from paver.easy import options as opts, task
from paver.ext.utils import sh


__all__ = [
  "submodule_init", "submodule_update", "current_branch", "tags",
]


@task
def submodule_update():
  """
  """
  return sh("git submodule update", cwd=opts.proj.dirs.base)


@task
def submodule_init():
  """
  """
  return sh("git submodule init", cwd=opts.proj.dirs.base)


def tags():
  """
    :returns: list of strings for git tags sorted by authordate.
  """
  return sh(
    "git for-each-ref --sort='*authordate' --format='%(tag)' refs/tags",
    capture=True, cwd=opts.proj.dirs.base).splitlines()


def current_branch():
  """
    :returns: the latest version number from git tags.
  """
  value = sh(
    "git rev-parse --abbrev-ref HEAD",
    capture=True, cwd=opts.proj.dirs.base).splitlines()[0]
  return value
