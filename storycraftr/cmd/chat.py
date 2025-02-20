import os
import click
import shlex
from rich.console import Console
from rich.markdown import Markdown
from storycraftr.utils.core import load_book_config
from storycraftr.agent.agents import (
    get_thread,
    create_or_get_assistant,
    create_message,
)
import storycraftr.cmd.story as story_cmd
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from pathlib import Path

console = Console()

# Dictionary of available command modules
command_modules = {
    "iterate": story_cmd.iterate,
    "outline": story_cmd.outline,
    "worldbuilding": story_cmd.worldbuilding,
    "chapters": story_cmd.chapters,
}


@click.command()
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
def chat(book_path=None):
    """
    Start a chat session with the assistant for the given book name.
    Allows executing commands dynamically from various modules.
    """
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"Starting chat for [bold]{book_path}[/bold]. Type [bold green]exit()[/bold green] to quit or [bold green]help()[/bold green] for a list of available commands."
    )

    # Create or get the assistant and thread
    assistant = create_or_get_assistant(book_path)
    thread = get_thread()

    session = PromptSession(history=InMemoryHistory())

    console.print("[bold green]USE help() to get help and exit() to exit[/bold green]")

    while True:
        try:
            # Capture user input with prompt_toolkit
            user_input = session.prompt("You: ")

            if user_input.lower() == "exit()":
                console.print("[bold red]Exiting chat...[/bold red]")
                break

            if user_input.lower() == "help()":
                display_help()
                continue

            if user_input.startswith("!"):
                execute_cli_command(user_input[1:])
                continue

            # Pass the user input to the assistant for processing
            user_input = (
                f"Answer the next prompt formatted on markdown (text): {user_input}"
            )

            try:
                # Generate the response
                response = create_message(
                    book_path,
                    thread_id=thread.id,
                    content=user_input,
                    assistant=assistant,
                    force_single_answer=True,
                )

                # Render Markdown response
                markdown_response = Markdown(response)
                console.print(markdown_response)

            except Exception as e:
                console.print(f"[bold red]Error: {str(e)}[/bold red]")

        except KeyboardInterrupt:
            console.print("[bold red]Exiting chat...[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")


def execute_cli_command(user_input):
    """
    Function to execute CLI commands dynamically based on the available modules,
    calling the undecorated function directly.
    """
    try:
        parts = shlex.split(user_input)
        module_name = parts[0]
        command_name = parts[1].replace("-", "_")
        command_args = parts[2:]

        if module_name in command_modules:
            module = command_modules[module_name]

            if hasattr(module, command_name):
                cmd_func = getattr(module, command_name)

                if hasattr(cmd_func, "callback"):
                    cmd_func = cmd_func.callback

                if callable(cmd_func):
                    console.print(
                        f"Executing command from module: [bold]{module_name}[/bold]"
                    )
                    cmd_func(*command_args)
                else:
                    console.print(
                        f"[bold red]'{command_name}' is not a valid command[/bold red]"
                    )
            else:
                console.print(
                    f"[bold red]Command '{command_name}' not found in {module_name}[/bold red]"
                )
        else:
            console.print(f"[bold red]Module {module_name} not found[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error executing command: {str(e)}[/bold red]")


def display_help():
    """
    Function to display help with available modules and commands.
    """
    help_text = """
# Available Commands

Type commands prefixed with `!` followed by the module and the command name. 
Here are the available modules and some example commands:

### Modules

- **iterate**: Commands related to refining the story iteratively.
    - Example: `!iterate check-names "Check character names for consistency."`
    - Example: `!iterate refine-motivation "Refine character motivation for Zevid."`
    - Example: `!iterate check-consistency "Ensure consistency of character arcs and motivations."`
    - Example: `!iterate insert-chapter 3 "Insert a chapter about Zevid's backstory between chapters 2 and 3."`
    
- **outline**: Commands related to outlining the book.
    - Example: `!outline general-outline "Summarize the overall plot of a dystopian sci-fi novel."`
    - Example: `!outline plot-points "Identify key plot points in the story."`
    - Example: `!outline character-summary "Summarize Zevid’s character."`
    - Example: `!outline chapter-synopsis "Outline each chapter of a dystopian society."`

- **worldbuilding**: Commands for building the world.
    - Example: `!worldbuilding history "Describe the history of a dystopian world."`
    - Example: `!worldbuilding geography "Describe the geography of a dystopian society."`
    - Example: `!worldbuilding culture "Describe the culture of a society controlled by an elite class."`
    - Example: `!worldbuilding technology "Describe the advanced biotechnology mistaken for magic."`
    - Example: `!worldbuilding magic-system "Describe the 'magic' system based on advanced technology."`

- **chapters**: Commands for working with specific chapters.
    - Example: `!chapters chapter 1 "Write chapter 1 based on the synopsis provided."`
    - Example: `!chapters insert-chapter 5 "Insert a chapter revealing Zevid’s manipulation."`
    - Example: `!chapters cover "Generate the cover text for the novel."`
    - Example: `!chapters back-cover "Generate the back-cover text for the novel."`

### Other
- **help()**: Display this help message.
- **exit()**: Quit the chat session.

**Use the `!` symbol before commands to execute them.**
"""
    console.print(Markdown(help_text))
