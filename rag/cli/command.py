# rag command patterned after django command
class BaseCommand:
    help = ''

    def add_arguments(self, parser):
        pass

    def execute(self, args):
        pass

# mixin that enables us to execute django commands from rag command line
class DjangoCommand:
        
    def execute(self, args):
        options = vars(args)
        args = options.pop('args', ())
        base_options = {'verbosity': 1, 'force_color': False, 'no_color': False, 'skip_checks': False}
        super().execute(*args, **{**options, **base_options})


# >> for django commands find and import the rag application, which will load django settings etc
# # find and import application
# def application():
#     return None
# # setup django
# # sys.path.append(os.getcwd())
# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
# # try:
# #     django.setup()
# # except ModuleNotFoundError:
# #     pass
