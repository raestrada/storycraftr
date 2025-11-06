from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Mapping


@dataclass
class SessionManager:
    book_path: str
    autosave_name: str = "autosave"
    _directory: Path = field(init=False)

    def __post_init__(self) -> None:
        root = Path(self.book_path)
        storage_root = root / ".storycraftr" / "sessions"
        storage_root.mkdir(parents=True, exist_ok=True)
        self._directory = storage_root

    def list_sessions(self) -> List[str]:
        return sorted(p.stem for p in self._directory.glob("*.json"))

    def _path_for(self, name: str) -> Path:
        safe_name = name.strip().replace("/", "-")
        if not safe_name:
            raise ValueError("Session name cannot be empty.")
        return self._directory / f"{safe_name}.json"

    def save(self, name: str, transcript: List[Mapping]) -> Path:
        path = self._path_for(name)
        with path.open("w", encoding="utf-8") as fh:
            json.dump(transcript, fh, ensure_ascii=False, indent=2)
        return path

    def load(self, name: str) -> List[Mapping]:
        path = self._path_for(name)
        if not path.exists():
            raise FileNotFoundError(f"Session '{name}' not found.")
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def autosave(self, transcript: List[Mapping]) -> None:
        self.save(self.autosave_name, transcript)
