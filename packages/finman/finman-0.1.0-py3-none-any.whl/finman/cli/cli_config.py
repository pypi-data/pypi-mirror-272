import click
from ..config.config import CONFIG_FILE

@click.command("config",
               help="Edit application configurations")
@click.option("--set", 
              help="Set a configuration option in Key Value format.",
              multiple=True,
              type=(str, str))
@click.option("--get",
              help="Get a configuration option's value") 
def config(set, get):
    config_file = CONFIG_FILE
    click.echo(f"The path of config file is {config_file}")
    