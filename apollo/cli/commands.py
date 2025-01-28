import click
from rich.console import Console

console = Console()

@click.group()
@click.version_option()
def cli():
    """Apollo CLI: Your Synthetic Data Generation Tool."""
    pass

@cli.command()
def generate():
    """Generate synthetic data."""
    console.print("Run 'apollo generate --help' for data generation options.")

@cli.command()
def curate():
    """Curate generated data."""
    console.print("Run 'apollo curate --help' for data curation options.")

@cli.command()
def add_key():
    """Add API keys for GenAI models."""
    console.print("Run 'apollo add-key --help' for API key management.")

@cli.command()
def add_prompt():
    """Add and manage system prompts."""
    console.print("Run 'apollo add-prompt --help' for prompt management.")