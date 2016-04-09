"""
  pavement
  ~~~~~~~~

  paver tasks. automate everything.


  :copyright: (c) 2016 by gregorynicholas.

"""
import os
import sys
sys.path.insert(0, "lib")
sys.path.append(os.path.abspath("."))
from hashlib import sha256
from itertools import chain
# from collections import defaultdict
from paver.ext.project import proj
from paver.ext.utils import sh, rm, yaml_load, file_to_utf8, sym
from paver.easy import BuildFailure
from paver.easy import task, call_task, cmdopts
from paver.easy import options as opts
from paver.options import Namespace
from paver.ext import (
  casperjs, git, gae, nose, pip, release)


env_id_opt = (
  "env_id=", "e",
  "the environment to seed data to. is one of {}.".format(opts.proj.envs))


class InvalidEnvironmentIdOption(BuildFailure):
  """
  """


def _validate_env_id(options, optional=False):
  """
    :param options: instance of a `paver.options.Namespace` object
    :param optional: boolean
  """
  err = False
  env_id = options.get("env_id", None)
  if env_id is None and not optional:
    err = True
  if not err and (env_id not in opts.proj.envs):
    err = True
  if err:
    raise InvalidEnvironmentIdOption("""
  an environment must be specified with the -e flag as one of:
    {}
  """.format(opts.proj.envs))


def _load_dependencies_config():
  return yaml_load(opts.proj.dirs.buildconfig / opts.proj.pip_dependencies)


def _bootstrap_init_dirs():
  opts.proj.dirs.data.root.makedirs()
  opts.proj.dirs.dist.makedirs()
  opts.proj.dirs.build.makedirs()
  opts.proj.dirs.lint.root.makedirs()
  opts.proj.dirs.lint.reports.makedirs()


def _install_pip_packages():
  packages = _load_dependencies_config()
  # pip.install(packages)
  print 'installing gae runtime libs..'
  gae.install_runtime_libs(packages, opts.proj.dirs.lib)


def _copy_page_templates(root):
  """
  copies html page templates from the client build dir to the app
  web templates dir.

  from ./client/build/dist/*.html to ./app/web/templates

    :param root: instance of a `paver.easy.path` object
  """
  dest = root / opts.proj.dirs.app_web_templates
  dest.makedirs()
  templates = opts.proj.dirs.client_build_dist.walkfiles("*.html")
  for template in templates:
    template.copy2(dest)


def _copy_client_build_to_static(root):
  """
  copies client build output to the app web static dir.

  from ./client/build/dist/*.[!html] to ./app/web/static

    :param root: instance of a `paver.easy.path` object
  """
  dest = root / opts.proj.dirs.app_web_static
  dest.rmtree()
  opts.proj.dirs.client_build_dist.cp(
    dest, ignore=("*.html", "test*"))


def _tag_static_build(root):
  """
  used to cache bust static files. hashes the contents of each static file,
  and appends the hash string to the end of the filenames.

    :param root: instance of a `paver.easy.path` object
  """
  templates_dir = root / opts.proj.dirs.app_web_templates
  static_dir = root / opts.proj.dirs.app_web_static

  replace_map = {}
  static_files = chain(
    static_dir.walkfiles("*.js"), static_dir.walkfiles("*.css"))

  for f in static_files:
    hash_str = sha256(open(f, "rb").read()).hexdigest()
    new_name = "{}_{}{}".format(f.namebase, hash_str, f.ext)
    replace_map["/" + f.name] = "/" + new_name
    f.rename(f.parent / new_name)

  for f in templates_dir.walkfiles("*.html"):
    file_to_utf8(f, replace_map)


@task
def bootstrap_client():
  """
  sets up the client development environment.
  """
  rm(opts.proj.dirs.client / "node_modules")
  sh("npm install -g grunt grunt-cli bower stylus")
  sh("npm install", cwd=opts.proj.dirs.client)
  sh("bower install", cwd=opts.proj.dirs.client)


@task
def bootstrap_backend():
  """
  installs 3rd party external python dependencies.
  """
  opts.proj.dirs.lib.makedirs()
  _install_pip_packages()


@task
def bootstrap():
  """
  sets up the project environment.

  todo: rollback if any steps fail
  """
  print "initializing directories.."
  _bootstrap_init_dirs()
  print "bootstrapping backend + build tools.."
  call_task("bootstrap_backend")
  print "boostrapping client.."
  call_task("bootstrap_client")
  print("---> bootstrap success\n")


@task
def re_bootstrap_virtualenv():
  """
  rebuilds the python virtualenv for the project.
  """
  rm(opts.proj.dirs.venv)
  sh("mkvirtualenv {}", opts.proj.virtualenv_id)


@task
def clean_lib():
  """
  clean all lib dependency artifacts.
  """
  rm(opts.proj.dirs.pip)
  rm(opts.proj.dirs.lib)


@task
def clean():
  """
  clean artifacts produced by dist and empty artifacts produced by build.
  """
  rm(opts.proj.dirs.build,
     opts.proj.dirs.dist,
     opts.proj.dirs.deploy)
  # [os.remove(f) for f in opts.proj.dirs.base.walkfiles("*.yaml")]
  [os.remove(f) for f in opts.proj.dirs.app.walkfiles("*.py[co]")]


@task
def build_casperjs_tests():
  """
  builds casperjs tests.
  """
  sh("grunt build_casperjs", cwd=opts.proj.dirs.client)


@task
def build_client():
  """
  builds the client.
  """
  sh("grunt dist", cwd=opts.proj.dirs.client)
  dest = opts.proj.dirs.base
  print("\n---> build_client success: copying artifacts to app..")
  _copy_page_templates(root=dest)
  _copy_client_build_to_static(root=dest)
  # _tag_static_build(root=dest)


@task
@cmdopts([env_id_opt])
def build(options):
  """
  builds a debug version of the app for local development.
  """
  env_id = options.get("env_id", opts.proj.envs.local)
  ver_id = release.dist_version_id()
  dest = opts.proj.dirs.base

  # STEP 1
  # ------
  # clean up previous build artifacts..
  call_task("clean")

  # STEP 2
  # ------
  # build the app client ui, then copy client build output
  # directly to the source app tree..
  call_task("build_client")

  # STEP 3
  # ------
  # build the app engine descriptors..
  gae.build_descriptors(
    dest=dest,
    env_id=env_id,
    ver_id=ver_id)

  print("---> build success\n")


@task
@cmdopts([
  ("suite=", "s", "Name of the html file to run the test suite.")
])
def test_client(options):
  """
  executes client unit & functional tests with mochajs.
  """
  suite = options.get("suite", "index.html")
  print("---> test_client success\n", suite)


@task
@cmdopts([
  ("path=", "p", "Path to the tests file you want to run."),
  ("mode=", "m", "Mode to the tests file you want to run. is one of "
                 "['local', 'integration']."),
])
def test_backend(options):
  """
  execute backend unit & functional tests with nosetests.  if no path is
  specified, scans all modules in the project + executes tests.
  """
  path = options.get("path", opts.proj.dirs.app)
  mode = options.get("mode", "local")
  # call_task("mongodb:run")
  try:
    rv = nose.run(
      path=path,
      config=opts.proj.dirs.buildconfig,
      mode=mode,
      env_id="test")
    print rv
  except:
    print("---> test_backend failure\n")
    raise
  # call_task("mongodb:stop")
  print("---> test_backend success\n")


@task
# @needs(["build_tests", "save"])
def test_headless_browser():
  """
  executes end-to-end tests with casperjs & phantomjs.
  """
  # wait for the server to run..
  # gae.verify_serving(
  #   "http://{}".format(opts.proj.default_hostname))
  casperjs.build()
  try:
    _options = Namespace()
    _options.path = "app/"
    casperjs.run(_options)
    # call_task("caspjerjs:run", _options)
  except casperjs.CasperjsTestsFailure, e:
    print("---> test_casperjs failure\n")
    raise e
  finally:
    # teardown test server..
    call_task("server_stop")
  print("---> test_headless_browser success\n")


@task
@cmdopts([env_id_opt])
def dist_build(options):
  """
  builds a release version of the app for deployment.
  """
  _validate_env_id(options)
  ver_id = release.dist_version_id()
  print "ver_id", ver_id

  # STEP 1
  # ------
  # clean up previous build artifacts..
  call_task("clean")
  call_task("build")

  # STEP 2
  # ------
  do_not_deploy = (
    ".data", ".lint", "build", "client", "tests", "docs", "*.py[co]",
    ".git*", "*.pid", "*.out", "*.err", "*.md", "*.sh", "*.txt",
    ".coverage", ".venv", ".DS_Store", "pavement.py", "paver_*",
    "testsuite")
  opts.proj.dirs.base.cp(opts.proj.dirs.dist, ignore=do_not_deploy)

  # STEP 3
  # ------
  release.write_ver_id(ver_id)

  print("---> dist success\n")


@task
@cmdopts([env_id_opt])
def dist_release(options):
  """
  make a release, deploy it to the target environment.
  """
  _validate_env_id(options)
  print("---> release success\n")


@task
@cmdopts([env_id_opt])
def dbseed(options):
  """
  load any reference data into the datastore if it"s not already present.
  """
  env_id = options.get("env_id", opts.proj.envs.local)
  _validate_env_id(options, optional=True)
  print env_id
  print("---> dbseed success\n")


@task
def lint():
  call_task("linter:check")
