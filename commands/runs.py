import click
from rich.console import Console
from rich.table import Table
from db import Session
from models.run import Run

console = Console()


@click.command("runs")
@click.option("--limit", default=10, help="Number of recent runs to show.")
def runs_cmd(limit):
    """List recent runs."""

    # TODO: query the DB for the most recent `limit` runs
    # TODO: build a rich Table with columns: #, Date, Distance, Pace, Avg HR, Elevation
    # TODO: print the table

    table = Table(title="Recent Runs")
    table.add_column("#", style="dim")
    table.add_column("Date")
    table.add_column("Distance")
    table.add_column("Avg Pace")
    table.add_column("Avg HR")
    table.add_column("Elev Gain")

    console.print(table)


@click.command("run")
@click.argument("run_id", type=int)
def run_detail_cmd(run_id):
    """Show detailed view of a single run including splits and HR zones."""

    # TODO: query run by ID, 404 if not found
    # TODO: print run summary header (date, distance, pace, HR, elevation)
    # TODO: print splits table (mile, pace, HR, elevation)
    # TODO: print HR zone breakdown as a simple bar or percentage

    console.print(f"[bold]Run #{run_id}[/bold]")
    console.print("[dim]TODO: implement run detail view[/dim]")
