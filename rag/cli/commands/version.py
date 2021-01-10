from rag.cli.command  import BaseCommand
try:
    from importlib import metadata
except ImportError: # for Python<3.8
    import importlib_metadata as metadata


class Command(BaseCommand):

    help = 'Display current Rag version'

    def execute(self, args):
        print(metadata.version('rag'))
