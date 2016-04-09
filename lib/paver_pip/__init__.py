"""
  paver.ext.pip
  ~~~~~~~~~~~~~

  automate pip.


  :copyright: (c) 2016 by gregorynicholas.
"""
from __future__ import unicode_literals
from pprint import pformat
from paver.easy import options as opts
from paver.ext.utils import sh
from pkg_resources import Distribution  # TODO: add as alias to utils


__all__ = ["get_installed_top_level_files"]


def _normalize(name):
  """
    :param name:
  """
  # TODO: check for "egg" vs "dist"
  return name.split("==")[0].split("#egg=")[-1].replace("-", "_").lower()


def install(packages):
  sh("pip install -q {packages}",
     packages=" ".join(packages["runtime"]),
     cache=opts.proj.dirs.base / ".pip",
     cwd=opts.proj.dirs.base)


def get_installed_top_level_files(packages):
  """
    :param packages:
    :returns:
  """
  venv_sitepackages = opts.proj.dirs.venv / "lib/python2.7/site-packages"
  print '  venv-site-packages:', venv_sitepackages
  runtimes = [_normalize(_) for _ in packages]
  print '  runtimes:', pformat(runtimes)
  rv = []

  dirs = venv_sitepackages.walkdirs("*.*-info")
  for root in dirs:
    print root.name
    print '  root:', root

    dist = Distribution.from_location(root, basename=str(root.name))
    if not dist:
      print '  dist not found.. ', root.name
      continue

    print '  project:', dist.project_name

    _project_name = _normalize(dist.project_name)
    if _project_name not in runtimes:
      print '  .. skipping ', _project_name, ', not found in runtime dependencies'
      continue

    toplevels = (root / "top_level.txt").text().strip().split("\n")
    toplevels = filter_top_level_runtime_deps(toplevels)

    for top in toplevels:
      if not (venv_sitepackages / top).isdir():
        top += ".py"
        print '  top-level module:', top

      else:
        print '  top-level package:', top
        pass  # TODO: try to append an __init__ file

      rv.append(venv_sitepackages / top)
  return rv


def filter_top_level_runtime_deps(toplevels):
  rv = []

  for top in toplevels:
    if (top == "tests") or (top.startswith("tests") or top.endswith("tests")):
      continue

    rv.append(top)
  return rv
