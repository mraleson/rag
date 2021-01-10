import sys
from subprocess import call
from rag.cli.command import BaseCommand


class Command(BaseCommand):

    help = 'Serve the application via daphne'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--port', default='8000', help='port to listen to')
        parser.add_argument('-b', '--bind', default='0.0.0.0', help='host to bind to')
        parser.add_argument('-a', '--application', default='asgi:app.router', help='asgi application module path')

    def execute(self, args):
        try:
            sys.exit(call(f'daphne -p {args.port} -b {args.bind} {args.application}', shell=True))
        except KeyboardInterrupt:
            pass
