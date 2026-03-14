import json
import anthropic
import click
from rich.console import Console
from rich.markdown import Markdown
from db import Session
from models.run import Run

console = Console()
client  = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env


# @click.command("plan")
# @click.option("--race",  required=True, help='Race name e.g. "Detroit Half Marathon"')
# @click.option("--date",  required=True, help="Race date in YYYY-MM-DD format")
# @click.option("--goal",  default=None,  help='Goal finish time e.g. "1:45:00"')
# @click.option("--weeks", default=12,    help="Number of weeks of recent runs to use as context")
# def plan_cmd(race, date, goal, weeks):
#     """Generate an AI training plan for an upcoming race."""

#     console.print(f"[bold]Generating training plan for {race} on {date}...[/bold]")

#     # TODO: query the last `weeks` weeks of runs from DB
#     # TODO: summarize into context (total miles/week, avg pace, recent long run, HR zones)
#     # TODO: build a prompt and call the Anthropic API
#     # TODO: parse the response and store in training_plans table
#     # TODO: display the plan using rich Markdown

#     context = build_context(weeks)
#     plan_text = call_ai(race, date, goal, context)

#     console.print(Markdown(plan_text))


def build_context(weeks: int) -> dict:
    """
    TODO: query DB for recent runs and return a summary dict like:
    {
        "avg_weekly_miles": 25.3,
        "recent_long_run_miles": 10.0,
        "avg_pace_s": 540,
        "avg_hr": 155,
        "total_runs": 24,
    }
    This gets sent to the AI so it can tailor the plan to your fitness.
    """
    return {}


def build_prompt(race: str, date: str, goal: str | None, context: dict) -> str:
    """
    TODO: build a prompt that includes:
    - The runner's recent training context
    - The race name, date, and goal time
    - Instructions to return a week-by-week training plan in Markdown
    """
    return f"""
You are an expert running coach. Here is the runner's recent training data:
{json.dumps(context, indent=2)}

Generate a week-by-week training plan for: {race} on {date}.
{"Goal finish time: " + goal if goal else ""}

Return the plan in Markdown with a table for each week showing: day, workout type, distance, notes.
"""


# def call_ai(race: str, date: str, goal: str | None, context: dict) -> str:
#     """Call the Anthropic API and return the plan as a string."""
#     prompt = build_prompt(race, date, goal, context)

#     message = client.messages.create(
#         model="claude-opus-4-5",
#         max_tokens=2048,
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return message.content[0].text
