import multiprocessing
import gunicorn.app.base
import flask.cli
import click
import os
from gunicorn.six import iteritems
from werkzeug.debug import DebuggedApplication


def server_port():
    if 'PORT' not in os.environ:
        return '5000'
    else:
        return os.environ['PORT']


def server_bind_address():
    if 'HTTP_HOST' not in os.environ:
        return '127.0.0.1'
    else:
        return os.environ['HTTP_HOST']


def number_of_workers():
    if not 'WEB_CONCURRENCY' in os.environ:
        return (multiprocessing.cpu_count() * 2) + 1
    else:
        return os.environ['WEB_CONCURRENCY']


class GunicornStandalone(gunicorn.app.base.BaseApplication):
    def __init__(self, application, options=None):
        """ Construct the Application. Default gUnicorn configuration is loaded """

        self.application = application
        self.options = options or {}
        print(self.options)

        # if port, or host isn't set-- run from os.environments
        #
        super(GunicornStandalone, self).__init__()

    def init(self, parser, opts, args):
        """ Apply our custom settings """

        cfg = {}
        for k, v in self.options.items():
            if k.lower() in self.cfg.settings and v is not None:
                cfg[k.lower()] = v
        return cfg

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


@click.command('run',
               short_help='Start serving application from Gunicorn.',
               context_settings={
                   'allow_extra_args': True,
                   'ignore_unknown_options': True,
                   'allow_interspersed_args': False,
               })
@click.option('--host', '-h', default=None, help='The interface to bind to.')
@click.option('--port', '-p', default=None, help='The port to bind to.')
@click.option('--reload/--no-reload', default=None,
              help='Enable or disable the reloader.  By default the reloader '
                   'is active if debug is enabled.')
@click.option('--debugger/--no-debugger', default=None,
              help='Enable or disable the debugger.  By default the debugger '
                   'is active if debug is enabled.')
@click.option('--workers', '-w', default=number_of_workers(), help='Number of Gunicorn workers')
@click.option('--worker_class', '-wc', default=None, help="Specify a custom class of worker to use")
@flask.cli.pass_script_info
def cli(info, host, port, reload, debugger, workers, worker_class):

    os.environ['FLASK_RUN_FROM_CLI_SERVER'] = '1'
    debug = flask.cli.get_debug_flag()

    port = port or server_port()
    host = host or server_bind_address()

    options = {
        'workers': workers or number_of_workers(),
        'bind': '{}:{}'.format(host, port)
    }

    if worker_class is not None:
        options["worker_class"] = worker_class

    app = info.load_app()

    if debug or debugger:
        options["workers"] = 1
        app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

        print(' * Launching in DEBUG mode')
        print(' * Serving Flask using a single worker "{}"'.format(info.app_import_path))

        if reload is None:
            options["reload"] = bool(debug)
        if debugger is None:
            options["debug"] = bool(debug) or debugger

    else:
        print(' * Launching in Production Mode')
        print(' * Serving Flask with {} worker(s) "{}"'.format(
            options["workers"], info.app_import_path
        ))

    server = GunicornStandalone(app, options=options)
    server.run()
