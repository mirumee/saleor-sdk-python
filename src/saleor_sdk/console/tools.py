from base64 import b64decode, b64encode

import click


@click.group
def tools():
    pass


@tools.command
@click.argument("saleor-id", type=str)
def decode_id(saleor_id: str):
    entity_type, identifier = (
        b64decode(saleor_id.encode("utf-8")).decode("utf-8").split(":")
    )
    click.echo(f"{entity_type}: {identifier}")


@tools.command
@click.argument("entity-type", type=str)
@click.argument("identifier", type=str)
def encode_id(entity_type: str, identifier: str):
    saleor_id = b64encode(f"{entity_type}:{identifier}".encode("utf-8")).decode("utf-8")
    click.echo(f"{saleor_id}")
