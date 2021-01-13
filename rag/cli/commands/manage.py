import sys
import django.__main__
from django.core.management import execute_from_command_line
from rag.cli.command import BaseCommand, ConfiguredCommand


class Command(BaseCommand, ConfiguredCommand):
    help = 'Run a django management command'

def inject():
    ConfiguredCommand.import_root_module()
    if len(sys.argv) >= 2 and sys.argv[1] == 'manage':
        # trim 'rag' off arguments and set to simulate "python -m django" for management and runserver autoreload
        sys.argv = sys.argv[1:]
        sys.argv[0] = django.__main__.__file__

        # run django's original manage.py command
        execute_from_command_line(sys.argv)
        return True
    return False
