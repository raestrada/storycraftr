"""
Integration of LlamaIndex with the chat interface.
"""
import re
from typing import Dict, Any, List, Optional, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from storycraftr.llamaindex.core import (
    build_index,
    query_index,
    get_relevant_context,
    build_index_with_knowledge,
    load_knowledge_source
)
from storycraftr.llamaindex.agent_integration import (
    enhanced_agent_query,
    add_document_to_agent_context
)
from storycraftr.state import debug_state

console = Console()


def register_chat_commands(chat_commands: Dict[str, Any]) -> Dict[str, Any]:
    """
    Register LlamaIndex commands with the chat interface.
    
    Args:
        chat_commands (Dict[str, Any]): The existing chat commands dictionary.
        
    Returns:
        Dict[str, Any]: The updated chat commands dictionary.
    """
    # Add LlamaIndex commands to the chat command list
    chat_commands["llamaindex"] = {
        "build": build_index_chat,
        "query": query_index_chat,
        "context": context_chat,
        "help": llamaindex_help,
        "knowledge": handle_knowledge_command
    }
    
    return chat_commands


def llamaindex_help(args: List[str], book_path: str, thread_id: str, **kwargs) -> str:
    """
    Display help information for LlamaIndex commands.
    
    Args:
        args (List[str]): Command arguments.
        book_path (str): Path to the book directory.
        thread_id (str): ID of the current thread.
        
    Returns:
        str: Help message for LlamaIndex commands.
    """
    help_text = """
# LlamaIndex Commands

LlamaIndex provides semantic search capabilities for your book content.

## Available Commands:

### !llamaindex build
Build a semantic index from your book content.
Example: `!llamaindex build`

### !llamaindex query [query]
Query the semantic index with AI-powered response generation.
Example: `!llamaindex query What are the main characters in my story?`

### !llamaindex context [query]
Get raw context from the semantic index without processing.
Example: `!llamaindex context Tell me about the protagonist's backstory`

### !llamaindex knowledge add <path> [--type <type>]
Add external knowledge source to the index.
Example: `!llamaindex knowledge add /path/to/knowledge --type research`

### !llamaindex knowledge list
List all added knowledge sources.

### !llamaindex knowledge build
Build index with knowledge sources.

### !llamaindex knowledge query <query>
Query with knowledge-enhanced index.

### !llamaindex help
Display this help message.
"""
    
    console.print(Markdown(help_text))
    return "LlamaIndex help displayed above."


def build_index_chat(args: List[str], book_path: str, thread_id: str, **kwargs) -> str:
    """
    Build a semantic index from book content via chat.
    
    Args:
        args (List[str]): Command arguments.
        book_path (str): Path to the book directory.
        thread_id (str): ID of the current thread.
        
    Returns:
        str: Result message.
    """
    console.print("[bold blue]Building index...[/bold blue]")
    
    result = build_index(book_path)
    
    if result:
        return "✅ Index built successfully! You can now use `!llamaindex query` to search your book content."
    else:
        return "❌ Failed to build index. Make sure your book has content to index."


def query_index_chat(args: List[str], book_path: str, thread_id: str, **kwargs) -> str:
    """
    Query the semantic index via chat.
    
    Args:
        args (List[str]): Command arguments.
        book_path (str): Path to the book directory.
        thread_id (str): ID of the current thread.
        
    Returns:
        str: Query result.
    """
    if not args:
        return "❌ Please provide a query. Example: `!llamaindex query What are the main themes of my story?`"
    
    query = " ".join(args)
    
    console.print(f"[bold blue]Querying index for: [/bold blue]{query}")
    
    # Get response from enhanced agent query
    response = enhanced_agent_query(
        book_path=book_path,
        query=query,
        context_limit=5,
        use_agent=True
    )
    
    # Add the context to the thread for agent awareness
    add_document_to_agent_context(book_path, thread_id, query)
    
    return response


def context_chat(args: List[str], book_path: str, thread_id: str, **kwargs) -> str:
    """
    Get raw context from the semantic index via chat.
    
    Args:
        args (List[str]): Command arguments.
        book_path (str): Path to the book directory.
        thread_id (str): ID of the current thread.
        
    Returns:
        str: Raw context result.
    """
    if not args:
        return "❌ Please provide a query. Example: `!llamaindex context What are the main themes of my story?`"
    
    query = " ".join(args)
    
    console.print(f"[bold blue]Retrieving context for: [/bold blue]{query}")
    
    # Get raw context
    context_list = get_relevant_context(book_path, query, similarity_top_k=3)
    
    if not context_list or context_list[0].startswith("Error") or context_list[0].startswith("Index not found"):
        return f"❌ {context_list[0] if context_list else 'No context found for the query.'}"
    
    # Format context as markdown
    result = "## Retrieved Context\n\n"
    for i, context in enumerate(context_list, 1):
        result += f"### Context {i}/{len(context_list)}\n\n{context}\n\n---\n\n"
    
    return result


def handle_knowledge_command(args: List[str], book_path: str, chat_state: Dict[str, Any]) -> str:
    """
    Handle the !llamaindex knowledge command from the chat interface.
    
    This command allows loading external knowledge sources and querying with them.
    Usage patterns:
        !llamaindex knowledge add <path> [--type <type>]  # Add knowledge source
        !llamaindex knowledge list                       # List loaded knowledge sources
        !llamaindex knowledge query <query>              # Query with knowledge sources
        !llamaindex knowledge build                      # Build index with knowledge sources
    
    Args:
        args (List[str]): Command arguments.
        book_path (str): Path to the book.
        chat_state (Dict[str, Any]): Chat state dictionary.
    
    Returns:
        str: Response message.
    """
    if len(args) < 1:
        return "⚠️ Missing subcommand. Use: add, list, query, or build"
    
    # Initialize knowledge sources in chat state if not present
    if "knowledge_sources" not in chat_state:
        chat_state["knowledge_sources"] = []
    
    subcommand = args[0].lower()
    
    # Handle add knowledge source
    if subcommand == "add":
        if len(args) < 2:
            return "⚠️ Missing path to knowledge source"
        
        path = args[1]
        k_type = "research"  # Default type
        
        # Check for --type flag
        for i, arg in enumerate(args):
            if arg == "--type" and i + 1 < len(args):
                k_type = args[i + 1]
        
        # Add to state
        chat_state["knowledge_sources"].append({
            "path": path,
            "type": k_type
        })
        
        return f"✅ Added knowledge source: {path} (type: {k_type})"
    
    # Handle list knowledge sources
    elif subcommand == "list":
        if not chat_state["knowledge_sources"]:
            return "No knowledge sources loaded yet. Add some with: !llamaindex knowledge add <path>"
        
        response = "📚 **Knowledge Sources:**\n\n"
        for i, source in enumerate(chat_state["knowledge_sources"], 1):
            response += f"{i}. **{source['path']}** (type: {source['type']})\n"
        
        return response
    
    # Handle build index with knowledge
    elif subcommand == "build":
        if not chat_state["knowledge_sources"]:
            return "⚠️ No knowledge sources added. Add some first with: !llamaindex knowledge add <path>"
        
        console.print("[bold blue]Building enhanced knowledge index...[/bold blue]")
        
        try:
            # Check for directory specification
            directories = None
            for i, arg in enumerate(args):
                if arg == "--dir" and i + 1 < len(args):
                    directories = args[i+1].split(",")
            
            # Build index with knowledge sources
            index = build_index_with_knowledge(
                book_path=book_path,
                directories=directories,
                knowledge_sources=chat_state["knowledge_sources"]
            )
            
            if index:
                return "✅ Successfully built knowledge-enhanced index! You can now query it with: !llamaindex knowledge query <your question>"
            else:
                return "❌ Failed to build knowledge-enhanced index."
        
        except Exception as e:
            return f"❌ Error building knowledge index: {str(e)}"
    
    # Handle query with knowledge
    elif subcommand == "query":
        if len(args) < 2:
            return "⚠️ Missing query. Usage: !llamaindex knowledge query <your question>"
        
        # Join remaining args for query
        query = " ".join(args[1:])
        console.print(f"[bold blue]Querying knowledge index: [/bold blue] {query}")
        
        # For knowledge queries, we use the enhanced agent query for better results
        result = enhanced_agent_query(
            book_path=book_path,
            query=query,
            context_limit=5,
            use_agent=True
        )
        
        return result
    
    else:
        return f"⚠️ Unknown subcommand: {subcommand}. Use: add, list, query, or build"


def handle_llamaindex_command(command: str, book_path: str, chat_state: Dict[str, Any]) -> str:
    """
    Handle LlamaIndex commands from the chat interface.
    
    Args:
        command (str): The command string (without the !llamaindex prefix).
        book_path (str): Path to the book.
        chat_state (Dict[str, Any]): Chat state dictionary.
        
    Returns:
        str: Response message.
    """
    command = command.strip()
    
    # Parse command and args
    parts = command.split()
    if not parts:
        return show_llamaindex_help()
    
    cmd = parts[0].lower()
    args = parts[1:]
    
    # Handle commands
    if cmd == "build" or cmd == "build-index":
        return handle_build_command(args, book_path)
    
    elif cmd == "query":
        return handle_query_command(args, book_path)
    
    elif cmd == "context":
        return handle_context_command(args, book_path)
    
    elif cmd == "knowledge":
        return handle_knowledge_command(args, book_path, chat_state)
    
    elif cmd == "help":
        return show_llamaindex_help()
    
    else:
        return f"Unknown LlamaIndex command: {cmd}. Type '!llamaindex help' for available commands."


def show_llamaindex_help() -> str:
    """Show help for LlamaIndex commands."""
    help_text = """
## LlamaIndex Commands

- **!llamaindex build** - Build a semantic index for your book
- **!llamaindex query <query>** - Query your book content
- **!llamaindex context <query>** - Get raw context for a query
- **!llamaindex knowledge add <path> [--type <type>]** - Add external knowledge source
- **!llamaindex knowledge list** - List added knowledge sources
- **!llamaindex knowledge build** - Build index with knowledge sources
- **!llamaindex knowledge query <query>** - Query with knowledge-enhanced index
- **!llamaindex help** - Show this help message
"""
    return help_text 