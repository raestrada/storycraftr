import io
import json

from storycraftr.integrations.vscode import (
    VSCodeEventEmitter,
    create_vscode_event_emitter,
    install_vscode_extension,
    is_running_in_vscode,
)


def test_is_running_in_vscode_detects_term_program():
    env = {"TERM_PROGRAM": "VSCODE"}
    assert is_running_in_vscode(env) is True


def test_is_running_in_vscode_detects_other_markers():
    env = {"VSCODE_PID": "1234"}
    assert is_running_in_vscode(env) is True


def test_is_running_in_vscode_returns_false_else():
    env = {"TERM_PROGRAM": "xterm"}
    assert is_running_in_vscode(env) is False


def test_vscode_event_emitter_writes_jsonl(tmp_path, monkeypatch):
    book_path = tmp_path / "novel"
    book_path.mkdir()
    emitter = VSCodeEventEmitter(str(book_path))
    emitter.emit("session.started", {"foo": "bar"})

    data = emitter.path.read_text(encoding="utf-8").strip().splitlines()
    assert len(data) == 1
    entry = json.loads(data[0])
    assert entry["event"] == "session.started"
    assert entry["payload"] == {"foo": "bar"}


def test_create_vscode_event_emitter_respects_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("TERM_PROGRAM", "vscode")
    from rich.console import Console

    emitter = create_vscode_event_emitter(
        book_path=str(tmp_path),
        console=Console(file=io.StringIO(), force_terminal=False),
    )
    assert emitter is not None


def test_install_vscode_extension_handles_missing_binary(monkeypatch):
    from rich.console import Console

    monkeypatch.setattr(
        "storycraftr.integrations.vscode._find_vscode_binary", lambda: None
    )
    console = Console(file=io.StringIO(), force_terminal=False)
    assert install_vscode_extension(console) is False


def test_install_vscode_extension_success(monkeypatch):
    from rich.console import Console

    monkeypatch.setattr(
        "storycraftr.integrations.vscode._find_vscode_binary",
        lambda: "/usr/bin/code",
    )

    class Result:
        returncode = 0
        stdout = "installed"
        stderr = ""

    monkeypatch.setattr(
        "subprocess.run",
        lambda *args, **kwargs: Result(),
    )
    console = Console(file=io.StringIO(), force_terminal=False)
    assert install_vscode_extension(console) is True


def test_install_vscode_extension_failure(monkeypatch):
    from rich.console import Console

    monkeypatch.setattr(
        "storycraftr.integrations.vscode._find_vscode_binary",
        lambda: "/usr/bin/code",
    )

    class Result:
        returncode = 1
        stdout = ""
        stderr = "error"

    monkeypatch.setattr(
        "subprocess.run",
        lambda *args, **kwargs: Result(),
    )
    console = Console(file=io.StringIO(), force_terminal=False)
    assert install_vscode_extension(console) is False
