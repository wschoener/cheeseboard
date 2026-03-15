import click
from db import init_db, wipe_db
from commands.import_run import import_cmd
from commands.runs import runs_cmd, run_detail_cmd
from commands.trends import trends_cmd
from commands.add_runner import add_runner_cmd


@click.group()
def cli():
    """COROS running app — your data, your way."""
    pass


cli.add_command(import_cmd,      name="import")
cli.add_command(runs_cmd,        name="runs")
cli.add_command(run_detail_cmd,  name="run")
cli.add_command(trends_cmd,      name="trends")
cli.add_command(add_runner_cmd, name="add_runner")


@cli.command("init")
def init_cmd():
    """Initialize the database (create tables). Call once on first run.""" 
    init_db()

@cli.command("wipe")
def wipe_cmd():
    """Wipe the database (drop all tables). Use with caution!"""
    if not click.confirm("This will delete all existing data. Are you sure?"):
        click.echo("Aborting.")
        return  

    wipe_db()


if __name__ == "__main__":
    cli()
