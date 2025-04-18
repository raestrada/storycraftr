"""
Agent integration for LlamaIndex with StoryCraftr.
"""
import os
from typing import List, Optional
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from storycraftr.llamaindex.core import (
    load_index,
    get_relevant_context,
    query_index
)
from storycraftr.agent.agents import create_message, get_thread, create_or_get_assistant
from storycraftr.state import debug_state
from storycraftr.utils.core import load_book_config

console = Console()


def get_context_for_agent(book_path: str, query: str, similarity_top_k: int = 5) -> List[str]:
    """
    Get relevant context for a query to enhance agent responses.
    
    Args:
        book_path (str): Path to the book project.
        query (str): Query string.
        similarity_top_k (int, optional): Number of top similar documents to retrieve.
                                         Defaults to 5.
    
    Returns:
        List[str]: List of relevant context strings.
    """
    try:
        context_list = get_relevant_context(book_path, query, similarity_top_k)
        
        if debug_state.debug:
            console.print(f"[yellow]Retrieved {len(context_list)} context items for agent.[/yellow]")
            
        return context_list
    except Exception as e:
        console.print(f"[red]Error retrieving context for agent: {e}[/red]")
        return []


def enhanced_agent_query(
    book_path: str,
    query: str,
    context_limit: int = 5,
    use_agent: bool = True
) -> str:
    """
    Enhance agent responses with context from the LlamaIndex.
    
    This function acts as a bridge between LlamaIndex and the StoryCraftr agent system.
    It retrieves relevant context and either processes it through the agent for a refined
    response or returns the raw query result.
    
    For fiction, this enhances storytelling consistency. For non-fiction, it provides 
    accurate references.
    
    Args:
        book_path (str): Path to the book project.
        query (str): Query string.
        context_limit (int, optional): Number of context items to retrieve. Defaults to 5.
        use_agent (bool, optional): Whether to use the agent for processing. Defaults to True.
        
    Returns:
        str: Response from the agent or direct query.
    """
    if not use_agent:
        # Direct query without agent processing
        return query_index(book_path, query, similarity_top_k=context_limit)
    
    try:
        # Get context for the query
        context_items = get_context_for_agent(book_path, query, context_limit)
        
        if not context_items:
            return query_index(book_path, query, similarity_top_k=context_limit)
        
        # Format context for agent
        formatted_context = "\n\n".join([
            f"Context {i+1}:\n{context}" 
            for i, context in enumerate(context_items)
        ])
        
        # Prepare agent prompt
        agent_prompt = f"""
Based on the following context from the book, please answer this question:

QUESTION: {query}

CONTEXT:
{formatted_context}

Please answer using ONLY information from the provided context, and make sure to maintain consistency with the book's content.
For fiction writing, maintain the style and tone of the story. For non-fiction, provide accurate references to the source material.
"""
        
        # Use direct query for now - in a real implementation, this would call the agent
        # This can be replaced with actual agent call once available
        response = query_index(book_path, agent_prompt, similarity_top_k=1)
        
        return response

    except Exception as e:
        console.print(f"[red]Error in enhanced agent query: {e}[/red]")
        return f"Error processing your query with agent enhancement: {e}"


def add_document_to_agent_context(
    book_path: str,
    thread_id: str,
    query: str,
    context_limit: int = 3
) -> bool:
    """
    Add relevant documents from LlamaIndex as context for an ongoing agent conversation.
    
    Args:
        book_path (str): Path to the book project.
        thread_id (str): The ID of the thread where the context will be added.
        query (str): Query to find relevant documents.
        context_limit (int, optional): Number of context items to retrieve. Defaults to 3.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Get relevant context from the index
        context_list = get_relevant_context(book_path, query, similarity_top_k=context_limit)
        
        if not context_list or context_list[0].startswith("Error") or context_list[0].startswith("Index not found"):
            if debug_state.debug:
                console.print(f"[yellow]No context found for query: {query}[/yellow]")
            return False
        
        # Format context for the agent
        formatted_context = f"""
        Additional context from your book that may be helpful:
        
        {' '.join(context_list)}
        """
        
        # Create or get the assistant
        assistant = create_or_get_assistant(book_path)
        
        # Add the context as a message
        create_message(
            book_path=book_path,
            thread_id=thread_id,
            content=formatted_context,
            assistant=assistant,
            role="user"
        )
        
        return True
        
    except Exception as e:
        console.print(f"[red]Error adding document to agent context: {e}[/red]")
        return False 