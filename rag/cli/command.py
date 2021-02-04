import os
import sys
from importlib import import_module


# rag command patterned after django command
class BaseCommand:
    help = ''

    def add_arguments(self, parser):
        pass

    def execute(self, args):
        pass

# mixin that finds provides functions to find and import rag application module to setup django app
class ConfiguredCommand:

    @staticmethod
    def find_root_module():
        cwd = os.path.abspath(os.getcwd())
        sys.path.append(cwd)
        os.listdir()
        files = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f)) and f.endswith('.py')]
        for file in files:
            with open(file, 'r') as f:
                text = f.read()
                if 'from rag import Application' in text or 'rag.Application' in text:
                    return file[:-3] # remove .py
        return None

    @classmethod
    def import_root_module(cls):
        module = cls.find_root_module()
        if not module:
            raise RuntimeError('No root application module specified and unable to find module.')
        return import_module(module)


# mixin that enables us to execute django commands from rag command line
class DjangoCommand(ConfiguredCommand):

    def execute(self, args):
        self.import_root_module()
        options = vars(args)
        args = options.pop('args', ())
        base_options = {'verbosity': 1, 'force_color': False, 'no_color': False, 'skip_checks': False}
        super().execute(*args, **{**options, **base_options})
