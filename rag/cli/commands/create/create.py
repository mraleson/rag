import os
import shutil
from subprocess import call
from string import Template
from rag.cli.command import BaseCommand
from rag.cli.commands.version import get_version


class Command(BaseCommand):

    help = 'Create an empty rag django project'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='project name / directory to create')
        parser.add_argument('size', type=str, choices=['micro'], help='project template size')

    def execute(self, args):
        working_dir = os.getcwd()
        file_dir = os.path.dirname(os.path.abspath(__file__))
        destination = os.path.join(working_dir, args.name)
        source = os.path.normpath(os.path.join(file_dir, f'./templates/{args.size}'))

        # copy template
        try:
            shutil.copytree(source, destination)
            print(f"Project {args.name} successfully created at {destination}")
        except FileExistsError:
            print(f"Unable to create project, the specified path '{destination}' already exists.")

        # fill in pyproject.toml
        self.template(os.path.join(destination, 'pyproject.toml'), version=get_version())

        # install project requirements
        print("Installing project dependencies in poetry virtual environment")
        os.chdir(destination)
        call(['poetry', 'install'])

    @staticmethod
    def template(path, **kwargs):
        with open(path, 'r') as file:
            text = file.read()
        text = Template(text).substitute(**kwargs)
        with open(path, 'w') as file:
            file.write(text)