from __future__ import annotations

import shlex
from typing import Dict, List, Optional

import click
from rich.console import Console

import storycraftr.cmd.story as story_cmd

COMMAND_MODULES: Dict[str, object] = {
    "iterate": story_cmd.iterate,
    "outline": story_cmd.outline,
    "worldbuilding": story_cmd.worldbuilding,
    "chapters": story_cmd.chapters,
    "publish": story_cmd.publish,
}


class ModuleCommandError(RuntimeError):
    """Raised when a StoryCraftr module command cannot be executed."""


def run_module_command(
    raw: str,
    *,
    console: Optional[Console] = None,
    book_path: Optional[str] = None,
) -> None:
    """
    Execute a StoryCraftr module command.

    Args:
        raw: Command string without the leading `!` (e.g. `outline general-outline "Prompt"`).
        console: Optional console for user-facing status messages.
        book_path: Optional book path injected as `--book-path` when the command accepts it.
    """
    console = console or Console()
    try:
        parts = shlex.split(raw)
    except ValueError as exc:
        raise ModuleCommandError(f"Could not parse command: {exc}") from exc

    if len(parts) < 2:
        raise ModuleCommandError("Usage: !<module> <command> [args]")

    module_name = parts[0]
    command_name = parts[1].replace("-", "_")
    command_args: List[str] = parts[2:]

    module = COMMAND_MODULES.get(module_name)
    if module is None:
        raise ModuleCommandError(f"Unknown module '{module_name}'.")

    command_obj = getattr(module, command_name, None)
    if command_obj is None:
        raise ModuleCommandError(
            f"Command '{command_name}' not found in module '{module_name}'."
        )

    args = list(command_args)
    if book_path and "--book-path" not in args:
        args.extend(["--book-path", book_path])

    console.print(f"[cyan]Running {module_name}.{command_name}…[/cyan]")

    if isinstance(command_obj, click.Command):
        try:
            command_obj.main(args=args, standalone_mode=False)
            return
        except click.ClickException as exc:
            raise ModuleCommandError(str(exc)) from exc

    if hasattr(command_obj, "callback"):
        command_obj = command_obj.callback

    if not callable(command_obj):
        raise ModuleCommandError(
            f"Executable for '{module_name}.{command_name}' is not callable."
        )

    command_obj(*args)
