import click
from rich.console import Console
from rich.table import Table
from db import Session
from models.run import Run

console = Console()


@click.command("trends")
@click.option("--weeks", default=8, help="Number of weeks to show.")
def trends_cmd(weeks):
    """Show weekly mileage and pace trends."""

    # TODO: query runs grouped by week for the last `weeks` weeks
    # TODO: calculate per-week: total miles, total runs, avg pace, avg HR
    # TODO: display as a table with a simple ASCII sparkline for mileage trend

    # Hint: SQLAlchemy + PostgreSQL date_trunc is great for this:
    #   func.date_trunc('week', Run.date)

    table = Table(title=f"Weekly Trends — Last {weeks} Weeks")
    table.add_column("Week")
    table.add_column("Runs")
    table.add_column("Miles")
    table.add_column("Avg Pace")
    table.add_column("Avg HR")

    console.print(table)
