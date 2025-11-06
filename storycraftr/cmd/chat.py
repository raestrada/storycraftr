from __future__ import annotations

from pathlib import Path
from queue import Empty, Queue
from typing import Dict, List, Optional

import click
import os
import time
from rich.console import Console
from rich.markdown import Markdown
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout

from storycraftr.chat.commands import CommandContext, handle_command
from storycraftr.chat.render import (
    render_footer,
    render_session_loaded,
    render_subagent_event,
    render_turn,
)
from storycraftr.chat.session import SessionManager
from storycraftr.chat.module_runner import ModuleCommandError, run_module_command
from storycraftr.integrations import (
    VS_CODE_EXTENSION_ID,
    create_vscode_event_emitter,
    install_vscode_extension,
)
from storycraftr.subagents import SubAgentJobManager
from storycraftr.agent.agents import (
    create_message,
    create_or_get_assistant,
    get_thread,
)
from storycraftr.utils.core import load_book_config

console = Console()


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


def _execute_module_command(raw: str, *, book_path: str) -> None:
    try:
        run_module_command(raw, console=console, book_path=book_path)
    except ModuleCommandError as exc:
        console.print(f"[red]{exc}[/red]")


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


def _render_session_footer(job_manager: SubAgentJobManager, footer_meta: dict) -> None:
    if not job_manager:
        return
    render_footer(
        console,
        job_stats=job_manager.job_stats(),
        **footer_meta,
    )


def _drain_subagent_events(
    event_queue: Queue,
    job_manager: SubAgentJobManager,
    footer_meta: dict,
) -> None:
    flushed = False
    while True:
        try:
            event = event_queue.get_nowait()
        except Empty:
            break
        render_subagent_event(console, event)
        flushed = True
    if flushed:
        _render_session_footer(job_manager, footer_meta)


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

    vscode_emitter = create_vscode_event_emitter(book_path=book_path, console=console)
    if vscode_emitter:
        console.print(
            "[cyan]StoryCraftr ships a companion VS Code extension that mirrors chat "
            "output and sub-agent jobs in the editor.[/cyan]"
        )
        if click.confirm(
            f"Install/update the VS Code extension '{VS_CODE_EXTENSION_ID}' now?",
            default=True,
        ):
            install_vscode_extension(console)
        else:
            console.print(
                "[dim]Skip installation for now. "
                "Run 'code --install-extension "
                f"{VS_CODE_EXTENSION_ID}' later to enable editor integration.[/dim]"
            )

    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)

    footer_meta = {
        "book_name": getattr(config, "book_name", Path(book_path).name),
        "language": getattr(config, "primary_language", "en"),
        "llm_provider": getattr(config, "llm_provider", "unknown"),
        "llm_model": getattr(config, "llm_model", "unknown"),
        "embed_model": getattr(config, "embed_model", "unknown"),
    }

    subagent_events: Queue = Queue()

    def _forward_job_event(event_type: str, job_payload: dict) -> None:
        if vscode_emitter:
            vscode_emitter.emit(f"sub_agent.{event_type}", job_payload)

    job_manager = SubAgentJobManager(
        book_path,
        console,
        event_queue=subagent_events,
        event_callback=_forward_job_event,
    )
    session_manager = SessionManager(book_path)
    if session_name:
        session_manager.autosave_name = session_name
    transcript: List[Dict] = []

    if vscode_emitter:
        vscode_emitter.emit(
            "session.started",
            {
                "book_path": str(book_path),
                "metadata": footer_meta,
                "session": session_name,
            },
        )

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
        if vscode_emitter:
            vscode_emitter.emit(
                "chat.turn",
                {
                    "user": prompt,
                    "answer": turn.get("answer"),
                    "documents": turn.get("documents"),
                    "duration": turn.get("duration"),
                },
            )
        _drain_subagent_events(subagent_events, job_manager, footer_meta)
        _render_session_footer(job_manager, footer_meta)
        job_manager.shutdown()
        return

    console.print(
        f"Starting chat for [bold]{book_path}[/bold]. Type [bold green]exit()[/bold green] to quit."
    )
    _print_inline_help()
    _render_session_footer(job_manager, footer_meta)

    session = PromptSession(history=InMemoryHistory())

    while True:
        _drain_subagent_events(subagent_events, job_manager, footer_meta)
        try:
            user_input = session.prompt("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit()":
                console.print("[bold red]Exiting chat...[/bold red]")
                break

            if user_input.lower() == "help()":
                _print_inline_help()
                _drain_subagent_events(subagent_events, job_manager, footer_meta)
                _render_session_footer(job_manager, footer_meta)
                continue

            if user_input.startswith(":"):
                if vscode_emitter:
                    vscode_emitter.emit(
                        "chat.command",
                        {
                            "input": user_input,
                            "session": session_name,
                        },
                    )
                ctx = CommandContext(
                    console=console,
                    session_manager=session_manager,
                    transcript=transcript,
                    assistant=assistant,
                    book_path=book_path,
                    job_manager=job_manager,
                    event_emitter=vscode_emitter,
                )

                command_result: List[dict] | None = None

                def _run_command():
                    nonlocal command_result
                    result = handle_command(user_input, ctx)
                    if isinstance(result, list):
                        command_result = result

                with patch_stdout(raw=True):
                    _run_command()
                if command_result is not None:
                    transcript[:] = command_result
                _drain_subagent_events(subagent_events, job_manager, footer_meta)
                _render_session_footer(job_manager, footer_meta)
                continue

            if user_input.startswith("!"):
                if vscode_emitter:
                    vscode_emitter.emit(
                        "chat.command",
                        {
                            "input": user_input,
                            "session": session_name,
                        },
                    )
                with patch_stdout(raw=True):
                    _execute_module_command(user_input[1:], book_path=book_path)
                _drain_subagent_events(subagent_events, job_manager, footer_meta)
                _render_session_footer(job_manager, footer_meta)
                continue

            turn = _run_turn(book_path, assistant, thread, user_input)
            transcript.append(turn)
            render_turn(console, turn, len(transcript))
            session_manager.autosave(transcript)
            if vscode_emitter:
                vscode_emitter.emit(
                    "chat.turn",
                    {
                        "user": user_input,
                        "answer": turn.get("answer"),
                        "documents": turn.get("documents"),
                        "duration": turn.get("duration"),
                    },
                )
            _drain_subagent_events(subagent_events, job_manager, footer_meta)
            _render_session_footer(job_manager, footer_meta)

        except KeyboardInterrupt:
            console.print("[bold red]Exiting chat...[/bold red]")
            break
        except Exception as exc:
            console.print(f"[bold red]Error: {exc}[/bold red]")
    job_manager.shutdown()
    if vscode_emitter:
        vscode_emitter.emit(
            "session.ended",
            {
                "book_path": str(book_path),
                "session": session_name,
            },
        )
