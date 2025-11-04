"""
LangChain service layer for StoryCraftr.

This package exposes helpers to build chat models, embeddings and supporting
infrastructure from the project configuration while keeping provider-specific
details isolated from the rest of the codebase.
"""

from .factory import build_chat_model, LLMSettings  # noqa: F401
from .embeddings import build_embedding_model, EmbeddingSettings  # noqa: F401
