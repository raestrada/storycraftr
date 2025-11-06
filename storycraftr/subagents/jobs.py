from __future__ import annotations

import json
import shlex
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass, field
from datetime import datetime, timezone
from importlib import import_module
from io import StringIO
from pathlib import Path
from queue import Queue
from typing import Dict, List, Optional

from rich.console import Console

from storycraftr.chat.module_runner import ModuleCommandError, run_module_command
from storycraftr.utils.core import load_book_config

from .models import SubAgentRole
from .storage import LOGS_DIRNAME, ensure_storage_dirs, load_roles, seed_default_roles


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class SubAgentJob:
    job_id: str
    role: SubAgentRole
    command_text: str
    status: str = "pending"
    created_at: datetime = field(default_factory=_utcnow)
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    output: str = ""
    error: Optional[str] = None
    log_path: Optional[Path] = None

    def to_dict(self) -> dict:
        return {
            "job_id": self.job_id,
            "role": self.role.slug,
            "role_name": self.role.name,
            "command_text": self.command_text,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "output": self.output,
            "error": self.error,
            "log_path": str(self.log_path) if self.log_path else None,
        }


class SubAgentJobManager:
    """
    Coordinates role discovery, job submission, and logging for sub-agents.
    """

    def __init__(
        self,
        book_path: str,
        console: Console,
        *,
        event_queue: Optional[Queue] = None,
    ):
        self.book_path = Path(book_path)
        self.console = console
        self.event_queue = event_queue
        self.root = ensure_storage_dirs(book_path)
        self.logs_root = self.root / LOGS_DIRNAME
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="subagent")
        self.roles = self._ensure_roles()
        self.jobs: Dict[str, SubAgentJob] = {}

    def shutdown(self) -> None:
        self.executor.shutdown(wait=False, cancel_futures=True)

    # Role management -----------------------------------------------------------------

    def _ensure_roles(self) -> Dict[str, SubAgentRole]:
        roles = load_roles(str(self.book_path))
        if roles:
            return roles
        language = "en"
        config = load_book_config(str(self.book_path))
        if config and getattr(config, "primary_language", None):
            language = config.primary_language
        seed_default_roles(str(self.book_path), language=language, force=False)
        return load_roles(str(self.book_path))

    def reload_roles(self) -> None:
        with self.lock:
            self.roles = load_roles(str(self.book_path))

    def list_roles(self) -> List[SubAgentRole]:
        with self.lock:
            return sorted(self.roles.values(), key=lambda r: r.name.lower())

    def get_role(self, slug: str) -> Optional[SubAgentRole]:
        slug = slug.lower()
        with self.lock:
            return self.roles.get(slug)

    # Job submission -------------------------------------------------------------------

    def submit(
        self,
        *,
        command_token: str,
        args: List[str],
        role_slug: Optional[str] = None,
    ) -> SubAgentJob:
        if not command_token.startswith("!"):
            raise ValueError("Command token must start with '!'.")

        role = self._select_role(command_token, role_slug)
        if role is None:
            raise ValueError(
                "No role found for the requested command. "
                "Use :sub-agent !list to inspect available roles."
            )

        payload_tokens = [command_token[1:]] + args
        command_text = shlex.join(payload_tokens)
        job = SubAgentJob(job_id=uuid.uuid4().hex, role=role, command_text=command_text)

        with self.lock:
            self.jobs[job.job_id] = job

        self._emit_event("queued", job)
        self.executor.submit(self._run_job, job)
        return job

    def list_jobs(self) -> List[SubAgentJob]:
        with self.lock:
            return sorted(
                self.jobs.values(), key=lambda job: job.created_at, reverse=True
            )

    def job_stats(self) -> Dict[str, int]:
        with self.lock:
            stats = {"pending": 0, "running": 0, "succeeded": 0, "failed": 0}
            for job in self.jobs.values():
                if job.status in stats:
                    stats[job.status] += 1
            return stats

    # Helpers -------------------------------------------------------------------------

    def _select_role(
        self, command_token: str, role_slug: Optional[str]
    ) -> Optional[SubAgentRole]:
        with self.lock:
            if role_slug:
                return self.roles.get(role_slug.lower())
            for role in self.roles.values():
                if command_token in role.command_whitelist:
                    return role
        return None

    def _run_job(self, job: SubAgentJob) -> None:
        job.started_at = _utcnow()
        job.status = "running"
        self._emit_event("running", job)
        buffer_out = StringIO()
        buffer_err = StringIO()
        job_console = Console(file=buffer_out, force_terminal=False, color_system=None)

        swaps = _swap_storycraftr_consoles(job_console)
        try:
            try:
                with redirect_stdout(buffer_out), redirect_stderr(buffer_err):
                    run_module_command(
                        job.command_text,
                        console=job_console,
                        book_path=str(self.book_path),
                    )
                job.status = "succeeded"
            except ModuleCommandError as exc:
                job.status = "failed"
                job.error = str(exc)
            except Exception as exc:  # pragma: no cover - safety net
                job.status = "failed"
                job.error = repr(exc)
            finally:
                job.finished_at = _utcnow()
                stdout_text = buffer_out.getvalue()
                stderr_text = buffer_err.getvalue()
                if stderr_text:
                    stdout_text = f"{stdout_text}\n\n[stderr]\n{stderr_text}".strip()
                job.output = stdout_text.strip()
                self._persist_job(job)
                self._emit_event(job.status, job)
        finally:
            _restore_storycraftr_consoles(swaps)

    def _persist_job(self, job: SubAgentJob) -> None:
        log_dir = self.logs_root / job.role.slug
        log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = (job.finished_at or _utcnow()).strftime("%Y%m%d-%H%M%S")
        log_base = f"{timestamp}-{job.job_id}"
        md_path = log_dir / f"{log_base}.md"
        metadata_path = log_dir / f"{log_base}.json"

        if job.output or job.error:
            md_body = [
                f"# Sub-Agent Run · {job.role.name}",
                f"- Role: {job.role.slug}",
                f"- Command: {job.command_text}",
                f"- Status: {job.status}",
                f"- Started: {job.started_at or job.created_at}",
                f"- Finished: {job.finished_at or ''}",
                "",
                "## Output",
                job.output or "_No output recorded._",
            ]
            if job.error:
                md_body.extend(["", "## Error", job.error])
            md_path.write_text("\n".join(md_body), encoding="utf-8")
            job.log_path = md_path

        metadata_path.write_text(json.dumps(job.to_dict(), indent=2), encoding="utf-8")

    # Logs ----------------------------------------------------------------------------

    def role_logs(self, role_slug: str, limit: int = 5) -> List[Path]:
        role_dir = self.logs_root / role_slug.lower()
        if not role_dir.exists():
            return []
        files = sorted(role_dir.glob("*.md"), reverse=True)
        return files[:limit]

    # Internal helpers -------------------------------------------------------

    def _emit_event(self, event_type: str, job: SubAgentJob) -> None:
        if not self.event_queue:
            return
        payload = {
            "type": event_type,
            "job": job.to_dict(),
        }
        self.event_queue.put(payload)


_CONSOLE_MODULES = [
    "storycraftr.cmd.story.chapters",
    "storycraftr.cmd.story.iterate",
    "storycraftr.cmd.story.outline",
    "storycraftr.cmd.story.worldbuilding",
    "storycraftr.cmd.story.publish",
    "storycraftr.agent.story.chapters",
    "storycraftr.agent.story.iterate",
    "storycraftr.agent.story.outline",
    "storycraftr.agent.story.worldbuilding",
]


def _swap_storycraftr_consoles(replacement: Console):
    swaps = []
    for module_name in _CONSOLE_MODULES:
        try:
            module = import_module(module_name)
        except ModuleNotFoundError:
            continue
        console_obj = getattr(module, "console", None)
        if isinstance(console_obj, Console):
            swaps.append((module, console_obj))
            setattr(module, "console", replacement)
    return swaps


def _restore_storycraftr_consoles(swaps) -> None:
    for module, original in swaps:
        setattr(module, "console", original)
