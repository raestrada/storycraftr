from __future__ import annotations

import textwrap
from typing import Iterable, List, Mapping

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table


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
