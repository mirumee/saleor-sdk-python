import click

from saleor_sdk.console.develop import develop
from saleor_sdk.console.tools import tools


@click.group
def cli():
    pass


cli.add_command(develop)
cli.add_command(tools)
