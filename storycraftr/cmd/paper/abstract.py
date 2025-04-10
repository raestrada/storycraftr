import click
from pathlib import Path
from rich.console import Console
from storycraftr.utils.core import load_book_config
from storycraftr.utils.markdown import save_to_markdown
from storycraftr.agent.agents import create_or_get_assistant, get_thread, create_message

console = Console()


@click.command()
@click.argument("prompt", type=str)
@click.option(
    "--book-path", type=click.Path(), help="Path to the paper directory", required=False
)
def abstract(prompt: str, book_path: str = None):
    """
    Generate an abstract for the paper.

    Args:
        prompt (str): A prompt describing what the abstract should contain.
        book_path (str, optional): Path to the paper directory.
    """
    book_path = book_path or Path.cwd()

    # Load book configuration
    config = load_book_config(book_path)
    if not config:
        console.print(
            f"[red bold]Error:[/red bold] Paper configuration not found in {book_path}."
        )
        return

    # Create sections directory if it doesn't exist
    sections_dir = Path(book_path) / "sections"
    sections_dir.mkdir(exist_ok=True)

    # Create or get the assistant and thread
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)

    # Generate abstract
    console.print("[bold blue]Generating abstract...[/bold blue]")

    # Create a more detailed prompt for the abstract
    detailed_prompt = f"""Generate a concise and informative abstract for an academic paper. The abstract should:

1. Start with a brief introduction to the topic
2. Clearly state the research problem or gap being addressed
3. Describe the methodology used
4. Summarize the key findings or results
5. Conclude with the main contributions and implications

Additional context for this paper:
{prompt}

Please write the abstract in a clear, academic style, avoiding unnecessary jargon. The abstract should be between 200-300 words."""

    # Get the abstract from the assistant
    abstract_content = create_message(
        book_path, thread_id=thread.id, content=detailed_prompt, assistant=assistant
    )

    # Save the abstract
    save_to_markdown(
        book_path=book_path,
        file_name="sections/abstract.md",
        header="Abstract",
        content=abstract_content,
    )

    console.print("[green bold]Abstract generated successfully![/green bold]")
    console.print("\nYou can find it in sections/abstract.md")
