import click

@click.group(invoke_without_command=True, no_args_is_help=True)
@click.version_option(package_name="poetryx")
def cli() -> None:
    pass

@cli.command()
@click.argument('name')
def hello(name):
    """ Placeholder. """
    click.echo(f"Hello, {name}!")

@cli.command()
def fix():
    """ Placeholder. """
    click.echo("Fix command placeholder.")

