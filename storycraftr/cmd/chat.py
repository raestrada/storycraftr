import os
import click
import inspect
from rich.console import Console
from rich.markdown import Markdown
from storycraftr.agent.agents import get_thread, create_or_get_assistant, create_message
from storycraftr.cmd import iterate, outline, worldbuilding, chapters

console = Console()

# Dictionary of available command modules
command_modules = {
    "iterate": iterate,
    "outline": outline,
    "worldbuilding": worldbuilding,
    "chapters": chapters,
}


@click.command()
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
def chat(book_path=None):
    """
    Start a chat session with the assistant for the given book name.
    Now also allows executing commands dynamically from various modules.
    """
    if not book_path:
        book_path = os.getcwd()
    console.print(
        f"Starting chat for [bold]{book_path}[/bold]. Type [bold green]exit()[/bold green] to quit or [bold green]help()[/bold green] for a list of available commands."
    )

    # Create or get the assistant and thread
    assistant = create_or_get_assistant(book_path)
    thread = get_thread()
    console.print("[bold green]USE help() to get help and exit() to exit[/bold green]")
    while True:
        user_input = console.input("[bold blue]You:[/bold blue] ")

        # Exit the chat
        if user_input.lower() == "exit()":
            console.print("[bold red]Exiting chat...[/bold red]")
            break

        # Display help
        if user_input.lower() == "help()":
            display_help()
            continue

        # Check if the user is asking to execute a command
        if user_input.startswith("!"):
            execute_cli_command(user_input[1:])
            continue

        user_input = (
            f"Answer the next prompt formatted on markdown (text): {user_input}"
        )
        # Send message to assistant
        try:
            response = create_message(
                book_path, thread_id=thread.id, content=user_input, assistant=assistant
            )
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
            continue

        # Display assistant's response formatted as markdown
        markdown_response = Markdown(response)
        console.print(markdown_response)


import inspect

import shlex
import inspect

import shlex
import inspect


def execute_cli_command(user_input):
    """
    Function to execute CLI commands dynamically based on the available modules,
    calling the undecorated function directly.
    """
    try:
        # Use shlex.split to handle quotes and separate arguments correctly
        parts = shlex.split(user_input)
        module_name = parts[0]
        command_name = parts[1].replace("-", "_")  # Replace hyphens with underscores
        command_args = parts[2:]  # Keep the rest of the arguments as a list

        # Check if the module exists in command_modules
        if module_name in command_modules:
            module = command_modules[module_name]

            # Introspection: Get the function by name
            if hasattr(module, command_name):
                cmd_func = getattr(module, command_name)

                # Check if it's a Click command
                if hasattr(cmd_func, "callback"):
                    # Call the underlying undecorated function directly
                    cmd_func = cmd_func.callback

                # Check if it's a callable (function)
                if callable(cmd_func):
                    console.print(
                        f"Executing command from module: [bold]{module_name}[/bold]"
                    )

                    # Directly call the function with the argument list
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
