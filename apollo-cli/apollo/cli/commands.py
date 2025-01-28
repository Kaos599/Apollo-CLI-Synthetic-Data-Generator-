import click
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Confirm  
from rich.progress import track
from rich.text import Text
from rich.box import ROUNDED

import inquirer  # Import inquirer

from apollo.generators.binary import BinaryGenerator
from apollo.generators.weighted import WeightedGenerator
from apollo.generators.genai import GeminiGenAIModel
# from apollo.generators.faker import FakerGenerator
from apollo.utils.output import save_csv, save_jsonl, save_yaml

console = Console()

def create_menu_table(title: str, options: list) -> Table:
    """Create a beautiful menu table using Rich"""
    table = Table(show_header=False, box=ROUNDED, expand=True, border_style="blue")
    table.add_column("Option", style="cyan", width=4)
    table.add_column("Description", style="white")

    for idx, (option, description) in enumerate(options, 1):
        table.add_row(f"{idx}", description)

    return Panel(table, title=f"[bold blue]{title}[/bold blue]", border_style="blue")

@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(package_name='apollo-cli')
def cli():
    """Apollo CLI: Your Synthetic Data Generation Tool."""
    # Create welcome banner
    welcome_text = Text()
    welcome_text.append("⚡ Welcome to ", style="bold blue")
    welcome_text.append("Apollo CLI", style="bold yellow")
    welcome_text.append(" ⚡", style="bold blue")

    console.print("\n")
    console.print(Panel(welcome_text, border_style="blue", box=ROUNDED))
    console.print("\n")

    while True:
        main_menu_options = [
            ("Generate Data", "Generate synthetic data using various methods"),
            ("Curate Data", "Curate and validate generated data (Coming Soon)"),
            ("Manage API Keys", "Configure API keys for GenAI models (Coming Soon)"),
            ("Manage Prompts", "Manage system prompts and templates (Coming Soon)"),
            ("Exit", "Exit Apollo CLI")
        ]

        console.print(create_menu_table("Main Menu", main_menu_options))

        questions = [
            inquirer.List('choice',
                          message="\n[bold cyan]Enter your choice[/bold cyan]",
                          choices=['1', '2', '3', '4', '5', 'Exit'],  # Added 'Exit' to choices for inquirer
                          carousel=True) # Optional: for better scrolling in long lists
        ]
        answers = inquirer.prompt(questions, console=False) # console=False to prevent inquirer messing with rich console
        if answers is None: # Handle Ctrl+C or Esc
            console.print("Exiting interactive mode. Goodbye!")
            break

        choice = answers['choice']

        if choice == '1' or choice == 'Generate Data': # Inquirer returns chosen value, not just index
            handle_generate_data_interactive()
        elif choice == '2' or choice == 'Curate Data':
            console.print(Panel("[yellow]Curate Data feature coming soon![/yellow]", border_style="yellow"))
        elif choice == '3' or choice == 'Manage API Keys':
            console.print(Panel("[yellow]API Key Management feature coming soon![/yellow]", border_style="yellow"))
        elif choice == '4' or choice == 'Manage Prompts':
            console.print(Panel("[yellow]Prompt Management feature coming soon![/yellow]", border_style="yellow"))
        elif choice == '5' or choice == 'Exit':
            console.print(Panel("👋 Thank you for using Apollo CLI. Goodbye!", border_style="blue"))
            break

def handle_generate_data_interactive():
    """Handles interactive data generation menu with improved UI using inquirer"""
    while True:
        data_options = [
            ("Binary Data", "Generate Yes/No binary data"),
            ("Weighted Data", "Generate data with custom weights"),
            ("Faker Data", "Generate data using Faker library"),
            ("GenAI Data", "Generate data using AI models (Placeholder)"),
            ("Back", "Return to main menu")
        ]

        console.print("\n")
        console.print(create_menu_table("Generate Data", data_options))

        questions = [
            inquirer.List('data_type_choice',
                          message="\n[bold cyan]Choose data type to generate[/bold cyan]",
                          choices=['1', '2', '3', '4', '5', 'Back'], # Added 'Back' to choices
                          carousel=True)
        ]
        answers = inquirer.prompt(questions, console=False)
        if answers is None:
            break # Go back to main menu if cancelled

        data_type_choice = answers['data_type_choice']

        if data_type_choice == '1' or data_type_choice == 'Binary Data':
            generate_binary_data_interactive()
        elif data_type_choice == '2' or data_type_choice == 'Weighted Data':
            generate_weighted_data_interactive()
        elif data_type_choice == '3' or data_type_choice == 'Faker Data':
            generate_faker_data_interactive()
        elif data_type_choice == '4' or data_type_choice == 'GenAI Data':
            generate_genai_data_interactive()
        elif data_type_choice == '5' or data_type_choice == 'Back':
            break # Back to main menu

def generate_binary_data_interactive():
    """Interactive binary data generation with improved UI using inquirer"""
    console.print("\n")
    console.print(Panel("[bold]Binary Data Generation[/bold]", border_style="blue"))

    questions = [
        inquirer.Text('probability', message="Enter probability for 'Yes' (0.0-1.0)", default="0.5", validate=lambda _, x: 0<=float(x)<=1),
        inquirer.Text('num_entries', message="Enter number of entries to generate", default="100", validate=lambda _, x: x.isdigit()),
        inquirer.Text('output_file', message="Enter output file path", default="binary_data.csv"),
        inquirer.List('output_format',
                      message="Choose output format",
                      choices=['csv', 'jsonl', 'yaml'],
                      default='csv',
                      carousel=True)
    ]
    answers = inquirer.prompt(questions, console=False)
    if answers is None:
        return # User cancelled

    probability = float(answers['probability'])
    num_entries = int(answers['num_entries'])
    output_file = answers['output_file']
    output_format = answers['output_format']

    with console.status("[bold blue]Generating binary data...") as status:
        generate_binary_data_cli(probability, num_entries, output_file, output_format)

def generate_weighted_data_interactive():
    """Interactive weighted data generation with improved UI using inquirer"""
    console.print("\n")
    console.print(Panel("[bold]Weighted Data Generation[/bold]", border_style="blue"))

    questions = [
        inquirer.Text('choices_str', message="Enter weighted choices (e.g., 'A:0.5,B:0.3,C:0.2')", default="A:0.5,B:0.5"),
        inquirer.Text('num_entries', message="Enter number of entries to generate", default="100", validate=lambda _, x: x.isdigit()),
        inquirer.Text('output_file', message="Enter output file path", default="weighted_data.csv"),
        inquirer.List('output_format',
                      message="Choose output format",
                      choices=['csv', 'jsonl', 'yaml'],
                      default='csv',
                      carousel=True)
    ]
    answers = inquirer.prompt(questions, console=False)
    if answers is None:
        return

    choices_str = answers['choices_str']
    num_entries = int(answers['num_entries'])
    output_file = answers['output_file']
    output_format = answers['output_format']

    with console.status("[bold blue]Generating weighted data...") as status:
        generate_weighted_data_cli(choices_str, num_entries, output_file, output_format)

def generate_faker_data_interactive():
    """Interactive Faker data generation with improved UI using inquirer"""
    console.print("\n")
    console.print(Panel("[bold]Faker Data Generation[/bold]", border_style="blue"))

    questions = [
        inquirer.Text('provider', message="Enter Faker provider (e.g., 'name', 'address', 'text')", default="name"),
        inquirer.Text('method', message="Enter Faker method (e.g., 'name', 'city', 'sentence')", default="name"),
        inquirer.Text('num_entries', message="Enter number of entries to generate", default="100", validate=lambda _, x: x.isdigit()),
        inquirer.Text('output_file', message="Enter output file path", default="faker_data.csv"),
        inquirer.List('output_format',
                      message="Choose output format",
                      choices=['csv', 'jsonl', 'yaml'],
                      default='csv',
                      carousel=True)
    ]
    answers = inquirer.prompt(questions, console=False)
    if answers is None:
        return

    provider = answers['provider']
    method = answers['method']
    num_entries = int(answers['num_entries'])
    output_file = answers['output_file']
    output_format = answers['output_format']

    with console.status("[bold blue]Generating faker data...") as status:
        generate_faker_data_cli(provider, method, num_entries, output_file, output_format)

def generate_genai_data_interactive():
    """Interactive GenAI data generation with improved UI using inquirer (Placeholder)"""
    console.print("\n")
    console.print(Panel("[bold]GenAI Data Generation (Placeholder)[/bold]", border_style="blue"))
    console.print(Panel("[yellow]GenAI data generation is a placeholder. Implementation coming soon.[/yellow]", border_style="yellow"))

    questions = [
        inquirer.Text('prompt_text', message="Enter GenAI prompt", default="Generate a short example text."),
        inquirer.Text('schema_file', message="Enter path to schema file (optional, press Enter to skip)", default=None),
        inquirer.Text('num_samples', message="Enter number of samples to generate", default="10", validate=lambda _, x: x.isdigit()),
        inquirer.Text('output_file', message="Enter output file path", default="genai_data.jsonl"),
        inquirer.List('output_format',
                      message="Choose output format",
                      choices=['jsonl', 'yaml', 'csv'],
                      default='jsonl',
                      carousel=True)
    ]
    answers = inquirer.prompt(questions, console=False)
    if answers is None:
        return

    prompt_text = answers['prompt_text']
    schema_file = answers['schema_file']
    num_samples = int(answers['num_samples'])
    output_file = answers['output_file']
    output_format = answers['output_format']

    with console.status("[bold blue]Generating GenAI data (placeholder)...") as status:
        generate_genai_data_cli('placeholder', prompt_text, schema_file, num_samples, output_file, output_format)


# ---  CLI Command Implementations (using _cli suffix - no changes needed in core logic) ---

@cli.group()
def generate():
    """
    [bold]Generate Synthetic Data[/bold] of various types.

    Use 'apollo generate <data_type> --help' for more options.

    [bold]Data Types:[/bold]
    \t[green]binary[/green]: Generate binary (Yes/No) data.
    \t[green]weighted[/green]: Generate weighted choice data.
    \t[green]faker[/green]: Generate data using Faker providers.
    \t[green]genai[/green]: Generate data using GenAI models (placeholder for now).
    """
    pass


@generate.command('binary')
@click.option('--probability', type=click.FloatRange(0.0, 1.0), required=True, help='Probability of "Yes" response.')
@click.option('--num-entries', type=int, required=True, help='Number of entries to generate.')
@click.option('--output', type=click.Path(), required=True, help='Output file path.')
@click.option('--format', type=click.Choice(['csv', 'jsonl', 'yaml']), default='csv', help='Output format.')
def generate_binary_data_cli(probability, num_entries, output, format):
    """[bold green]Generate Binary Response Data (Yes/No)[/bold green].

    Generates synthetic data with binary responses ('Yes' or 'No') based on a given probability.
    """
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
def generate_weighted_data_cli(choices_str, num_entries, output, format):
    """[bold green]Generate Weighted Response Data[/bold green].

    Generates synthetic data with weighted responses based on user-defined choices and probabilities.
    """
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
def generate_faker_data_cli(provider, method, num_entries, output, format):
    """[bold green]Generate Data using Faker Library Providers[/bold green].

    Leverages the Faker library to generate data based on specified providers and methods.
    Refer to the Faker documentation for available providers and methods.
    """
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
@click.option('--schema', type=click.Path(exists=True), required=False, help='Path to JSON schema file (for structured output, if supported by model).')
@click.option('--num-samples', type=int, default=10, help='Number of samples to generate.')
@click.option('--output', type=click.Path(), required=True, help='Output file path.')
@click.option('--format', type=click.Choice(['jsonl', 'yaml', 'csv']), default='jsonl', help='Output format.')
def generate_genai_data_cli(model_type, prompt, schema, num_samples, output, format):
    """[bold green]Generate Data using GenAI Models[/bold green] (Placeholder).

    [yellow]Currently a placeholder[/yellow]. Will be implemented to generate structured data using GenAI models like Gemini, Ollama, Groq.
    """
    try:
        if model_type == 'placeholder':
            console.print("[yellow]Using Placeholder GenAI Model.[/yellow]")
            genai_model = GenAIModel()
        elif model_type == 'gemini':
            console.print("[yellow]Using Gemini GenAI Model.[/yellow]")
            genai_model = GeminiGenAIModel()
        else:
            raise ValueError(f"Unknown model type: {model_type}")

        data = genai_model.generate_data(prompt, num_samples)

        progress_bar = track(range(num_samples), description=f"Generating {model_type} GenAI data...")
        list(progress_bar)

        if format == 'csv':
            save_csv(data, output)
        elif format == 'jsonl':
            save_jsonl(data, output)
        elif format == 'yaml':
            save_yaml(data, output)
        console.print(f"[green]{model_type.capitalize()} GenAI data saved to '{output}' in {format} format.[/green]")

    except ValueError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]Error during GenAI generation:[/bold red] {e}")


@cli.command()
def curate():
    """[bold]Curate Generated Data[/bold] (Coming Soon).

    [yellow]This feature is under development and will be available in a future version.[/yellow]
    """
    console.print(Panel("[yellow]Curate Data feature coming soon![/yellow]", border_style="yellow"))

@cli.command()
def add_key():
    """[bold]Add API Keys for GenAI Models[/bold] (Coming Soon).

    [yellow]This feature is under development and will be available in a future version.[/yellow]
    """
    console.print(Panel("[yellow]API Key Management feature coming soon![/yellow]", border_style="yellow"))

@cli.command()
def add_prompt():
    """[bold]Add and Manage System Prompts[/bold] (Coming Soon).

    [yellow]This feature is under development and will be available in a future version.[/yellow]
    """
    console.print(Panel("[yellow]Prompt Management feature coming soon![/yellow]", border_style="yellow"))