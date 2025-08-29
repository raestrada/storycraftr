from dataclasses import dataclass
from typing import Protocol, List

@dataclass
class DocumentChunk:
    """A chunk of a document."""
    page_content: str
    metadata: dict

class EmbeddingFunction(Protocol):
    """A protocol for embedding functions."""
    def __call__(self, input: List[str]) -> List[List[float]]:
        ...
