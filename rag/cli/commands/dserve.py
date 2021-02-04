import sys
from subprocess import call
from importlib import import_module
from rag import Application
from rag.cli.command import BaseCommand
from rag.cli.command import ConfiguredCommand


class Command(BaseCommand, ConfiguredCommand):

    help = 'Serve the application via daphne'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--port', default='8000', help='port to listen to')
        parser.add_argument('-b', '--bind', default='0.0.0.0', help='host to bind to')
        parser.add_argument('-a', '--application', default=None, help='asgi application module path')

    def execute(self, args):
        if not args.application:
            path = self.find_root_module()
            module = import_module(path)
            app = 'asd'
            for k in dir(module):
                if isinstance(getattr(module, k), Application):
                    app = k
            args.application = f'{path}:{app}.router'
        try:
            sys.exit(call(f'daphne -p {args.port} -b {args.bind} {args.application}', shell=True))
        except KeyboardInterrupt:
            pass
