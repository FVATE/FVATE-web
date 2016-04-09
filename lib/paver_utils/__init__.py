"""
  paver.ext.utils
  ~~~~~~~~~~~~~~~

  hoping to make life easier for every engineer.


  :copyright: (c) 2016 by gregorynicholas.
"""
from __future__ import unicode_literals
import os
import codecs
import shutil
import time
import tempfile
import urllib2
import yaml
from paver.easy import BuildFailure
from paver.easy import Bunch
from paver.easy import path
from paver.easy import sh2 as sh
from paver.easy import task


__all__ = [
  "sh", "sym", "rm", "wget", "extract", "file_to_utf8",
  "ping", "osx_clear", "yaml_load", "rbunch", "rpath",
]


class InvalidArchiveFile(BuildFailure):
  """
  """


def rm(*paths):
  """
  fucking sick of how tedious it is to make a simple `rm` call.
  """
  for p in paths:
    sh("rm -rf {}", p)
  return paths


def wget(src, dest, callback=None):
  """
    :param src: instance of a `paver.easy.path` object.
    :param dest: instance of a `paver.easy.path` object.
    :param callback (todo): move the DL to non-blocking, and invoke
      callback function on done.
  """
  return sh("wget {}", src, err=True, cwd=dest)


def curl(src, dest, callback=None):
  """
    :param src: instance of a `paver.easy.path` object.
    :param dest: instance of a `paver.easy.path` object.
    :param callback (todo): move the DL to non-blocking, and invoke
      callback function on done.
  """


def archive(src, dest, format="zip"):
  """
  create an archive file (eg. zip or tar).

    :param format: "zip", "tar", "bztar" or "gztar"
  """
  shutil.make_archive(
    base_name=dest.name,
    format=format,
    root_dir=dest.abspath(),
    base_dir=src)
  return src


def extract(archive, dest):
  """
  extract an archive, any archive.

    :param archive: instance of a `paver.easy.path` object.
    :param dest: instance of a `paver.easy.path` object.
  """
  if archive.endswith(".zip"):
    run = "unzip {archive}"
  elif archive.endswith(".tar"):
    run = "tar xvzf {archive}"
  elif archive.endswith(".tar.gz"):
    run = "tar -zxvf {archive}"
  else:
    raise InvalidArchiveFile("""
  unable to extract archive, unsupported format:
    {}
  """.format(archive))
  return sh(run, archive=archive, cwd=dest)


def file_to_utf8(file_path, replacements):
  """
  replaces contents of a file with utf-8 encoded text.

    :param file_path: instance of a `paver.easy.path` object.
    :param replacements:
  """
  return _replace_in_file(file_path, replacements)


def _replace_in_file(file_path, replacements):
  """
  replaces contents of a file with utf-8 encoded text.

    :param file_path: instance of a `paver.easy.path` object.
    :param replacements:
  """

  def _replace(_line, _orig, _replace):
    return _line.replace(_orig, _replace).encode("utf-8")

  tmp, tmp_path = tempfile.mkstemp()
  with open(tmp_path, "wb") as f1:
    with codecs.open(file_path, "r", "utf-8") as f2:
      for line in f2:
        for (orig, new) in replacements.iteritems():
          f1.write(_replace(line, orig, new))
  os.close(tmp)
  rm(file_path)
  path(tmp_path).move(file_path)


def sym(src, dest):
  """
  symlinks a path, overwriting if the destination already exists.

    :param src: instance of a `paver.easy.path` object.
    :param dest: instance of a `paver.easy.path` object.
  """
  rm(dest)
  src.symlink(dest)


class PingError(ValueError):
  """
  """


def ping(url, retries=15, sleep=2):
  """
  makes http requests to a url until it responds with a 200-299 status.

    :param url: string url to ping
    :param retries: maximum number of retries to attempt
    :param sleep: number of seconds to sleep between retries
  """
  for _ in range(retries):
    try:
      urllib2.urlopen(url)
      break
    except urllib2.URLError:
      print "can't connect to local appengine server.. will retry.."
    time.sleep(sleep)
  else:
    raise PingError("""
  maximum number of retries reached
  """)


def yaml_load(path):
  """
    :param path: instance of a `paver.easy.path` object.
  """
  with open(path, "r") as f:
    rv = yaml.safe_load(f)
  return rv


def rpath(d):
  """
  recursively Bunch a dict, converting string values to `paver.easy.path`.

    :param d: instance of a dict.
  """
  rv = {}
  if isinstance(d, dict):
    for k, v in d.iteritems():
      if isinstance(v, dict):
        rv[k] = Bunch(**rpath(v))
      elif isinstance(v, basestring):
        if v.startswith("~"):
          v = os.path.expanduser(v)
        rv[k] = path(v)
  return rv


def rbunch(d):
  """
  recursively Bunch dict values.

    :param d: instance of a dict.
  """
  rv = {}
  if isinstance(d, dict):
    for k, v in d.iteritems():
      rv[k] = Bunch(**rbunch(v)) if isinstance(v, dict) else v
  return rv


@task
def osx_clear():
  """
  invokes an applescript to clear the terminal screen. same as pressing cmd+k
  """
  osascript(
    'tell application "System Events" to tell process '
    '"Terminal" to keystroke "k" using command down')


def osascript(script):
  """
  executes applescripts and other osa language scripts
  """
  return sh(
    "/usr/bin/open -a Terminal /usr/bin/osascript -e '{script}'",
    script=script.replace('"', '\"'))
