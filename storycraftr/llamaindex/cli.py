"""
CLI commands for LlamaIndex integration.
"""
import os
import json
import click
from pathlib import Path
from typing import List, Dict, Optional

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table

from storycraftr.llamaindex.core import (
    build_index,
    load_index,
    query_index,
    get_relevant_context,
    get_raw_context, 
    load_knowledge_source,
    build_index_with_knowledge
)
from storycraftr.llamaindex.agent_integration import enhanced_agent_query
from storycraftr.state import debug_state

console = Console()


@click.group()
def llamaindex():
    """
    LlamaIndex commands for semantic search and retrieval.
    """
    pass


@llamaindex.command("build-index")
@click.option(
    "--book-path", 
    type=click.Path(exists=True), 
    help="Path to the book directory", 
    required=False
)
@click.option(
    "--directories",
    "-d",
    multiple=True,
    help="Directories to include in the index (multiple allowed)",
)
def build_index_command(book_path, directories):
    """
    Build a semantic index from book content.
    """
    from storycraftr.cli import verify_book_path
    
    book_path = verify_book_path(book_path)
    
    dir_list = list(directories) if directories else None
    
    result = build_index(book_path, dir_list)
    
    if result:
        console.print("[green]✓ Index built successfully![/green]")
    else:
        console.print("[red]✖ Failed to build index.[/red]")


@llamaindex.command("query")
@click.option(
    "--book-path", 
    type=click.Path(exists=True), 
    help="Path to the book directory", 
    required=False
)
@click.argument("query")
@click.option(
    "--limit", 
    "-k", 
    default=5, 
    help="Number of results to return", 
    type=int
)
@click.option(
    "--raw", 
    is_flag=True, 
    help="Return raw results without agent processing"
)
def query_command(book_path, query, limit, raw):
    """
    Query the semantic index.
    """
    from storycraftr.cli import verify_book_path
    
    book_path = verify_book_path(book_path)
    
    if raw:
        # Use direct index query without agent processing
        result = query_index(book_path, query, similarity_top_k=limit)
    else:
        # Use enhanced query with agent processing
        result = enhanced_agent_query(
            book_path=book_path,
            query=query,
            context_limit=limit,
            use_agent=True
        )
    
    # Format and display the result
    console.print("\n")
    console.print(Panel(
        Markdown(result),
        title="[bold blue]Query Result[/bold blue]",
        border_style="blue"
    ))


@llamaindex.command("context")
@click.option(
    "--book-path", 
    type=click.Path(exists=True), 
    help="Path to the book directory", 
    required=False
)
@click.argument("query")
@click.option(
    "--limit", 
    "-k", 
    default=5, 
    help="Number of context items to return", 
    type=int
)
def context_command(book_path, query, limit):
    """
    Get raw context from the semantic index.
    """
    from storycraftr.cli import verify_book_path
    
    book_path = verify_book_path(book_path)
    
    context_list = get_relevant_context(book_path, query, similarity_top_k=limit)
    
    if not context_list or context_list[0].startswith("Error") or context_list[0].startswith("Index not found"):
        console.print(f"[red]{context_list[0] if context_list else 'No context found for the query.'}")
        return
    
    console.print("\n[bold blue]Relevant Context:[/bold blue]\n")
    
    for i, context in enumerate(context_list, 1):
        console.print(Panel(
            Markdown(context),
            title=f"[bold blue]Context {i}/{len(context_list)}[/bold blue]",
            border_style="blue"
        ))
        console.print("\n")


@llamaindex.command("build-knowledge-index")
@click.argument('book_path', type=str)
@click.option('--knowledge', '-k', type=str, multiple=True, help="Path to knowledge source (file or directory)")
@click.option('--knowledge-type', '-kt', type=str, multiple=True, help="Type of knowledge (research, worldbuilding, etc.)")
@click.option('--directories', '-d', type=str, multiple=True, help="Book directories to include in index")
def build_knowledge_index_command(book_path: str, knowledge: tuple, knowledge_type: tuple, directories: tuple):
    """
    Build an index with external knowledge sources for enhanced storytelling.
    
    This command builds a semantic index combining your book content with external knowledge sources.
    Use this for both fiction (worldbuilding, character guides) and non-fiction (research, citations) storytelling.
    
    Examples:
    \b
    # Build an index with a research paper for non-fiction:
    storycraftr llama build-knowledge-index ./my_book --knowledge ./research/paper.pdf --knowledge-type research
    
    \b
    # Build an index with worldbuilding and character guides for fiction:
    storycraftr llama build-knowledge-index ./my_book --knowledge ./lore/world.md --knowledge-type worldbuilding --knowledge ./lore/characters.json --knowledge-type character
    """
    try:
        from storycraftr.cli import verify_book_path
        
        book_path = verify_book_path(book_path)
        
        # Process knowledge sources with types
        knowledge_sources = []
        for i, path in enumerate(knowledge):
            # Default to "research" if not enough types provided
            k_type = knowledge_type[i] if i < len(knowledge_type) else "research"
            knowledge_sources.append({
                "path": path,
                "type": k_type
            })
            
        # Convert directories to list
        dir_list = list(directories) if directories else None
        
        # Show info about what we're indexing
        console.print(f"[bold blue]Building enhanced knowledge index for book at:[/bold blue] {book_path}")
        
        if dir_list:
            console.print(f"[bold blue]Including book directories:[/bold blue] {', '.join(dir_list)}")
        
        if knowledge_sources:
            console.print(f"[bold blue]Including knowledge sources:[/bold blue]")
            knowledge_table = Table(show_header=True, header_style="bold magenta")
            knowledge_table.add_column("Path")
            knowledge_table.add_column("Type")
            
            for source in knowledge_sources:
                knowledge_table.add_row(source["path"], source["type"])
                
            console.print(knowledge_table)
        
        # Build the index
        index = build_index_with_knowledge(
            book_path=book_path,
            directories=dir_list,
            knowledge_sources=knowledge_sources
        )
        
        if index:
            console.print("[bold green]Enhanced knowledge index built successfully![/bold green]")
            console.print(f"[green]You can now query your book and knowledge sources using 'storycraftr llama query {book_path} \"your question\"'[/green]")
        else:
            console.print("[bold red]Failed to build enhanced knowledge index.[/bold red]")
            
    except Exception as e:
        console.print(f"[bold red]Error building enhanced knowledge index:[/bold red] {e}")


# Register these commands with the main CLI
def register_llamaindex_commands(cli):
    """
    Register LlamaIndex commands with the main CLI.
    """
    cli.add_command(llamaindex) 