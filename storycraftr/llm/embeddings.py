from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from langchain_huggingface import HuggingFaceEmbeddings


@dataclass
class EmbeddingSettings:
    """Normalized configuration to construct embedding models."""

    model_name: str = "BAAI/bge-large-en-v1.5"
    device: str = "auto"
    cache_dir: Optional[str] = None
    normalize: Optional[bool] = None


def _should_normalize(model_name: str, explicit: Optional[bool]) -> bool:
    if explicit is not None:
        return explicit
    return "bge" in model_name.lower()


def build_embedding_model(settings: EmbeddingSettings):
    """
    Build a HuggingFace embedding model with sane defaults for local usage.
    """

    model_name_lower = settings.model_name.lower()
    if model_name_lower in {"fake", "offline", "offline-placeholder"}:
        raise RuntimeError(
            "Embedding provider is set to a placeholder model. Configure a valid embedding model."
        )

    model_kwargs = {}
    if settings.device and settings.device != "auto":
        model_kwargs["device"] = settings.device
    cache_dir = settings.cache_dir or os.getenv("STORYCRAFTR_EMBED_CACHE")
    if cache_dir:
        model_kwargs["cache_dir"] = cache_dir

    encode_kwargs = {}
    if _should_normalize(settings.model_name, settings.normalize):
        encode_kwargs["normalize_embeddings"] = True

    try:
        return HuggingFaceEmbeddings(
            model_name=settings.model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )
    except Exception as exc:
        raise RuntimeError(
            f"Failed to load embedding model '{settings.model_name}'. "
            "Install prerequisites or provide a reachable model."
        ) from exc
