from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Mapping

from rich.console import Console

console = Console()

_KEY_FILE_MAP: Mapping[str, tuple[str, ...]] = {
    "OPENAI_API_KEY": ("openai_api_key.txt",),
    "OPENROUTER_API_KEY": ("openrouter_api_key.txt",),
    "OLLAMA_API_KEY": ("ollama_api_key.txt",),
}


def load_local_credentials(extra_dirs: Iterable[Path] | None = None) -> None:
    """
    Attempt to populate provider API key environment variables from local config files.

    This keeps support for the existing ~/.storycraftr and ~/.papercraftr layouts while
    allowing additional directories (e.g., custom project paths) to be supplied.
    """

    home_dir = Path.home()
    search_dirs = [
        home_dir / ".storycraftr",
        home_dir / ".papercraftr",
    ]
    if extra_dirs:
        search_dirs.extend(Path(p) for p in extra_dirs)

    for env_var, candidate_files in _KEY_FILE_MAP.items():
        if os.getenv(env_var):
            continue
        for base_dir in search_dirs:
            for filename in candidate_files:
                key_path = base_dir / filename
                if key_path.exists():
                    api_key = key_path.read_text(encoding="utf-8").strip()
                    if api_key:
                        os.environ[env_var] = api_key
                        console.print(
                            f"[green]{env_var} loaded from {key_path}[/green]"
                        )
                        break
            if os.getenv(env_var):
                break
