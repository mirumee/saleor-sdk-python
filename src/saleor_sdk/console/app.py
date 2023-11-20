import click

from saleor_sdk.console.tools import tools


@click.group
def cli() -> None:
    pass


cli.add_command(tools)
