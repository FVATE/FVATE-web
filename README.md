FVATE
=====

source code for [FVATE.com](http://fvate.com), a google-appengine app.

<br />

-----

* i: [INSTALL.md](docs/INSTALL.md)
* ii: [QUICKSTART.md](docs/QUICKSTART.md)
* iii: [CLIENT.md](docs/CLIENT.md)

-----

<br />


setup shell commands:

    $ mkvirtualenv --no-site-packages fvate-dev
    $ pip install pip --upgrade
    $ pip install -r requirements.txt
    $ paver bootstrap_backend
    $ paver bootstrap_client
    # $ paver bootstrap_init_dirs
    $ paver gae:install_sdk
    $ paver gae:datastore_init

run shell commands:

    $ activate-virtualenv
    $ workon fvate-dev
    $ paver gae:server_run
    $ paver gae:server_tail
    $ paver gae:server_stop
