from __future__ import annotations

import shlex
from dataclasses import dataclass
from typing import List, Optional

from rich.console import Console
from rich.table import Table

from . import render
from .render import render_subagent_event
from .session import SessionManager
from storycraftr.subagents import SubAgentJobManager, seed_default_roles


@dataclass
class CommandContext:
    console: Console
    session_manager: SessionManager
    transcript: List[dict]
    assistant: object
    book_path: str
    job_manager: Optional[SubAgentJobManager] = None


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

    if cmd == "sub-agent":
        _handle_sub_agent(parts[1:], context)
        return None

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
[bold]:sub-agent !list[/bold]     List available sub-agent roles
[bold]:sub-agent !status[/bold]   Show queued/background jobs
[bold]:sub-agent !command[/bold]  Launch `!outline`, `!chapters`, etc. in background
        """
    )


def _handle_sub_agent(args: List[str], context: CommandContext) -> None:
    manager = context.job_manager
    if manager is None:
        context.console.print(
            "[red]Sub-agent support is disabled in this session.[/red]"
        )
        return
    if not args:
        context.console.print(
            "[yellow]Usage: :sub-agent !command [role] [args][/yellow]"
        )
        return

    action = args[0]
    if action == "!list":
        _render_roles(manager, context.console)
        return
    if action == "!describe":
        if len(args) < 2:
            context.console.print("[yellow]Usage: :sub-agent !describe <role>[/yellow]")
            return
        role = manager.get_role(args[1])
        if not role:
            context.console.print(f"[red]Role '{args[1]}' not found.[/red]")
            return
        _render_role_details(role, context.console)
        return
    if action == "!status":
        _render_job_status(manager, context.console)
        return
    if action == "!logs":
        if len(args) < 2:
            context.console.print("[yellow]Usage: :sub-agent !logs <role>[/yellow]")
            return
        _render_logs(args[1], manager, context.console)
        return
    if action == "!seed":
        _handle_seed(args[1:], context)
        manager.reload_roles()
        _render_roles(manager, context.console)
        return

    if not action.startswith("!"):
        context.console.print("[yellow]Commands must start with '!'.[/yellow]")
        return

    role_candidate = None
    payload_args = args[1:]
    if payload_args:
        candidate = payload_args[0]
        if manager.get_role(candidate):
            role_candidate = candidate
            payload_args = payload_args[1:]

    try:
        job = manager.submit(
            command_token=action, args=payload_args, role_slug=role_candidate
        )
        event = {"type": "queued", "job": job.to_dict()}
        render_subagent_event(context.console, event)
    except ValueError as exc:
        context.console.print(f"[red]{exc}[/red]")


def _render_roles(manager: SubAgentJobManager, console: Console) -> None:
    roles = manager.list_roles()
    if not roles:
        console.print("[yellow]No roles configured. Run :sub-agent !seed.[/yellow]")
        return
    table = Table(title="Sub-Agent Roles")
    table.add_column("Role", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Commands", style="magenta")
    for role in roles:
        table.add_row(
            role.slug,
            role.description,
            ", ".join(role.command_whitelist),
        )
    console.print(table)


def _render_role_details(role, console: Console) -> None:
    console.print(
        f"[bold]{role.name}[/bold] ({role.slug}) - {role.description}\n"
        f"[italic]Persona:[/italic] {role.persona or 'n/a'}\n"
        f"[italic]Commands:[/italic] {', '.join(role.command_whitelist)}\n"
        f"[italic]Language:[/italic] {role.language}"
    )


def _render_job_status(manager: SubAgentJobManager, console: Console) -> None:
    jobs = manager.list_jobs()
    if not jobs:
        console.print("[italic]No background jobs yet.[/italic]")
        return
    table = Table(title="Sub-Agent Jobs", show_lines=True)
    table.add_column("Job", no_wrap=True)
    table.add_column("Role", style="cyan", no_wrap=True)
    table.add_column("Command", style="white")
    table.add_column("Status", style="magenta", no_wrap=True)
    for job in jobs[:10]:
        table.add_row(
            job.job_id[:8],
            job.role.slug,
            job.command_text,
            job.status,
        )
    console.print(table)


def _render_logs(role_slug: str, manager: SubAgentJobManager, console: Console) -> None:
    files = manager.role_logs(role_slug, limit=5)
    if not files:
        console.print(f"[yellow]No logs for role '{role_slug}'.[/yellow]")
        return
    console.print(f"[bold]Recent logs for {role_slug}:[/bold]")
    for path in files:
        console.print(f"- {path.name}")


def _handle_seed(args: List[str], context: CommandContext) -> None:
    language = "en"
    force = False
    idx = 0
    while idx < len(args):
        token = args[idx]
        if token == "--language" and idx + 1 < len(args):  # nosec B105
            language = args[idx + 1]
            idx += 2
            continue
        if token == "--force":  # nosec B105
            force = True
            idx += 1
            continue
        idx += 1

    written = seed_default_roles(context.book_path, language=language, force=force)
    if written:
        context.console.print(
            f"[green]Seeded {len(written)} role definition(s) for language '{language}'.[/green]"
        )
    else:
        context.console.print(
            f"[yellow]Roles already exist. Use --force to overwrite (language '{language}').[/yellow]"
        )
