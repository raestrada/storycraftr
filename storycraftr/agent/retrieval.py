from rich.console import Console

from storycraftr.agent.agents import create_message

console = Console()


def summarize_content(book_path: str, original_prompt: str) -> str:
    """
    Summarizes the original prompt to reduce its size and complexity.
    """
    console.print("[bold blue]Summarizing content...[/bold blue]")
    prompt = f"Summarize the following content:\n\n{original_prompt}"
    summary = create_message(book_path, content=prompt, history=[])
    return summary


def optimize_query_with_summary(book_path: str, summarized_prompt: str) -> str:
    """
    Optimizes the summarized prompt for the best response.
    """
    console.print("[bold blue]Optimizing query...[/bold blue]")
    prompt = f"Optimize the following query for a large language model, based on the provided summary:\n\n{summarized_prompt}"
    optimized_query = create_message(book_path, content=prompt, history=[])
    return optimized_query


def final_query(book_path: str, optimized_prompt: str) -> str:
    """
    Executes the final query using the optimized prompt.
    """
    console.print("[bold blue]Executing final query...[/bold blue]")
    response = create_message(book_path, content=optimized_prompt, history=[])
    return response


def handle_failed_prompt(book_path: str, original_prompt: str) -> str:
    """
    Full process to handle a failed prompt by summarizing, optimizing, and re-executing it.
    """
    console.print(
        "[bold red]Original prompt failed. Starting recovery process...[/bold red]"
    )
    summarized_prompt = summarize_content(book_path, original_prompt)
    optimized_prompt = optimize_query_with_summary(book_path, summarized_prompt)
    final_response = final_query(book_path, optimized_prompt)
    return final_response
