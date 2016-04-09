"""
  paver.ext.gae.appcfg
  ~~~~~~~~~~~~~~~~~~~~

  helper for working with the appcfg.py app engine sdk cli.


  :copyright: (c) 2015 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from paver.easy import options as opts
from paver.ext.utils import sh


__all__ = ["appcfg"]


def appcfg(command, **kw):
  """
  wraps the app engine `appcfg.py` command with common parameters.

    :param command: string command to execute + run
  """
  err = kw.pop("error", False)
  cap = kw.pop("capture", False)
  cwd = kw.pop("cwd", opts.proj.dirs.base)
  _cwd = cwd
  backend_name = kw.pop("backend_name", "")
  # a bit of trickery because gae decided to have some weirdness in the way
  # it invokes commands for backends operations..
  if backend_name and backend_name != "":
    _cwd = ""
  kw.setdefault("skip_sdk_update_check", True)
  return sh(
    'echo "{password}" | '
    '{gae_sdk}/appcfg.py {command} . {backend_name} {flags} '
    '--email={email} --passin ',
    command=command,
    flags=_to_flags(kw),
    backend_name=backend_name,
    email=opts.proj.email,
    password=opts.proj.password,
    gae_sdk=opts.gae.sdk.root,
    cwd=cwd, _cwd=_cwd,
    error=err,
    capture=cap)


def _to_flags(d):
  rv = []
  for k, v in d.iteritems():
    if v is (None or True):
      rv.append(" --{} ".format(k))
    else:
      rv.append(" --{}={} ".format(k, v))
  return "".join(rv)
