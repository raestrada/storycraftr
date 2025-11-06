from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import yaml

from .defaults import get_default_roles_for_language
from .models import SubAgentRole

SUBAGENT_ROOT = ".storycraftr/subagents"
LOGS_DIRNAME = "logs"


def subagent_root(book_path: str) -> Path:
    return Path(book_path) / SUBAGENT_ROOT


def ensure_storage_dirs(book_path: str) -> Path:
    root = subagent_root(book_path)
    root.mkdir(parents=True, exist_ok=True)
    (root / LOGS_DIRNAME).mkdir(parents=True, exist_ok=True)
    return root


def role_file_path(root: Path, slug: str) -> Path:
    return root / f"{slug}.yaml"


def load_roles(book_path: str) -> Dict[str, SubAgentRole]:
    root = ensure_storage_dirs(book_path)
    roles: Dict[str, SubAgentRole] = {}
    for file_path in root.glob("*.yaml"):
        data = yaml.safe_load(file_path.read_text(encoding="utf-8")) or {}
        slug = data.get("slug", file_path.stem).lower()
        role = SubAgentRole.from_dict(slug, data)
        roles[role.slug] = role
    return roles


def seed_default_roles(
    book_path: str,
    language: str = "en",
    *,
    force: bool = False,
) -> List[Path]:
    """
    Materialise the default role YAML files for the project.

    Args:
        book_path: Path to the project root.
        language: Preferred language for prompts; falls back to English.
        force: Overwrite existing files when True.
    Returns:
        A list of file paths that were created or updated.
    """
    root = ensure_storage_dirs(book_path)
    roles = get_default_roles_for_language(language)
    written: List[Path] = []

    for role in roles:
        file_path = role_file_path(root, role.slug)
        if file_path.exists() and not force:
            continue
        file_path.write_text(
            yaml.safe_dump(role.to_dict(), sort_keys=False), encoding="utf-8"
        )
        written.append(file_path)

    return written
