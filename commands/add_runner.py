import click
from rich.console import Console
from rich.table import Table
from db import Session
from models.runner import Runner

console = Console()


@click.command("add_runner")
@click.option("--name", prompt="Runner name", help="Name of the runner to add.")
@click.option("--username", prompt="Runner username", help="Unique username for the runner.")
@click.option("--age", prompt="Runner age", type=int, help="Age of the runner (optional).")
@click.option("--gender", prompt="Runner gender", type=click.Choice(["male", "female", "other"], case_sensitive=False), help="Gender of the runner (optional).")
@click.option("--height", prompt="Runner height (inches)", type=int, help="Height of the runner in inches (optional).")
@click.option("--weight", prompt="Runner weight (pounds)", type=int, help="Weight of the runner in pounds (optional).")
def add_runner_cmd(name, age, gender, height, weight):
    """Add a new runner."""

    # TODO: Implement runner addition logic
    # Hint: create a new Runner object, add to session, commit, and print a success message
    runner = Runner(name=name, age=age, gender=gender, height_in=height, weight_lbs=weight)
    with Session() as session:
        session.add(runner)
        session.commit()
        console.print(f"[green]Runner '{name}' added successfully![/green]")
