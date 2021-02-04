import os
from channels.management.commands.runserver import Command as RunServerCommand
from rag.cli.command  import DjangoCommand


class Command(DjangoCommand, RunServerCommand):
    default_addr = '0.0.0.0'
    default_addr_ipv6 = '::'

    def execute(self, *args, **kwargs):
        os.environ['RAG_ENV'] = os.environ.get('RAG_ENV', 'development')
        super().execute(*args, **kwargs)
