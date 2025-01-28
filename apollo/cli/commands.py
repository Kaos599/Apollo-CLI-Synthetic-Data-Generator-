import click
import json
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import track

from apollo.generators.binary import BinaryGenerator
from apollo.generators.weighted import WeightedGenerator
from apollo.generators.genai import GeminiGenAIModel, GenAIModel  # Import GenAIModel
from apollo.generators.faker import FakerGenerator
from apollo.utils.output import save_csv, save_jsonl, save_yaml

console = Console()

@click.group()
@click.version_option()
def cli():
    """Apollo CLI: Your Synthetic Data Generation Tool."""
    console.print("[bold blue]Welcome to Apollo CLI Interactive Mode![/bold blue]")
    while True:
        console.print("\n[bold]Main Menu:[/bold]")
        console.print("1. Generate Data")
        console.print("2. Curate Data (Coming Soon)")
        console.print("3. Manage API Keys (Coming Soon)")
        console.print("4. Manage Prompts (Coming Soon)")
        console.print("5. Exit")

        choice = Prompt.ask("Enter your choice", choices=['1', '2', '3', '4', '5'], default='1')

        if choice == '1':
            handle_generate_data_interactive() # Function to handle interactive data generation
        elif choice == '2':
            console.print("[yellow]Curate Data - Coming Soon![/yellow]")
        elif choice == '3':
            console.print("[yellow]Manage API Keys - Coming Soon![/yellow]")
        elif choice == '4':
            console.print("[yellow]Manage Prompts - Coming Soon![/yellow]")
        elif choice == '5':
            console.print("Exiting interactive mode. Goodbye!")
            break
        else:
            console.print("[bold red]Invalid choice.[/bold red]")


def handle_generate_data_interactive():
    """Handles interactive data generation menu."""
    while True:
        console.print("\n[bold]Generate Data Menu:[/bold]")
        console.print("1. Binary Data (Yes/No)")
        console.print("2. Weighted Data")
        console.print("3. Faker Data")
        console.print("4. GenAI Data (Placeholder)") # Update when GenAI is fully implemented
        console.print("5. Back to Main Menu")

        data_type_choice = Prompt.ask("Choose data type to generate", choices=['1', '2', '3', '4', '5'], default='1')

        if data_type_choice == '1':
            probability = Prompt.ask("Enter probability for 'Yes' (0.0-1.0)", float, default=0.5)
            num_entries = Prompt.ask("Enter number of entries to generate", int, default=100)
            output_file = Prompt.ask("Enter output file path", default="binary_data.csv")
            output_format = Prompt.ask("Choose output format", choices=['csv', 'jsonl', 'yaml'], default='csv')
            generate_binary_data_cli(probability, num_entries, output_file, output_format) # Call CLI function
        elif data_type_choice == '2':
            choices_str = Prompt.ask("Enter weighted choices (e.g., 'A:0.5,B:0.3,C:0.2')")
            num_entries = Prompt.ask("Enter number of entries to generate", int, default=100)
            output_file = Prompt.ask("Enter output file path", default="weighted_data.csv")
            output_format = Prompt.ask("Choose output format", choices=['csv', 'jsonl', 'yaml'], default='csv')
            generate_weighted_data_cli(choices_str, num_entries, output_file, output_format) # Call CLI function
        elif data_type_choice == '3':
            provider = Prompt.ask("Enter Faker provider (e.g., 'name', 'address', 'text')")
            method = Prompt.ask("Enter Faker method (e.g., 'name', 'city', 'sentence')")
            num_entries = Prompt.ask("Enter number of entries to generate", int, default=100)
            output_file = Prompt.ask("Enter output file path", default="faker_data.csv")
            output_format = Prompt.ask("Choose output format", choices=['csv', 'jsonl', 'yaml'], default='csv')
            generate_faker_data_cli(provider, method, num_entries, output_file, output_format) # Call CLI function
        elif data_type_choice == '4':
            prompt_text = Prompt.ask("Enter GenAI prompt")
            schema_file = Prompt.ask("Enter path to schema file (optional, press Enter to skip)", default=None) # Optional schema for now
            num_samples = Prompt.ask("Enter number of samples to generate", int, default=10)
            output_file = Prompt.ask("Enter output file path", default="genai_data.jsonl")
            output_format = Prompt.ask("Choose output format", choices=['jsonl', 'yaml', 'csv'], default='jsonl')
            generate_genai_data_cli('placeholder', prompt_text, schema_file, num_samples, output_file, output_format) # Call CLI function with placeholder model
        elif data_type_choice == '5':
            break # Back to main menu
        else:
            console.print("[bold red]Invalid choice.[/bold red]")


# ---  CLI Command Implementations (using _cli suffix to differentiate from interactive functions) ---

@cli.group()
def generate():
    """Generate synthetic data of various types (use --help for options within each)."""
    pass


@generate.command('binary')
@click.option('--probability', type=click.FloatRange(0.0, 1.0), required=True, help='Probability of "Yes" response.')
@click.option('--num-entries', type=int, required=True, help='Number of entries to generate.')
@click.option('--output', type=click.Path(), required=True, help='Output file path.')
@click.option('--format', type=click.Choice(['csv', 'jsonl', 'yaml']), default='csv', help='Output format.')
def generate_binary_data_cli(probability, num_entries, output, format): # _cli suffix
    """Generate binary response data (Yes/No)."""
    generator = BinaryGenerator(probability)
    data = generator.generate_data(num_entries)
    progress_bar = track(range(num_entries), description="Generating binary data...")
    list(progress_bar)

    if format == 'csv':
        save_csv(data, output)
    elif format == 'jsonl':
        save_jsonl(data, output)
    elif format == 'yaml':
        save_yaml(data, output)
    console.print(f"[green]Binary data saved to '{output}' in {format} format.[/green]")


@generate.command('weighted')
@click.option('--choices', type=str, required=True, help='Comma-separated choices with probabilities (e.g., "A:0.5,B:0.3,C:0.2").')
@click.option('--num-entries', type=int, required=True, help='Number of entries to generate.')
@click.option('--output', type=click.Path(), required=True, help='Output file path.')
@click.option('--format', type=click.Choice(['csv', 'jsonl', 'yaml']), default='csv', help='Output format.')
def generate_weighted_data_cli(choices_str, num_entries, output, format): # _cli suffix
    """Generate weighted response data."""
    try:
        generator = WeightedGenerator(choices_str)
        data = generator.generate_data(num_entries)

        progress_bar = track(range(num_entries), description="Generating weighted data...")
        list(progress_bar)

        if format == 'csv':
            save_csv(data, output)
        elif format == 'jsonl':
            save_jsonl(data, output)
        elif format == 'yaml':
            save_yaml(data, output)
        console.print(f"[green]Weighted data saved to '{output}' in {format} format.[/green]")
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@generate.command('faker')
@click.option('--provider', required=True, help='Faker provider (e.g., "name", "address", "text"). See faker documentation.')
@click.option('--method', required=True, help='Faker provider method (e.g., "name", "city", "sentence").')
@click.option('--num-entries', type=int, required=True, help='Number of entries to generate.')
@click.option('--output', type=click.Path(), required=True, help='Output file path.')
@click.option('--format', type=click.Choice(['csv', 'jsonl', 'yaml']), default='csv', help='Output format.')
def generate_faker_data_cli(provider, method, num_entries, output, format): # _cli suffix
    """Generate data using Faker library providers."""
    try:
        generator = FakerGenerator(provider, method)
        data = generator.generate_data(num_entries)

        progress_bar = track(range(num_entries), description=f"Generating faker data using {provider}.{method}...")
        list(progress_bar)

        if format == 'csv':
            save_csv(data, output)
        elif format == 'jsonl':
            save_jsonl(data, output)
        elif format == 'yaml':
            save_yaml(data, output)
        console.print(f"[green]Faker data saved to '{output}' in {format} format.[/green]")
    except AttributeError:
        console.print(f"[bold red]Error:[/bold red] Invalid Faker provider or method. Check faker documentation.")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] An error occurred: {e}")



@generate.command('genai')
@click.option('--model-type', type=click.Choice(['placeholder', 'gemini']), default='placeholder', help='GenAI model type.')
@click.option('--prompt', type=str, required=True, help='Prompt for GenAI data generation.')
@click.option('--schema', type=click.Path(exists=True), required=False, help='Path to JSON schema file (for structured output, if supported by model).') # Schema is optional for now
@click.option('--num-samples', type=int, default=10, help='Number of samples to generate.')
@click.option('--output', type=click.Path(), required=True, help='Output file path.')
@click.option('--format', type=click.Choice(['jsonl', 'yaml', 'csv']), default='jsonl', help='Output format.')
def generate_genai_data_cli(model_type, prompt, schema, num_samples, output, format): # _cli suffix
    """Generate data using GenAI models (Gemini, etc.)."""
    try:
        if model_type == 'placeholder':
            console.print("[yellow]Using Placeholder GenAI Model.[/yellow]")
            genai_model = GenAIModel()
        elif model_type == 'gemini':
            console.print("[yellow]Using Gemini GenAI Model.[/yellow]")
            genai_model = GeminiGenAIModel() # Use Gemini model
        else:
            raise ValueError(f"Unknown model type: {model_type}")

        data = genai_model.generate_data(prompt, num_samples)

        progress_bar = track(range(num_samples), description=f"Generating {model_type} GenAI data...")
        list(progress_bar)

        if format == 'csv':
            save_csv(data, output) # Might need to flatten JSON for CSV - to be improved
        elif format == 'jsonl':
            save_jsonl(data, output)
        elif format == 'yaml':
            save_yaml(data, output)
        console.print(f"[green]{model_type.capitalize()} GenAI data saved to '{output}' in {format} format.[/green]")

    except ValueError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}") # For API key not set, etc.
    except Exception as e:
        console.print(f"[bold red]Error during GenAI generation:[/bold red] {e}")


@cli.command()
def curate():
    """Curate generated data."""
    console.print("Run 'apollo curate --help' for data curation options.") # Placeholder for now

@cli.command()
def add_key():
    """Add API keys for GenAI models."""
    console.print("Run 'apollo add-key --help' for API key management.") # Placeholder for now

@cli.command()
def add_prompt():
    """Add and manage system prompts."""
    console.print("Run 'apollo add-prompt --help' for prompt management.") # Placeholder for now