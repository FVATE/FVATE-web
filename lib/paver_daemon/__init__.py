"""
  paver.ext.daemon
  ~~~~~~~~~~~~~~~~

  make working with daemons easier.


  :copyright: (c) 2016 by gregorynicholas.
"""
from __future__ import unicode_literals
from os import kill as os_kill
from paver.ext.utils import sh, rm


__all__ = ["nohup", "kill", "is_pid_running"]


def nohup(command, pid, *a, **kw):
  """
  capture the process id, so we can manage by saving the process.

    :param command: command string to run.
    :param pid: instance of a `paver.easy.path` object for a process id
    :param append: boolean.
  """
  append = kw.pop("append", False)
  if append:
    append = '>>'
  else:
    append = '>'
  stderr = "{}.err".format(pid.name)
  stdout = "{}.out".format(pid.name)
  try:
    run = """
    nohup {cmd} {append}{stderr} 2{append}{stdout} &
    pid=$!
    echo $pid > {pid}
    """.format(
      cmd=command,
      stderr=stderr,
      stdout=stdout,
      append=append,
      pid=pid)
    return sh(run, *a, **kw)
  except Exception, e:
    raise RunProcessFailure("""
  an error occurred starting the process:
    {}
  """.format(e))


class RunProcessFailure(ValueError):
  """
  """


class ProcessNotFound(ValueError):
  """
  """


class ProcessNotRunning(ValueError):
  """
  """


def _osx_find_process(pid):
  """
    :param pid: instance of a `paver.easy.path` object for a process id
  """
  return sh(
    'ps -ef | grep "%s" | awk "{print $2}" ' % pid.name,
    capture=True).strip().split(' ')[1]


def _kill(pidv):
  """
    :param pidv: int for a process id
  """
  return sh(
    "kill -9 {pid}",
    pid=pidv, error=True, capture=True)


def kill(pid):
  """
  kill a background process by it's pid file. only really tested for OSX.

    :param pid: instance of a `paver.easy.path` object for a process id
  """
  try:
    if not is_pid_running(pid):
      raise ProcessNotRunning("""
process not running: {}
""".format(pid))

    pidv = _parse_pid_value(pid)
    rv = _kill(pidv)
    if "no such process" in rv.lower():
      raise ProcessNotFound("""
  process not found: {}
  """.format(pidv))
  except (ProcessNotRunning):  # ignore..
    pass
  except (ProcessNotFound, IOError):
    try:
      # todo: this only works on osx..
      _kill(_osx_find_process(pid.name))
    except Exception, e:
      print type(e), e
  finally:
    rm(pid)


def _parse_pid_value(pid):
  """
    :param pid: instance of a `paver.easy.path` object for a process id
  """
  if not pid.isfile():
    return None
  rv = pid.text().strip()
  try:
    rv = int(rv)
  except Exception, e:
    print type(e), e
    rv = -1
  return rv


def is_pid_running(pid):
  """
  sending signal 0 to a process will raise an OSError if the
  process is not running and do nothing otherwise.

    :param pid: instance of a `paver.easy.path` object for a process id
    :returns: True if a process with given process id is running
  """
  pidv = _parse_pid_value(pid)
  if pidv is None:
    return False
  try:
    os_kill(pidv, 0)
  except OSError:
    return False
  else:
    return True
