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
@click.option("--known-hr", prompt="Do you know your HR zones? (yes/no)", type=click.Choice(["yes", "no"], case_sensitive=False), help="Whether the runner knows their HR zones (optional).")
def add_runner_cmd(name, username, age, gender, height, weight, known_hr):
    """Add a new runner."""

    if known_hr.lower() == "yes":
        threshold_hr = click.prompt("Enter your threshold heart rate (bpm)", type=int)
        hr_zone_1 = click.prompt("Enter your HR Zone 1 upper limit (bpm)", type=int)
        hr_zone_2 = click.prompt("Enter your HR Zone 2 upper limit (bpm)", type=int)
        hr_zone_3 = click.prompt("Enter your HR Zone 3 upper limit (bpm)", type=int)
        hr_zone_4 = click.prompt("Enter your HR Zone 4 upper limit (bpm)", type=int)
        hr_zone_5 = click.prompt("Enter your HR Zone 5 upper limit (bpm)", type=int)

    # TODO: Implement runner addition logic
    # Hint: create a new Runner object, add to session, commit, and print a success message
    runner = Runner(name=name, age=age, gender=gender, height_in=height, weight_lbs=weight, username=username, threshold_hr=threshold_hr if known_hr.lower() == "yes" else None, hr_zone_1_stop=hr_zone_1 if known_hr.lower() == "yes" else None, hr_zone_2_stop=hr_zone_2 if known_hr.lower() == "yes" else None, hr_zone_3_stop=hr_zone_3 if known_hr.lower() == "yes" else None, hr_zone_4_stop=hr_zone_4 if known_hr.lower() == "yes" else None, hr_zone_5_stop=hr_zone_5 if known_hr.lower() == "yes" else None)
    with Session() as session:
        session.add(runner)
        session.commit()
        console.print(f"[green]Runner '{name}' added successfully![/green]")
