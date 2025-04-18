"""
Core functionality for LlamaIndex integration with StoryCraftr.
"""
import os
from pathlib import Path
import json
from typing import Dict, List, Optional, Union

from llama_index.core import Settings, StorageContext
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from storycraftr.state import debug_state
from storycraftr.utils.core import load_book_config

console = Console()


def configure_llama_index(book_path: str, openai_model: Optional[str] = None, openai_url: Optional[str] = None) -> None:
    """
    Configure LlamaIndex settings using StoryCraftr configuration.
    
    Args:
        book_path (str): Path to the book project.
        openai_model (str, optional): OpenAI model to use.
        openai_url (str, optional): URL for the OpenAI API.
    """
    config = load_book_config(book_path)
    
    model = openai_model or config.openai_model
    api_url = openai_url or config.openai_url
    
    llm = OpenAI(
        model=model,
        api_base=api_url,
        api_key=os.environ.get("OPENAI_API_KEY", ""),
    )
    
    embed_model = OpenAIEmbedding(
        api_base=api_url,
        api_key=os.environ.get("OPENAI_API_KEY", ""),
    )
    
    Settings.llm = llm
    Settings.embed_model = embed_model
    Settings.chunk_size = 512
    Settings.chunk_overlap = 20
    
    if debug_state.debug:
        console.print(f"[yellow]LlamaIndex configured with model: {model}[/yellow]")


def get_index_path(book_path: str) -> Path:
    """
    Get the path where the index will be stored.
    
    Args:
        book_path (str): Path to the book project.
        
    Returns:
        Path: The path to the index directory.
    """
    return Path(book_path) / "indexes" / "llamaindex"


def build_index(book_path: str, directories: List[str] = None) -> VectorStoreIndex:
    """
    Build a Vector Store Index for the book.
    
    Args:
        book_path (str): Path to the book project.
        directories (List[str], optional): Specific directories to index. 
                                          Defaults to standard book directories.
    
    Returns:
        VectorStoreIndex: The created index.
    """
    configure_llama_index(book_path)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[bold blue]Building index...", total=None)
        
        if not directories:
            # Default directories to index
            directories = [
                "worldbuilding",
                "outline",
                "chapters",
                "reference"
            ]
        
        all_documents = []
        
        for directory in directories:
            dir_path = Path(book_path) / directory
            if dir_path.exists():
                try:
                    documents = SimpleDirectoryReader(
                        input_dir=str(dir_path),
                        recursive=True,
                        file_extractor={
                            ".md": lambda x: x,
                            ".txt": lambda x: x,
                            ".json": lambda x: x
                        }
                    ).load_data()
                    
                    all_documents.extend(documents)
                    
                    if debug_state.debug:
                        console.print(f"[green]Loaded {len(documents)} documents from {directory}[/green]")
                except Exception as e:
                    console.print(f"[red]Error loading documents from {directory}: {e}[/red]")
        
        if not all_documents:
            progress.stop()
            console.print("[red]No documents found to index.[/red]")
            return None
        
        # Create the index directory if it doesn't exist
        index_path = get_index_path(book_path)
        index_path.mkdir(parents=True, exist_ok=True)
        
        # Create storage context
        storage_context = StorageContext.from_defaults(persist_dir=str(index_path))
        
        # Create the index with the loaded documents
        parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
        nodes = parser.get_nodes_from_documents(all_documents)
        
        index = VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
        )
        
        # Persist the index
        index.storage_context.persist()
        
        progress.update(task, completed=True)
        console.print(f"[green]Index built successfully with {len(all_documents)} documents![/green]")
        
        return index


def load_index(book_path: str) -> Optional[VectorStoreIndex]:
    """
    Load an existing LlamaIndex from disk.
    
    Args:
        book_path (str): Path to the book project.
        
    Returns:
        Optional[VectorStoreIndex]: The loaded index, or None if it doesn't exist.
    """
    configure_llama_index(book_path)
    
    index_path = get_index_path(book_path)
    
    if not index_path.exists():
        console.print("[yellow]Index does not exist. Run 'build-index' first.[/yellow]")
        return None
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[bold blue]Loading index...", total=None)
            
            storage_context = StorageContext.from_defaults(persist_dir=str(index_path))
            index = VectorStoreIndex.from_storage(storage_context)
            
            progress.update(task, completed=True)
            
        console.print("[green]Index loaded successfully![/green]")
        return index
    except Exception as e:
        console.print(f"[red]Error loading index: {e}[/red]")
        return None


def query_index(book_path: str, query: str, similarity_top_k: int = 5) -> str:
    """
    Query the LlamaIndex for relevant information.
    
    Args:
        book_path (str): Path to the book project.
        query (str): Query string.
        similarity_top_k (int, optional): Number of top similar documents to retrieve. 
                                         Defaults to 5.
    
    Returns:
        str: Response from the index query.
    """
    index = load_index(book_path)
    
    if not index:
        return "Index not found. Please build the index first using the build-index command."
    
    try:
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=similarity_top_k,
        )
        
        query_engine = RetrieverQueryEngine.from_args(
            retriever=retriever,
        )
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[bold blue]Querying index...", total=None)
            response = query_engine.query(query)
            progress.update(task, completed=True)
        
        if debug_state.debug:
            console.print(f"[yellow]Query response: {response}[/yellow]")
            
        return str(response)
    except Exception as e:
        console.print(f"[red]Error querying index: {e}[/red]")
        return f"Error querying index: {e}"


def get_relevant_context(book_path: str, query: str, similarity_top_k: int = 5) -> List[str]:
    """
    Get relevant context for a query without processing it into a response.
    
    Args:
        book_path (str): Path to the book project.
        query (str): Query string.
        similarity_top_k (int, optional): Number of top similar documents to retrieve.
                                         Defaults to 5.
    
    Returns:
        List[str]: List of relevant context strings.
    """
    index = load_index(book_path)
    
    if not index:
        return ["Index not found. Please build the index first using the build-index command."]
    
    try:
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=similarity_top_k,
        )
        
        nodes = retriever.retrieve(query)
        
        context_list = [node.get_content() for node in nodes]
        
        if debug_state.debug:
            console.print(f"[yellow]Retrieved {len(context_list)} relevant contexts[/yellow]")
            
        return context_list
    except Exception as e:
        console.print(f"[red]Error retrieving context: {e}[/red]")
        return [f"Error retrieving context: {e}"]


def load_knowledge_source(
    book_path: str, 
    knowledge_path: str, 
    knowledge_type: str = "research", 
    metadata: Optional[Dict] = None
) -> List[Document]:
    """
    Load external knowledge sources to enhance storytelling with references.
    
    This function allows loading additional knowledge beyond the book's content,
    which can be used for both fiction (worldbuilding, character guides) and
    non-fiction (research materials, citations) storytelling.
    
    Args:
        book_path (str): Path to the book project.
        knowledge_path (str): Path to knowledge source directory or file.
        knowledge_type (str, optional): Type of knowledge ('research', 'worldbuilding', 
                                        'character', 'plot', 'setting', etc.). 
                                        Defaults to "research".
        metadata (Dict, optional): Additional metadata for the documents. Defaults to None.
    
    Returns:
        List[Document]: List of loaded documents.
    """
    if not metadata:
        metadata = {}
    
    # Ensure knowledge_type is in metadata
    metadata["knowledge_type"] = knowledge_type
    
    knowledge_path = Path(knowledge_path)
    documents = []
    
    if not knowledge_path.exists():
        console.print(f"[red]Knowledge source path does not exist: {knowledge_path}[/red]")
        return documents
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"[bold blue]Loading {knowledge_type} knowledge...", total=None)
            
            # Handle either a file or directory
            if knowledge_path.is_file():
                # Determine file type and load appropriately
                file_ext = knowledge_path.suffix.lower()
                
                if file_ext in ['.txt', '.md', '.markdown']:
                    with open(knowledge_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        doc = Document(
                            text=content,
                            metadata={
                                **metadata,
                                "source": str(knowledge_path),
                                "filename": knowledge_path.name
                            }
                        )
                        documents.append(doc)
                
                elif file_ext in ['.json']:
                    with open(knowledge_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)
                        # Handle different JSON formats
                        if isinstance(json_data, list):
                            for i, item in enumerate(json_data):
                                content = json.dumps(item, ensure_ascii=False, indent=2)
                                doc = Document(
                                    text=content,
                                    metadata={
                                        **metadata,
                                        "source": str(knowledge_path),
                                        "filename": knowledge_path.name,
                                        "index": i
                                    }
                                )
                                documents.append(doc)
                        else:
                            content = json.dumps(json_data, ensure_ascii=False, indent=2)
                            doc = Document(
                                text=content,
                                metadata={
                                    **metadata,
                                    "source": str(knowledge_path),
                                    "filename": knowledge_path.name
                                }
                            )
                            documents.append(doc)
                
                else:
                    console.print(f"[yellow]Unsupported file type: {file_ext}[/yellow]")
            
            elif knowledge_path.is_dir():
                # Load all supported files from directory
                file_extractor = {
                    ".md": lambda x: x,
                    ".txt": lambda x: x,
                    ".json": lambda x: x
                }
                
                reader = SimpleDirectoryReader(
                    input_dir=str(knowledge_path),
                    recursive=True,
                    file_extractor=file_extractor
                )
                
                loaded_docs = reader.load_data()
                
                # Add metadata to each document
                for doc in loaded_docs:
                    # Update metadata without removing existing
                    doc.metadata.update(metadata)
                    documents.append(doc)
            
            progress.update(task, completed=True)
            
            console.print(f"[green]Loaded {len(documents)} documents from knowledge source![/green]")
    
    except Exception as e:
        console.print(f"[red]Error loading knowledge source: {e}[/red]")
    
    return documents


def build_index_with_knowledge(
    book_path: str, 
    directories: List[str] = None,
    knowledge_sources: List[Dict] = None
) -> VectorStoreIndex:
    """
    Build a Vector Store Index for the book with additional knowledge sources.
    
    Args:
        book_path (str): Path to the book project.
        directories (List[str], optional): Specific directories to index. 
                                          Defaults to standard book directories.
        knowledge_sources (List[Dict], optional): List of knowledge source configurations.
                                                 Each dict should contain 'path', 'type',
                                                 and optional 'metadata' keys.
    
    Returns:
        VectorStoreIndex: The created index.
    """
    configure_llama_index(book_path)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[bold blue]Building enhanced knowledge index...", total=None)
        
        if not directories:
            # Default directories to index
            directories = [
                "worldbuilding",
                "outline",
                "chapters",
                "reference"
            ]
        
        all_documents = []
        
        # Load book content
        for directory in directories:
            dir_path = Path(book_path) / directory
            if dir_path.exists():
                try:
                    documents = SimpleDirectoryReader(
                        input_dir=str(dir_path),
                        recursive=True,
                        file_extractor={
                            ".md": lambda x: x,
                            ".txt": lambda x: x,
                            ".json": lambda x: x
                        }
                    ).load_data()
                    
                    # Add metadata about source
                    for doc in documents:
                        doc.metadata["source_type"] = "book_content"
                        doc.metadata["content_directory"] = directory
                    
                    all_documents.extend(documents)
                    
                    if debug_state.debug:
                        console.print(f"[green]Loaded {len(documents)} documents from {directory}[/green]")
                except Exception as e:
                    console.print(f"[red]Error loading documents from {directory}: {e}[/red]")
        
        # Load additional knowledge sources if provided
        if knowledge_sources:
            for source in knowledge_sources:
                path = source.get("path")
                k_type = source.get("type", "research")
                metadata = source.get("metadata", {})
                
                if path:
                    knowledge_docs = load_knowledge_source(
                        book_path=book_path,
                        knowledge_path=path,
                        knowledge_type=k_type,
                        metadata=metadata
                    )
                    all_documents.extend(knowledge_docs)
        
        if not all_documents:
            progress.stop()
            console.print("[red]No documents found to index.[/red]")
            return None
        
        # Create the index directory if it doesn't exist
        index_path = get_index_path(book_path)
        index_path.mkdir(parents=True, exist_ok=True)
        
        # Create storage context
        storage_context = StorageContext.from_defaults(persist_dir=str(index_path))
        
        # Create the index with the loaded documents
        parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
        nodes = parser.get_nodes_from_documents(all_documents)
        
        index = VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
        )
        
        # Persist the index
        index.storage_context.persist()
        
        progress.update(task, completed=True)
        console.print(f"[green]Enhanced knowledge index built successfully with {len(all_documents)} documents![/green]")
        
        return index 