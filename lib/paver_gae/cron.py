"""
  paver.ext.gae.cron
  ~~~~~~~~~~~~~~~~~~

  paver extension to automate app engine.


  :copyright: (c) 2016 by gregorynicholas.
"""
from __future__ import unicode_literals
from paver.easy import options as opts
from paver.easy import task
from paver.ext.gae import descriptor
from paver.ext.utils import sh


__all__ = ["crons"]


def get_crons():
  """
    :returns: list of Bunch objects for each descriptor config.
  """
  return descriptor.cron(opts.proj.dirs.dist)


@task
def crons():
  # todo: yaml dump
  print get_crons()
