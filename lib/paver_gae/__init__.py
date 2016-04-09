"""
  paver.ext.gae
  ~~~~~~~~~~~~~

  paver extension to automate app engine.


  :copyright: (c) 2016 by gregorynicholas.
"""
from __future__ import unicode_literals
from paver.easy import Bunch, options as opts, cmdopts
from paver.easy import task, call_task
from paver.easy import BuildFailure, error, path
from paver.ext import daemon, pip, release, utils
from paver.ext.utils import sh, rm
from paver.ext.gae import remote_api
from jinja2 import Environment
from jinja2.loaders import DictLoader

from paver.ext.gae.appcfg import appcfg
from paver.ext.gae.backends import *
from paver.ext.gae.cron import *
from paver.ext.gae.dos import *
from paver.ext.gae.index import *
from paver.ext.gae.queue import *


__all__ = [
  "appcfg", "install_runtime_libs", "build_descriptors", "fix_gae_sdk_path",
  "verify_serving", "ServerStartFailure",
  "install_sdk", "install_mapreduce_lib",
  "datastore_init", "open_admin",
  "server_run", "server_stop", "server_restart", "server_tail",
  "deploy", "deploy_branch", "update_indexes",
  "backends", "backends_rollback", "backends_deploy", "get_backends",
]


opts(
  gae=Bunch(
    sdk=Bunch(
      root=opts.proj.dirs.venv / opts.proj.dev_appserver.ver,
      venv_pth=opts.proj.dirs.venv / "lib/python2.7/site-packages/gaesdk.pth",
    ),
    dev_appserver=opts.proj.dev_appserver
  ))


class ServerStartFailure(BuildFailure):
  """
  """


class SdkServerNotRunningFailure(BuildFailure):
  """
  """


def _load_descriptors():
  """
    :returns: instance of a `jinja2.Environment`
  """
  descriptors = opts.proj.dirs.gae.descriptors.walkfiles("*.yaml")
  rv = Environment(loader=DictLoader(
    {str(d.name): str(d.text()) for d in descriptors}
  ))
  return rv


def build_descriptors(dest, env_id, ver_id=None):
  """
    :param dest:
    :param env_id:
    :param ver_id:
  """
  if ver_id is None:
    ver_id = release.dist_version_id()

  context = dict(
    env_id=env_id,
    ver_id=ver_id,
    templates_dir=str(opts.proj.dirs.app_web_templates.relpath()),
    static_dir=str(opts.proj.dirs.app_web_static.relpath()))
  jinjaenv = _load_descriptors()

  for name, dt in jinjaenv.loader.mapping.iteritems():
    _create_descriptor(
      name.replace(".template", ""),
      jinjaenv.get_template(name),
      context,
      dest)


def _create_descriptor(name, template, context, dest):
  """
  parses the config template files and generates yaml descriptor files in
  the root directory.

    :param template: instance of a jinja2 template object
    :param context: instance of a dict
    :param dest: instance of a paver.easy.path object
  """
  descriptor = dest / name.replace(".template", "")
  descriptor.write_text(template.render(**context))


def verify_serving(url, retries=15, sleep=2):
  """
    :param url:
    :param retries:
    :param sleep:
  """
  try:
    utils.ping(url, retries=retries, sleep=sleep)
  except utils.PingError:
    raise SdkServerNotRunningFailure("""
  can't connect to local appengine sdk server..
  """)
  else:
    print "connected to local appengine server.."


def fix_gae_sdk_path():
  """
  hack to load the app engine sdk.
  """
  import dev_appserver
  dev_appserver.fix_sys_path()


def _dev_appserver_config(config_id="default"):
  config = opts.gae.dev_appserver[config_id]
  if "blobstore_path" not in config["args"]:
    config["args"]["blobstore_path"] = opts.proj.dirs.data.blobstore
  if "datastore_path" not in config["args"]:
    config["args"]["datastore_path"] = opts.proj.dirs.data.datastore_file
  return config


def _build_dev_appserver_cmd(cfg):
  """
  generates a string to use as the dev_appserver start command.
  """
  flags = "".join(
    [" --%s " % x for x in cfg["flags"]])
  flags += "".join(
    [" --%s=%s " % (x, cfg["args"][x]) for x in cfg["args"]])
  return "{}/dev_appserver.py {} .".format(opts.gae.sdk.root, flags)


def install_runtime_libs(packages, dest):
  """
  since app engine doesn't allow for fucking pip installs, we have to symlink
  the libs to a local project directory. we could do 2 separate pip installs,
  but that shit gets slow as fuck.

    :todo: zip each lib inside of the lib dir to serve third party libs
  """
  top_level = pip.get_installed_top_level_files(packages["runtime"])
  for f in top_level:
    print "- sym-linking: ", f
    f.sym(dest / f.name)


@task
def install_sdk():
  """
  installs the app engine sdk to the virtualenv.
  """
  # todo: add a "force" option to override cache
  archive = path(opts.gae.dev_appserver.ver + ".zip")
  if not (opts.proj.dirs.venv / archive).exists():
    utils.wget(
      opts.gae.dev_appserver.src + archive.name, opts.proj.dirs.venv)

  rm(opts.gae.sdk.root)
  sh(
    """
    unzip -d ./ -oq {archive} && mv ./google_appengine {sdk_root}
    """,
    archive=archive.name,
    sdk_root=opts.gae.sdk.root,
    cwd=opts.proj.dirs.venv,
    err=True)

  if not opts.gae.sdk.root.exists():
    raise BuildFailure("shit didn't download + extract the lib properly.")

  # integrate the app engine sdk with virtualenv
  opts.gae.sdk.venv_pth.write_lines([
    opts.gae.sdk.root.abspath(),
    "import dev_appserver",
    "dev_appserver.fix_sys_path()"])

  # add gae sdk to path when in virtualenv
  postactivate = opts.proj.dirs.venv / "bin/postactivate"
  postactivate.write_lines([
    "#!/bin/bash",
    "export PATH=\"{}\":$PATH".format(opts.gae.sdk.root)])


@task
def install_mapreduce_lib():
  """
  installs a custom fork of google app engine's mapreduce library.
  (http://github.com/gregorynicholas/appengine-mapreduce)
  """
  if (opts.proj.dirs.lib / "mapreduce.zip").exists():
    return
  print "installing app engine mapreduce libraries.."

  rm(opts.proj.dirs.lib / "appengine-mapreduce-master")
  rm(opts.proj.dirs.lib / "mapreduce")
  rm(opts.proj.dirs.lib / "appengine_pipeline")

  if not (opts.proj.dirs.lib / "master.tar.gz").exists():
    utils.wget("https://github.com/gregorynicholas/appengine-mapreduce/"
               "archive/master.tar.gz", opts.proj.dirs.lib)

  utils.extract("master.tar.gz", opts.proj.dirs.lib)
  (opts.proj.dirs.lib / "appengine-mapreduce-master/mapreduce"
   ).move(opts.proj.dirs.lib)
  (opts.proj.dirs.lib / "appengine-mapreduce-master/appengine_pipeline"
   ).move(opts.proj.dirs.lib)
  rm(opts.proj.dirs.lib / "appengine-mapreduce-master")


@task
@cmdopts([
  ("set-default", "d", "set the current dist version as the default serving "
                       "version on app engine.", False),
  ("clear-cookies=", "c", "clear the local cookiejar before deploying.", True),
  ("deploy-backends", "b", "flag to deploy the backend servers.", False),
])
def deploy(options):
  """
  deploys the app to google app engine production servers.
  """
  ver_id = release.dist_version_id()
  appcfg("update -v ", error=True, cwd=opts.proj.dirs.dist)

  if options.set_default:
    set_default_serving_version(ver_id)

  if options.deploy_backends:
    call_task("backends_deploy")

  print("---> deploy success\n")


def set_default_serving_version(ver_id):
  """
  sets the default serving version on app engine production servers.

    :param ver_id:
  """
  appcfg(
    "set_default_version",
    version=ver_id,
    cwd=opts.proj.dirs.dist)


@task
def deploy_branch(options):
  """
  deploy current branch to named instance onto the integration environment.
  """
  call_task("build")

  _opts = opts.Namespace()
  _opts.env_id = opts.proj.envs.integration
  call_task("dist", options=_opts)

  _opts = opts.Namespace()
  _opts.default = False
  call_task("deploy", options=_opts)


@task
def update_indexes():
  """
  updates model index definitions on google app engine production servers.
  """
  appcfg("vacuum_indexes", quiet=True, cwd=opts.proj.dirs.dist)
  appcfg("update_indexes", quiet=True, cwd=opts.proj.dirs.dist)
  print("---> update_indexes success\n")


@task
def datastore_init():
  """
  cleans + creates the local app engine sdk server blobstore & datastore.
  """
  rm(opts.proj.dirs.data.datastore,
     opts.proj.dirs.data.blobstore)
  opts.proj.dirs.data.blobstore.makedirs()
  opts.proj.dirs.data.datastore.makedirs()
  opts.proj.dirs.data.datastore_file.touch()
  print("---> datastore_init success\n")


dev_appserver_config_opt = (
  "config_id=", "c", "name of the configuration profile, defined in "
                     "dev_appserver.yaml, to run the server with.")


@task
@cmdopts([dev_appserver_config_opt])
def server_run(options):
  """
  starts a google app engine server for local development.
  """
  config_id = options.get("config_id", "default")

  pid = opts.proj.dirs.gae.dev_appserver_pid
  if daemon.is_pid_running(pid):
    raise ServerStartFailure(" .. app-engine sdk server already running, pid detected..")

  stdout = path("{}.out".format(pid.name))
  try:
    sh = _build_dev_appserver_cmd(_dev_appserver_config(config_id))
    print '\n\n', sh, '\n\n'
    daemon.nohup(
      sh,
      pid=pid,
      append=False,
      error=True,
      capture=False,
      cwd=opts.proj.dirs.base)
  except:
    out = stdout.text().strip()
    if "socket.error: [Errno 48] Address already in use" in out:
      print ' .. existing server detected, attempting restart..'
      call_task("gae:server_restart")
      return

    elif "unable to open database file" in out:
      print ' .. gae-sdk datastore needs to be initialized, attempting to initialize..'
      call_task("gae:datastore_init")
      return

    raise ServerStartFailure("""
  an error occurred starting the sdk server:
    {}
  """.format(out))


@task
def server_stop():
  """
  stops the local google app engine sdk server.
  """
  # since dev_appserver2, we need to kill 2 processes..
  run = """
  psgrep dev_appserver.py | awk '{print $2}' | xargs kill -9
  psgrep _python_runtime.py | awk '{print $2}' | xargs kill -9
  """

  # std: kill pid file..
  daemon.kill(opts.proj.dirs.gae.dev_appserver_pid)


@task
@cmdopts([
  ("config_id=", "c", "name of the configuration profile, defined in "
                      "project.yaml, to run the server with.")
])
def server_restart(options):
  """
  restarts the local Google App Engine SDK server.
  """
  call_task("server_stop")
  server_run(options)


@task
def server_tail():
  """
  view the dev_appserver logs by running the unix native "tail" command.
  """
  stdout = path("{}.out".format(opts.proj.dirs.gae.dev_appserver_pid.name))
  sh("tail -f {pid}", pid=stdout)


@task
@cmdopts([
  ("config_id=", "c", "name of the configuration profile, defined in "
                      "project.yaml, to run the server with.")
])
def open_admin(options):
  """
  opens the google app engine sdk admin console.
  """
  config_id = options.get("config_id", "default")
  sh("open http://{url}:{port}/",
     cwd=opts.proj.dirs.base,
     **_dev_appserver_config(config_id).get("args"))


def create_oauth2_token():
  """
  """
  # first run to create a token..
  run = "appcfg.py update --skip_sdk_update_check --oauth2 "
  " --noauth_local_webserver . "
  sh(run)

  # generated credentials json:
  # {
  #   "_module": "oauth2client.client",
  #   "_class": "OAuth2Credentials",
  #   "access_token": "ya29.AHES6ZQmoHwZgrtRWJy1nV7b7OFuWHfu3amqQt0rfWDAjMiq7",
  #   "token_uri": "https://accounts.google.com/o/oauth2/token",
  #   "invalid": false,
  #   "client_id": "550516889912.apps.googleusercontent.com",
  #   "id_token": null,
  #   "client_secret": "ykPq-0UYfKNprLRjVx1hBBar",
  #   "token_expiry": "2013-06-12T05:16:55Z",
  #   "refresh_token": "1/W5dm5K8N03BWD_SeabvD2w6v6pzZqCBq1otvQsJEIsc",
  #   "user_agent": "appcfg_py/prerelease-1.8.1 Darwin/11.4.2
  #                  Python/2.7.5.final.0"
  # }

  # second run to use the refresh token..
  run = "appcfg.py update --skip_sdk_update_check "
  " --oauth2_refresh_token {} . "


def remote(options):
  """
  attaches to an app engine remote_api endpoint.
  """
  env_id = options.get("env_id", opts.proj.envs.local)

  dev_appserver = opts.proj.dev_appserver[env_id]
  host = "{}:{}".format(dev_appserver.host, dev_appserver.port)

  partition = options.get("partition", dev_appserver.partition)
  app_name = options.get("app_name", remote_api.DEFAULT_APP_NAME)
  host = options.get("host", remote_api.DEFAULT_HOST_NAME)
  path = options.get("path", remote_api.DEFAULT_ENDPOINT_PATH)
  email = options.get("email")
  password = options.get("password")

  if env_id == opts.proj.envs.local:
    verify_serving(host)
    partition = "dev"

  if email is None and host != remote_api.DEFAULT_HOST_NAME:
    email = opts.proj.email
    password = opts.proj.password

  fix_gae_sdk_path()
  print "connecting to remote_api: ", env_id, host, email, password
  remote_api.connect(
    "{}~{}-{}".format(partition, app_name, env_id),
    path=path, host=host, email=email, password=password)
