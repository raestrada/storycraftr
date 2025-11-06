import json
import time
from io import StringIO
from pathlib import Path

from rich.console import Console

from storycraftr.subagents import SubAgentJobManager, seed_default_roles


def _minimal_config(tmp_path: Path) -> None:
    config = {
        "book_name": "Test",
        "primary_language": "en",
        "alternate_languages": [],
        "default_author": "Tester",
        "genre": "fantasy",
        "license": "CC",
        "reference_author": "",
        "cli_name": "storycraftr",
        "multiple_answer": True,
        "llm_provider": "openai",
        "llm_model": "gpt-4o",
        "llm_endpoint": "",
        "llm_api_key_env": "",
        "temperature": 0.7,
        "request_timeout": 120,
        "embed_model": "BAAI/bge-large-en-v1.5",
        "embed_device": "auto",
        "embed_cache_dir": "",
    }
    (tmp_path / "storycraftr.json").write_text(json.dumps(config), encoding="utf-8")


def test_seed_default_roles_creates_files(tmp_path):
    _minimal_config(tmp_path)
    written = seed_default_roles(tmp_path, language="en", force=True)
    assert written, "Expected the default role YAML files to be created."
    for path in written:
        assert path.is_file()


def test_job_manager_runs_background_job(monkeypatch, tmp_path):
    _minimal_config(tmp_path)
    seed_default_roles(tmp_path, language="en", force=True)

    captured = {}

    def fake_run_module_command(command_text, console, book_path):
        captured["command"] = command_text
        captured["book_path"] = book_path

    monkeypatch.setattr(
        "storycraftr.subagents.jobs.run_module_command", fake_run_module_command
    )

    manager = SubAgentJobManager(
        str(tmp_path), Console(file=StringIO(), force_terminal=False)
    )

    job = manager.submit(
        command_token="!outline",  # nosec B106
        args=["general-outline", "Refine the prologue"],
        role_slug="editor",
    )

    for _ in range(50):
        status = manager.list_jobs()[0].status
        if status in {"succeeded", "failed"}:
            break
        time.sleep(0.1)

    manager.shutdown()

    assert captured["book_path"] == str(tmp_path)
    assert captured["command"].startswith("outline general-outline")
    assert manager.list_jobs()[0].status == "succeeded"
