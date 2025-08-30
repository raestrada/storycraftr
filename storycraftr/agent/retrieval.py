from rich.console import Console
from openai import APIError

from storycraftr.agent.agents import create_message

console = Console()


def summarize_content(book_path: str, original_prompt: str) -> str:
    """
    Summarizes the original prompt to reduce its size and complexity.

    Args:
        book_path (str): The path to the book's directory.
        original_prompt (str): The original content to summarize.

    Returns:
        str: The summarized content, or an empty string if an error occurs.
    """
    console.print("[bold blue]Summarizing content...[/bold blue]")
    prompt = f"Summarize the following content:\n\n{original_prompt}"
    try:
        summary = create_message(book_path, content=prompt, history=[])
        return summary
    except APIError as e:
        console.print(f"[bold red]API Error during summarization: {e}[/bold red]")
        return ""


def optimize_query_with_summary(book_path: str, summarized_prompt: str) -> str:
    """
    Optimizes the summarized prompt for the best response.

    Args:
        book_path (str): The path to the book's directory.
        summarized_prompt (str): The summarized prompt to optimize.

    Returns:
        str: The optimized query, or an empty string if an error occurs.
    """
    console.print("[bold blue]Optimizing query...[/bold blue]")
    prompt = f"Optimize the following query for a large language model, based on the provided summary:\n\n{summarized_prompt}"
    try:
        optimized_query = create_message(book_path, content=prompt, history=[])
        return optimized_query
    except APIError as e:
        console.print(f"[bold red]API Error during query optimization: {e}[/bold red]")
        return ""


def final_query(book_path: str, optimized_prompt: str) -> str:
    """
    Executes the final query using the optimized prompt.

    Args:
        book_path (str): The path to the book's directory.
        optimized_prompt (str): The optimized prompt to execute.

    Returns:
        str: The response from the model, or an empty string if an error occurs.
    """
    console.print("[bold blue]Executing final query...[/bold blue]")
    try:
        response = create_message(book_path, content=optimized_prompt, history=[])
        return response
    except APIError as e:
        console.print(
            f"[bold red]API Error during final query execution: {e}[/bold red]"
        )
        return ""


def handle_failed_prompt(book_path: str, original_prompt: str) -> str:
    """
    Full process to handle a failed prompt by summarizing, optimizing, and re-executing it.
    This provides a single-shot recovery attempt.

    Args:
        book_path (str): The path to the book's directory.
        original_prompt (str): The original prompt that failed.

    Returns:
        str: The final response after recovery, or an empty string if recovery fails.
    """
    console.print(
        "[bold red]Original prompt failed. Starting recovery process...[/bold red]"
    )
    summarized_prompt = summarize_content(book_path, original_prompt)
    if not summarized_prompt:
        console.print(
            "[bold red]Recovery failed: Could not summarize content.[/bold red]"
        )
        return ""

    optimized_prompt = optimize_query_with_summary(book_path, summarized_prompt)
    if not optimized_prompt:
        console.print("[bold red]Recovery failed: Could not optimize query.[/bold red]")
        return ""
    final_response = final_query(book_path, optimized_prompt)
    return final_response
