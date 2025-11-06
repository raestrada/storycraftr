from __future__ import annotations

import json
import os
import shutil
import subprocess  # nosec B404
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


VS_CODE_EXTENSION_ID = "storycraftr.storycraftr"


def _find_vscode_binary() -> Optional[str]:
    for candidate in ("code", "code-insiders"):
        path = shutil.which(candidate)
        if path:
            return path
    return None


def install_vscode_extension(console: Console, *, force: bool = False) -> bool:
    """
    Attempt to install/update the StoryCraftr VS Code extension.
    """
    binary = _find_vscode_binary()
    if not binary:
        console.print(
            "[yellow]VS Code CLI ('code' or 'code-insiders') not found. "
            "Install VS Code or add the CLI to PATH to enable automatic setup.[/yellow]"
        )
        return False

    args = [binary, "--install-extension", VS_CODE_EXTENSION_ID]
    if force:
        args.append("--force")

    try:
        result = subprocess.run(  # nosec B603
            args,
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception as exc:  # pragma: no cover - defensive
        console.print(f"[red]Failed to run '{binary}': {exc}[/red]")
        return False

    stdout = result.stdout.strip() if result.stdout else ""
    stderr = result.stderr.strip() if result.stderr else ""

    if result.returncode == 0:
        if stdout:
            console.print(stdout)
        console.print(
            "[green]StoryCraftr VS Code extension installed. "
            "Reload VS Code to activate it.[/green]"
        )
        return True

    console.print(
        "[red]VS Code extension installation failed. "
        "Run the 'code --install-extension' command manually to retry.[/red]"
    )
    if stdout:
        console.print(f"[dim]{stdout}[/dim]")
    if stderr:
        console.print(f"[red]{stderr}[/red]")
    return False
