from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class SubAgentRole:
    slug: str
    name: str
    description: str
    command_whitelist: List[str]
    system_prompt: str
    language: str = "en"
    persona: str = ""
    temperature: float = 0.2

    @classmethod
    def from_dict(cls, slug: str, data: dict) -> "SubAgentRole":
        return cls(
            slug=data.get("slug", slug).lower(),
            name=data.get("name", slug.title()),
            description=data.get("description", ""),
            command_whitelist=data.get("command_whitelist", []),
            system_prompt=data.get("system_prompt", ""),
            language=data.get("language", "en"),
            persona=data.get("persona", ""),
            temperature=float(data.get("temperature", 0.2)),
        )

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "name": self.name,
            "description": self.description,
            "command_whitelist": self.command_whitelist,
            "system_prompt": self.system_prompt,
            "language": self.language,
            "persona": self.persona,
            "temperature": self.temperature,
        }
