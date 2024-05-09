import os

import click
from sphinxbio.client import SphinxBio
from sphinxbio.dataset_schemas.abstract import AbstractSphinxDatasetSchema
from sphinxbio.entity_schemas.abstract import AbstractSphinxEntitySchema
from sphinxbio.environment import SphinxbioEnvironment

from .utils import find_subclasses


@click.group()
def cli():
    pass


@cli.group()
def datasets():
    pass


@cli.group()
def entities():
    pass


sphinx_api_key = os.environ.get("SPHINX_API_KEY")

if sphinx_api_key is None:
    raise ValueError("Please set SPHINX_API_KEY environment variable")

client = SphinxBio(
    environment=SphinxbioEnvironment.PRODUCTION,
    base_url=os.environ.get("SPHINX_API_HOST"),
    token=sphinx_api_key,
)


@datasets.command()
def register():
    for cls in find_subclasses("sphinx", AbstractSphinxDatasetSchema):
        print("Registering dataset schema for", cls.__name__)
        client.register_dataset_schema(pydantic_model=cls)


@entities.command()
def register_entities():
    for cls in find_subclasses("sphinx", AbstractSphinxEntitySchema):
        print("Registering entity schema for", cls.__name__)
        client.register_entity_schema(pydantic_model=cls)


if __name__ == "__main__":
    cli()
