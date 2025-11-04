from __future__ import annotations

import glob
import os
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional
from uuid import uuid4

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_community.vectorstores import Chroma
from rich.console import Console
from rich.progress import Progress

from storycraftr.llm import build_chat_model, build_embedding_model
from storycraftr.prompts.story.core import FORMAT_OUTPUT
from storycraftr.utils.core import (
    generate_prompt_with_hash,
    load_book_config,
    llm_settings_from_config,
    embedding_settings_from_config,
)
from storycraftr.vectorstores import build_chroma_store

console = Console()


@dataclass
class ConversationThread:
    id: str
    book_path: str
    messages: List[HumanMessage | AIMessage] = field(default_factory=list)


@dataclass
class LangChainAssistant:
    id: str
    book_path: str
    config: object
    llm: BaseChatModel
    vector_store: Optional[Chroma]
    behavior: str
    retriever: Optional[object] = None

    def ensure_vector_store(self, force: bool = False) -> None:
        """
        Ensure that the local Chroma store is populated with Markdown content.
        """

        if self.vector_store is None:
            raise RuntimeError(
                "Vector store is not initialised. Ensure embeddings are available before continuing."
            )

        persist_dir_str = getattr(
            self.vector_store,
            "_persist_directory",
            str(Path(self.book_path) / "vector_store"),
        )
        persist_dir = Path(persist_dir_str)
        if force and persist_dir.exists():
            shutil.rmtree(persist_dir, ignore_errors=True)

        try:
            needs_refresh = (
                force or not persist_dir.exists() or not any(persist_dir.iterdir())
            )
        except OSError:
            needs_refresh = True

        if needs_refresh:
            documents = load_markdown_documents(self.book_path)
            if not documents:
                raise RuntimeError(
                    f"No Markdown documents available to index for project {self.book_path}."
                )
            else:
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000, chunk_overlap=150
                )
                chunks = splitter.split_documents(documents)
                try:
                    self.vector_store.add_documents(chunks)
                except Exception as exc:
                    raise RuntimeError(
                        f"Failed to populate vector store: {exc}"
                    ) from exc

        try:
            self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 6})
        except Exception as exc:
            raise RuntimeError(
                f"Unable to construct retriever from vector store: {exc}"
            ) from exc

    @property
    def system_prompt(self) -> str:
        format_prompt = FORMAT_OUTPUT.format(
            reference_author=getattr(self.config, "reference_author", ""),
            language=getattr(self.config, "primary_language", "en"),
        )
        meta = (
            f"Project: {Path(self.book_path).name}\n"
            f"Primary language: {getattr(self.config, 'primary_language', 'en')}\n"
        )
        return f"{self.behavior.strip()}\n\n{meta}{format_prompt}"


_ASSISTANT_CACHE: Dict[str, LangChainAssistant] = {}
_THREADS: Dict[str, ConversationThread] = {}


def load_markdown_documents(book_path: str) -> List[Document]:
    """
    Load Markdown files from the project for indexing.
    """

    patterns = [
        os.path.join(book_path, "**", "*.md"),
    ]
    documents: List[Document] = []

    for pattern in patterns:
        for file_path in glob.glob(pattern, recursive=True):
            if "/vector_store/" in file_path.replace("\\", "/"):
                continue
            try:
                with open(file_path, "r", encoding="utf-8") as handle:
                    lines = handle.readlines()
                if len(lines) <= 3:
                    continue
                relative = str(Path(file_path).relative_to(book_path))
                documents.append(
                    Document(
                        page_content="".join(lines),
                        metadata={"source": relative},
                    )
                )
            except (UnicodeDecodeError, FileNotFoundError):
                console.print(
                    f"[yellow]Skipping unreadable file for embeddings: {file_path}[/yellow]"
                )

    return documents


def create_or_get_assistant(book_path: str) -> LangChainAssistant:
    """
    Initialize (or fetch) the LangChain-powered assistant for a project.
    """

    if not book_path:
        raise ValueError("book_path is required to create an assistant.")

    book_path = str(Path(book_path).resolve())
    if book_path in _ASSISTANT_CACHE:
        return _ASSISTANT_CACHE[book_path]

    config = load_book_config(book_path)
    if not config:
        raise RuntimeError("Unable to load project configuration.")

    behavior_path = Path(book_path) / "behaviors" / "default.txt"
    if behavior_path.exists():
        behavior_text = behavior_path.read_text(encoding="utf-8")
    else:
        behavior_text = (
            "You are the StoryCraftr creative writing assistant. "
            "Respond in markdown, keep outputs structured, and respect the requested tone."
        )

    llm_settings = llm_settings_from_config(config)
    embedding_settings = embedding_settings_from_config(config)

    llm = build_chat_model(llm_settings)
    embeddings = build_embedding_model(embedding_settings)
    vector_store = build_chroma_store(book_path, embeddings)

    assistant = LangChainAssistant(
        id=f"assistant:{Path(book_path).name}",
        book_path=book_path,
        config=config,
        llm=llm,
        vector_store=vector_store,
        behavior=behavior_text,
    )
    assistant.ensure_vector_store()

    _ASSISTANT_CACHE[book_path] = assistant
    return assistant


def get_thread(book_path: str) -> ConversationThread:
    """
    Create a new in-memory conversation thread for the project.
    """

    thread_id = f"thread:{Path(book_path).name}:{uuid4().hex}"
    thread = ConversationThread(id=thread_id, book_path=book_path)
    _THREADS[thread_id] = thread
    return thread


def _resolve_thread(thread_id: str, book_path: str) -> ConversationThread:
    thread = _THREADS.get(thread_id)
    if thread is None:
        thread = ConversationThread(
            id=thread_id or f"thread:{uuid4().hex}", book_path=book_path
        )
        _THREADS[thread.id] = thread
    return thread


def create_message(
    book_path: str,
    thread_id: str,
    content: str,
    assistant: LangChainAssistant,
    file_path: Optional[str] = None,
    progress: Optional[Progress] = None,
    task_id=None,
    force_single_answer: bool = False,
) -> str:
    """
    Generate a response from the assistant using the shared LangChain pipeline.
    """

    assistant = assistant or create_or_get_assistant(book_path)
    thread = _resolve_thread(thread_id, book_path)
    config = assistant.config

    if file_path and os.path.exists(file_path):
        file_text = Path(file_path).read_text(encoding="utf-8")
        content = f"{content}\n\nHere is the existing content to adjust:\n{file_text}"

    if config.multiple_answer and not force_single_answer:
        content = (
            "Divide the answer into three titled sections (Part 1, Part 2, Part 3). "
            "Conclude the final section with the token END_OF_RESPONSE. " + content
        )

    prompt_body = FORMAT_OUTPUT.format(
        reference_author=getattr(config, "reference_author", ""),
        language=getattr(config, "primary_language", "en"),
    )
    prompt_text = f"{prompt_body}\n\n{content}"

    prompt_with_hash = generate_prompt_with_hash(
        prompt_text,
        datetime.now().strftime("%B %d, %Y"),
        book_path=book_path,
    )

    retrieved_context = ""
    documents = []
    if assistant.retriever:
        try:
            documents = assistant.retriever.invoke({"query": content})
        except TypeError:
            documents = assistant.retriever.invoke(content)
        except AttributeError:
            documents = []

    if not documents and assistant.vector_store is not None:
        try:
            documents = assistant.vector_store.similarity_search(content, k=6)
        except Exception as exc:
            raise RuntimeError(f"Vector store similarity search failed: {exc}") from exc

    if documents:
        if not isinstance(documents, list):
            documents = [documents]
        serialized_docs = []
        for doc in documents:
            source = doc.metadata.get("source", "context")
            serialized_docs.append(f"Source: {source}\n{doc.page_content.strip()}")
        retrieved_context = "\n\n".join(serialized_docs)

    system_messages: List[SystemMessage] = [
        SystemMessage(content=assistant.system_prompt)
    ]
    if retrieved_context:
        system_messages.append(
            SystemMessage(
                content=f"Relevant project context:\n{retrieved_context}",
            )
        )

    user_message = HumanMessage(content=prompt_with_hash)
    history: Iterable[HumanMessage | AIMessage] = thread.messages

    response: AIMessage = assistant.llm.invoke(
        [*system_messages, *history, user_message]
    )

    thread.messages.extend([user_message, response])

    if progress and task_id is not None:
        try:
            progress.update(task_id, completed=1)
        except Exception as exc:
            console.print(f"[yellow]Warning: progress update failed ({exc}).[/yellow]")

    text = (
        response.content if isinstance(response.content, str) else str(response.content)
    )
    return text.replace("END_OF_RESPONSE", "").strip()


def update_agent_files(book_path: str, assistant: Optional[LangChainAssistant] = None):
    """
    Rebuild the embedded knowledge base for the assistant.
    """

    assistant = assistant or _ASSISTANT_CACHE.get(str(Path(book_path).resolve()))
    if not assistant:
        assistant = create_or_get_assistant(book_path)
    assistant.ensure_vector_store(force=True)

    # Reset active threads for this project to avoid stale context.
    stale_ids = [
        thread_id
        for thread_id, thread in _THREADS.items()
        if thread.book_path == book_path
    ]
    for thread_id in stale_ids:
        _THREADS.pop(thread_id, None)


def process_chapters(
    save_to_markdown,
    book_path: str,
    prompt_template: str,
    task_description: str,
    file_suffix: str,
    **prompt_kwargs,
):
    """
    Process chapter files by generating refinements from the assistant.
    """

    chapters_dir = os.path.join(book_path, "chapters")
    outline_dir = os.path.join(book_path, "outline")
    worldbuilding_dir = os.path.join(book_path, "worldbuilding")

    for dir_path in [chapters_dir, outline_dir, worldbuilding_dir]:
        if not os.path.exists(dir_path):
            raise FileNotFoundError(f"The directory '{dir_path}' does not exist.")

    excluded_files = {"cover.md", "back-cover.md"}
    files_to_process: List[str] = []
    for dir_path in [chapters_dir, outline_dir, worldbuilding_dir]:
        for filename in os.listdir(dir_path):
            if filename.endswith(".md") and filename not in excluded_files:
                files_to_process.append(os.path.join(dir_path, filename))

    if not files_to_process:
        raise FileNotFoundError(
            "No Markdown (.md) files were found in the chapter directory."
        )

    assistant = create_or_get_assistant(book_path)

    with Progress() as progress:
        task_chapters = progress.add_task(
            f"[cyan]{task_description}",
            total=len(files_to_process),
        )
        task_llm = progress.add_task("[green]Calling language model...", total=1)

        for chapter_file in files_to_process:
            prompt = prompt_template.format(**prompt_kwargs)
            thread = get_thread(book_path)

            progress.reset(task_llm)
            refined_text = create_message(
                book_path,
                thread_id=thread.id,
                content=prompt,
                assistant=assistant,
                progress=progress,
                task_id=task_llm,
                file_path=chapter_file,
            )

            relative_path = os.path.relpath(chapter_file, book_path)
            save_to_markdown(
                book_path,
                relative_path,
                file_suffix,
                refined_text,
                progress=progress,
                task=task_chapters,
            )
            progress.update(task_chapters, advance=1)

    update_agent_files(book_path, assistant)
