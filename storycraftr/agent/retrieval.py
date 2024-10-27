from storycraftr.agent.story.agents import create_message, get_thread
from rich.console import Console
from rich.progress import Progress

console = Console()


def summarize_content(assistant, original_prompt: str) -> str:
    """
    Summarizes the original prompt to reduce its size and complexity.

    Args:
        assistant: The assistant object to handle the interaction.
        original_prompt (str): The prompt or content to be summarized.

    Returns:
        str: The summarized content, or an empty string if summarization fails.
    """
    thread = get_thread()
    content = f"Summarize the following prompt to make it more concise:\n\nPrompt:\n{original_prompt}"

    console.print("[cyan]Summarizing the prompt...[/cyan]")

    # Send the summarization request to the assistant
    summary_response = create_message(
        book_path=None, thread_id=thread.id, content=content, assistant=assistant
    )

    if summary_response:
        console.print("[green]Summary completed successfully.[/green]")
        return summary_response
    else:
        console.print("[red]Error summarizing prompt.[/red]")
        return ""


def optimize_query_with_summary(assistant, summarized_prompt: str) -> str:
    """
    Optimizes the summarized prompt for the best response.

    Args:
        assistant: The assistant object to handle the interaction.
        summarized_prompt (str): The summarized prompt to optimize.

    Returns:
        str: The optimized content, or an empty string if optimization fails.
    """
    thread = get_thread()
    content = f"Using the following summarized prompt, optimize it for the best result:\n\nSummarized Prompt: {summarized_prompt}"

    console.print("[cyan]Optimizing the summarized prompt...[/cyan]")

    # Send the optimization request to the assistant
    optimized_response = create_message(
        book_path=None, thread_id=thread.id, content=content, assistant=assistant
    )

    if optimized_response:
        console.print("[green]Optimization completed successfully.[/green]")
        return optimized_response
    else:
        console.print("[red]Error optimizing the query.[/red]")
        return ""


def final_query(assistant, optimized_prompt: str) -> str:
    """
    Executes the final query using the optimized prompt.

    Args:
        assistant: The assistant object to handle the interaction.
        optimized_prompt (str): The optimized prompt for the final query.

    Returns:
        str: The response to the final query, or an empty string if the query fails.
    """
    thread = get_thread()
    content = f"Answer the following query:\n\nQuery: {optimized_prompt}"

    console.print("[cyan]Executing the final query...[/cyan]")

    # Send the final query to the assistant
    final_response = create_message(
        book_path=None, thread_id=thread.id, content=content, assistant=assistant
    )

    if final_response:
        console.print("[green]Final query executed successfully.[/green]")
        return final_response
    else:
        console.print("[red]Error in the final query.[/red]")
        return ""


def handle_failed_prompt(assistant, original_prompt: str) -> str:
    """
    Full process to handle a failed prompt by summarizing, optimizing, and re-executing it.

    Args:
        assistant: The assistant object to handle the interaction.
        original_prompt (str): The original prompt that needs handling.

    Returns:
        str: The final response to the processed prompt, or an empty string if the process fails.
    """
    with Progress() as progress:
        task = progress.add_task("[yellow]Processing failed prompt...", total=3)

        # Step 1: Summarize the original prompt
        console.print(
            "[bold blue]Step 1: Summarizing the original prompt...[/bold blue]"
        )
        summarized_prompt = summarize_content(assistant, original_prompt)
        progress.update(task, advance=1)

        # Step 2: Optimize the summarized prompt
        console.print(
            "[bold blue]Step 2: Optimizing the summarized prompt...[/bold blue]"
        )
        optimized_prompt = optimize_query_with_summary(assistant, summarized_prompt)
        progress.update(task, advance=1)

        # Step 3: Execute the final query
        console.print("[bold blue]Step 3: Executing the final query...[/bold blue]")
        final_response = final_query(assistant, optimized_prompt)
        progress.update(task, advance=1)

    return final_response


# Example usage
if __name__ == "__main__":
    from storycraftr.agent.story.agents import create_or_get_assistant

    # Initialize or retrieve the assistant
    assistant = create_or_get_assistant(book_path=None)

    original_prompt = "What are the key points of this content related to X?"

    # Handle the failed prompt and get the final response
    result = handle_failed_prompt(assistant, original_prompt)

    if result:
        console.print("[green]Final response received successfully![/green]")
        print(result)
    else:
        console.print("[red]Failed to process the prompt.[/red]")
