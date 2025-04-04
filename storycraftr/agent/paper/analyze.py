import os
from pathlib import Path
from rich.console import Console
from storycraftr.utils.core import load_book_config
from storycraftr.agent.agents import (
    create_or_get_assistant,
    get_thread,
    create_message,
    update_agent_files,
)
from storycraftr.utils.markdown import save_to_markdown
from storycraftr.prompts.paper.analyze import (
    RUN_ANALYSIS_PROMPT_NEW,
    RUN_ANALYSIS_PROMPT_REFINE,
    SUMMARIZE_RESULTS_PROMPT_NEW,
    SUMMARIZE_RESULTS_PROMPT_REFINE,
)

console = Console()

def run_data_analysis(book_path: str, prompt: str) -> str:
    """
    Generate or refine a data analysis plan.

    Args:
        book_path (str): Path to the paper's directory.
        prompt (str): The prompt to guide the analysis plan generation.

    Returns:
        str: The generated or refined analysis plan.
    """
    console.print("[bold blue]Generating data analysis plan...[/bold blue]")

    # Load configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "sections", "analysis_plan.md")
    paper_title = config.book_name

    # Check if analysis plan exists and choose appropriate prompt
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        console.print("[yellow]Refining existing analysis plan...[/yellow]")
        content = RUN_ANALYSIS_PROMPT_REFINE.format(
            prompt=prompt,
            paper_title=paper_title
        )
    else:
        console.print("[yellow]Generating new analysis plan...[/yellow]")
        content = RUN_ANALYSIS_PROMPT_NEW.format(
            prompt=prompt,
            paper_title=paper_title
        )

    # Generate analysis plan using the assistant
    analysis_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path
    )

    # Save the result
    save_to_markdown(
        book_path,
        "sections/analysis_plan.md",
        "Data Analysis Plan",
        analysis_content
    )
    console.print("[bold green]✔ Data analysis plan generated successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return analysis_content

def summarize_analysis_results(book_path: str, prompt: str) -> str:
    """
    Generate or refine a summary of analysis results.

    Args:
        book_path (str): Path to the paper's directory.
        prompt (str): The prompt to guide the results summary generation.

    Returns:
        str: The generated or refined results summary.
    """
    console.print("[bold blue]Generating results summary...[/bold blue]")

    # Load configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "sections", "results.md")
    paper_title = config.book_name

    # Check if results summary exists and choose appropriate prompt
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        console.print("[yellow]Refining existing results summary...[/yellow]")
        content = SUMMARIZE_RESULTS_PROMPT_REFINE.format(
            prompt=prompt,
            paper_title=paper_title
        )
    else:
        console.print("[yellow]Generating new results summary...[/yellow]")
        content = SUMMARIZE_RESULTS_PROMPT_NEW.format(
            prompt=prompt,
            paper_title=paper_title
        )

    # Generate results summary using the assistant
    results_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path
    )

    # Save the result
    save_to_markdown(
        book_path,
        "sections/results.md",
        "Results",
        results_content
    )
    console.print("[bold green]✔ Results summary generated successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return results_content 