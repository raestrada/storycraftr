from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional
import warnings

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import FakeEmbeddings


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
        return FakeEmbeddings(size=1024)

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
        warnings.warn(
            f"Falling back to FakeEmbeddings because '{settings.model_name}' could not be loaded ({exc})."
        )
        return FakeEmbeddings(size=1024)
