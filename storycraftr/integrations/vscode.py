from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Optional

from rich.console import Console


_VS_CODE_SENTINELS = {
    "TERM_PROGRAM": "vscode",
    "VSCODE_PID": None,
    "VSCODE_IPC_HOOK": None,
    "CODE_PORTABLE_EXECUTABLE": None,
    "VSCODE_CWD": None,
}


def is_running_in_vscode(env: Optional[dict] = None) -> bool:
    """Best-effort detection that StoryCraftr runs inside a VS Code terminal."""
    env = env or os.environ
    term_program = env.get("TERM_PROGRAM", "").lower()
    if term_program == "vscode":
        return True
    for key, expected in _VS_CODE_SENTINELS.items():
        if key not in env:
            continue
        if expected is None:
            return True
        if str(env.get(key, "")).lower() == expected:
            return True
    return False


class VSCodeEventEmitter:
    """
    Emits JSON lines describing StoryCraftr events so a VS Code extension
    can mirror chat output, background jobs, etc.
    """

    def __init__(self, book_path: str):
        self._book_path = Path(book_path)
        self._events_path = self._book_path / ".storycraftr" / "vscode-events.jsonl"
        self._events_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    @property
    def path(self) -> Path:
        return self._events_path

    def emit(self, event_type: str, payload: dict) -> None:
        entry = {
            "event": event_type,
            "payload": payload,
        }
        data = json.dumps(entry, ensure_ascii=False)
        with self._lock:
            with self._events_path.open("a", encoding="utf-8") as handle:
                handle.write(data + "\n")


def create_vscode_event_emitter(
    *,
    book_path: str,
    console: Console,
) -> Optional[VSCodeEventEmitter]:
    if not is_running_in_vscode():
        return None

    emitter = VSCodeEventEmitter(book_path)
    console.print(
        "[cyan]VS Code environment detected.[/cyan] "
        "StoryCraftr is recording events to "
        f"[bold]{emitter.path}[/bold]. Install the upcoming VS Code extension "
        "to mirror chat output, job status, and file edits automatically."
    )
    console.print(
        "[dim]Tip: delete the JSONL file if you want to reset the integration.[/dim]"
    )
    return emitter
