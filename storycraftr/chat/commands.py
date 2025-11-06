from __future__ import annotations

import shlex
from dataclasses import dataclass
from typing import List, Optional

from rich.console import Console

from . import render
from .session import SessionManager


@dataclass
class CommandContext:
    console: Console
    session_manager: SessionManager
    transcript: List[dict]
    assistant: object


def handle_command(raw: str, context: CommandContext) -> Optional[List[dict]]:
    try:
        parts = shlex.split(raw.lstrip(":"))
    except ValueError as exc:
        context.console.print(f"[red]Command parse error:[/red] {exc}")
        return None

    if not parts:
        context.console.print("[yellow]Empty command.[/yellow]")
        return None

    cmd = parts[0].lower()

    if cmd == "help":
        _print_help(context.console)
        return None

    if cmd == "status":
        render.render_status(context.console, context.assistant.last_documents)
        return None

    if cmd == "session":
        return _handle_session(parts[1:], context)

    context.console.print(f"[yellow]Unknown command ':'{cmd}'. Try :help.[/yellow]")
    return None


def _handle_session(args: List[str], context: CommandContext) -> Optional[List[dict]]:
    if not args:
        context.console.print("[yellow]Usage: :session <list|save|load> [...][/yellow]")
        return None

    action = args[0].lower()
    manager = context.session_manager

    if action == "list":
        sessions = manager.list_sessions()
        if sessions:
            context.console.print(
                "[bold]Available sessions:[/bold] " + ", ".join(sessions)
            )
        else:
            context.console.print("[italic]No saved sessions.[/italic]")
        return None

    if action == "save":
        if len(args) < 2:
            context.console.print("[yellow]Usage: :session save <name>[/yellow]")
            return None
        name = args[1]
        manager.save(name, context.transcript)
        context.console.print(f"[green]Session '{name}' saved.[/green]")
        return None

    if action == "load":
        if len(args) < 2:
            context.console.print("[yellow]Usage: :session load <name>[/yellow]")
            return None
        name = args[1]
        try:
            transcript = manager.load(name)
        except FileNotFoundError as exc:
            context.console.print(f"[red]{exc}[/red]")
            return None
        render.render_session_loaded(context.console, name, transcript)
        for idx, turn in enumerate(transcript, start=1):
            render.render_turn(context.console, turn, idx)
        return transcript

    context.console.print(f"[yellow]Unknown session action '{action}'.[/yellow]")
    return None


def _print_help(console: Console) -> None:
    console.print(
        """
[bold]:help[/bold]                Show this message
[bold]:status[/bold]              Display the latest retrieval context
[bold]:session list[/bold]        List saved sessions
[bold]:session save <name>[/bold] Save current conversation
[bold]:session load <name>[/bold] Load and display a saved conversation
        """
    )
