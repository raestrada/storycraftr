from __future__ import annotations

import os
import time
import click
from pathlib import Path
from typing import Dict, List

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from rich.console import Console
from rich.markdown import Markdown

import storycraftr.cmd.story as story_cmd
from storycraftr.chat import (
    CommandContext,
    SessionManager,
    handle_command,
    render_session_loaded,
    render_turn,
)
from storycraftr.utils.core import load_book_config
from storycraftr.agent.agents import (
    create_message,
    create_or_get_assistant,
    get_thread,
)

console = Console()

command_modules = {
    "iterate": story_cmd.iterate,
    "outline": story_cmd.outline,
    "worldbuilding": story_cmd.worldbuilding,
    "chapters": story_cmd.chapters,
}


def _format_user_prompt(message: str) -> str:
    return f"Answer the next prompt formatted on markdown (text): {message}".strip()


def _summarise_documents(documents, limit: int = 5, max_chars: int = 400) -> List[Dict]:
    summaries: List[Dict] = []
    if not documents:
        return summaries
    for doc in documents[:limit]:
        excerpt = getattr(doc, "page_content", str(doc))
        excerpt = excerpt.strip()
        if len(excerpt) > max_chars:
            excerpt = excerpt[: max_chars - 1].rstrip() + "…"
        source = getattr(doc, "metadata", {}).get("source", "context")
        summaries.append({"source": source, "excerpt": excerpt})
    return summaries


def _run_turn(
    book_path, assistant, thread, user_text: str, force_single_answer: bool = True
):
    formatted_prompt = _format_user_prompt(user_text)
    start = time.perf_counter()
    answer = create_message(
        book_path,
        thread_id=thread.id,
        content=formatted_prompt,
        assistant=assistant,
        force_single_answer=force_single_answer,
    )
    duration = time.perf_counter() - start
    documents = _summarise_documents(assistant.last_documents)
    return {
        "user": user_text,
        "answer": answer,
        "duration": duration,
        "documents": documents,
    }


def _execute_module_command(raw: str) -> None:
    try:
        parts = raw.split()
        if len(parts) < 2:
            console.print("[yellow]Usage: !<module> <command> [args][/yellow]")
            return
        module_name = parts[0]
        command_name = parts[1].replace("-", "_")
        command_args = parts[2:]
        module = command_modules.get(module_name)
        if not module:
            console.print(f"[yellow]Unknown module '{module_name}'.[/yellow]")
            return
        func = getattr(module, command_name, None)
        if hasattr(func, "callback"):
            func = func.callback
        if not callable(func):
            console.print(
                f"[yellow]Command '{command_name}' not found in module '{module_name}'.[/yellow]"
            )
            return
        console.print(f"[cyan]Running {module_name}.{command_name}…[/cyan]")
        func(*command_args)
    except Exception as exc:
        console.print(f"[red]Error executing module command:[/red] {exc}")


def _print_inline_help() -> None:
    console.print(
        Markdown(
            """
### Chat Shortcuts
- Type `:help` for chat commands (sessions, status, etc.).
- Use `!module command` to call StoryCraftr utilities (e.g., `!outline general-outline …`).
- `exit()` closes the session.
            """
        )
    )


@click.command()
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
@click.option(
    "--prompt",
    type=str,
    default=None,
    help="Run a single prompt in non-interactive mode and print the response.",
)
@click.option(
    "--session-name",
    type=str,
    default=None,
    help="Load or autosave conversation under this name.",
)
def chat(book_path=None, prompt=None, session_name=None):
    if not book_path:
        book_path = os.getcwd()

    config = load_book_config(book_path)
    if not config:
        return None

    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)

    session_manager = SessionManager(book_path)
    if session_name:
        session_manager.autosave_name = session_name
    transcript: List[Dict] = []

    if session_name:
        try:
            transcript = session_manager.load(session_name)
            render_session_loaded(console, session_name, transcript)
            for idx, turn in enumerate(transcript, start=1):
                render_turn(console, turn, idx)
        except FileNotFoundError:
            console.print(
                f"[yellow]Session '{session_name}' not found. A new session will be created.[/yellow]"
            )

    if prompt is not None:
        turn = _run_turn(book_path, assistant, thread, prompt)
        render_turn(console, turn, len(transcript) + 1)
        return

    console.print(
        f"Starting chat for [bold]{book_path}[/bold]. Type [bold green]exit()[/bold green] to quit."
    )
    _print_inline_help()

    session = PromptSession(history=InMemoryHistory())

    while True:
        try:
            user_input = session.prompt("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit()":
                console.print("[bold red]Exiting chat...[/bold red]")
                break

            if user_input.lower() == "help()":
                _print_inline_help()
                continue

            if user_input.startswith(":"):
                ctx = CommandContext(
                    console=console,
                    session_manager=session_manager,
                    transcript=transcript,
                    assistant=assistant,
                )
                result = handle_command(user_input, ctx)
                if isinstance(result, list):
                    transcript[:] = result
                continue

            if user_input.startswith("!"):
                _execute_module_command(user_input[1:])
                continue

            turn = _run_turn(book_path, assistant, thread, user_input)
            transcript.append(turn)
            render_turn(console, turn, len(transcript))
            session_manager.autosave(transcript)

        except KeyboardInterrupt:
            console.print("[bold red]Exiting chat...[/bold red]")
            break
        except Exception as exc:
            console.print(f"[bold red]Error: {exc}[/bold red]")
