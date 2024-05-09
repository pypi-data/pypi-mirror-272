import click
from . import __version__


@click.group()
def cli():
    pass


@click.version_option(version=__version__)
def get_version():
    return __version__


from mysnippet.cli_config import config

cli.add_command(config)

from mysnippet.cli_encrypt import encrypt

cli.add_command(encrypt)

from mysnippet.cli_project import project

cli.add_command(project)

from mysnippet.cli_snippet import snippet

cli.add_command(snippet)

from mysnippet.cli_tool import tool

cli.add_command(tool)

cli()
