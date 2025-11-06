from __future__ import annotations

import textwrap
from typing import Iterable, List, Mapping

from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def _truncate(text: str, width: int = 220) -> str:
    text = text.replace("\n", " ").strip()
    return textwrap.shorten(text, width=width, placeholder=" …")


def render_turn(console: Console, turn: Mapping, turn_index: int) -> None:
    user_text = turn.get("user", "")
    answer_text = turn.get("answer", "")
    duration = turn.get("duration")
    docs: List[Mapping] = turn.get("documents", []) or []

    console.print(
        Panel(
            Markdown(user_text or "(vacío)"),
            title=f"[yellow]You · Turn {turn_index}[/yellow]",
            border_style="yellow",
        )
    )

    subtitle = f"Turn {turn_index}"
    if duration is not None:
        subtitle += f" · {duration:.2f}s"

    console.print(
        Panel(
            Markdown(answer_text or "(sin respuesta)"),
            title=f"[green]StoryCraftr · {subtitle}[/green]",
            border_style="green",
        )
    )

    if docs:
        table = Table(title="Retrieved Context", show_lines=True)
        table.add_column("Source", style="cyan", no_wrap=True)
        table.add_column("Excerpt", style="white")

        for doc in docs:
            source = doc.get("source", "context")
            excerpt = _truncate(doc.get("excerpt", ""))
            table.add_row(source, excerpt or "…")

        console.print(table)


def render_status(console: Console, docs: Iterable[Mapping]) -> None:
    docs = list(docs)
    if not docs:
        console.print("[italic yellow]No retrieval context available.[/italic yellow]")
        return

    table = Table(title="Current Retrieval Context", show_lines=True)
    table.add_column("Source", style="cyan", no_wrap=True)
    table.add_column("Excerpt", style="white")
    for doc in docs:
        table.add_row(doc.get("source", "context"), _truncate(doc.get("excerpt", "")))
    console.print(table)


def render_session_loaded(console: Console, name: str, turns: List[Mapping]) -> None:
    console.print(
        Panel(
            f"Loaded session '[bold]{name}[/bold]' with {len(turns)} turns.",
            border_style="blue",
        )
    )


def render_footer(
    console: Console,
    *,
    book_name: str,
    language: str,
    llm_provider: str,
    llm_model: str,
    embed_model: str,
    job_stats: Mapping[str, int],
) -> None:
    info_text = Text(
        f"{book_name} · Lang: {language} · LLM: {llm_provider}/{llm_model} · Embed: {embed_model}",
        style="cyan",
    )
    jobs = job_stats or {}
    job_text = Text(
        f"Sub-Agents — pending:{jobs.get('pending',0)} "
        f"running:{jobs.get('running',0)} "
        f"succeeded:{jobs.get('succeeded',0)} "
        f"failed:{jobs.get('failed',0)}",
        style="magenta",
    )
    console.print(
        Panel(
            Group(info_text, job_text),
            border_style="dim",
            title="[grey62]Session Status[/grey62]",
        )
    )


def render_subagent_event(console: Console, event: Mapping) -> None:
    event_type = event.get("type", "").upper()
    job = event.get("job", {})
    role = job.get("role_name") or job.get("role") or "sub-agent"
    title = f"[magenta]Sub-Agent · {role}[/magenta]"
    lines = [
        f"Event: {event_type}",
        f"Command: {job.get('command_text', '—')}",
    ]
    if job.get("log_path"):
        lines.append(f"Log: {job['log_path']}")
    if job.get("error"):
        lines.append(f"Error: {job['error']}")
    console.print(
        Panel(
            "\n".join(lines),
            border_style="magenta"
            if job.get("status") == "succeeded"
            else "red"
            if job.get("status") == "failed"
            else "cyan",
            title=title,
        )
    )
