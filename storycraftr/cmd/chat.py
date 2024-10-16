import os
import click
from rich.console import Console
from rich.markdown import Markdown
from storycraftr.agent.agents import get_thread, create_or_get_assistant, create_message

console = Console()


@click.command()
@click.option("--book-name", type=click.Path(), help="Path to the book directory")
def chat(book_name=None):
    """
    Start a chat session with the assistant for the given book name.
    """
    if not book_name:
        book_name = os.getcwd()
    console.print(
        f"Starting chat for [bold]{book_name}[/bold]. Type [bold green]exit()[/bold green] to quit."
    )

    # Create or get the assistant and thread
    assistant = create_or_get_assistant(book_name)
    thread = get_thread()

    while True:
        user_input = console.input("[bold blue]You:[/bold blue] ")

        # Exit the chat
        if user_input.lower() == "exit()":
            console.print("[bold red]Exiting chat...[/bold red]")
            break

        user_input = (
            f"Answer the next prompt formatted on markdown (text): {user_input}"
        )
        # Send message to assistant
        try:
            response = create_message(
                thread_id=thread.id, content=user_input, assistant=assistant
            )
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
            continue

        # Display assistant's response formatted as markdown
        markdown_response = Markdown(response)
        console.print(markdown_response)
