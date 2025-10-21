import os
from pathlib import Path
from rich.console import Console
from storycraftr.utils.core import load_book_config
from storycraftr.agent.agents import create_message
from storycraftr.utils.markdown import save_to_markdown
from storycraftr.prompts.paper.iterate import (
    REINFORCE_IDEAS_PROMPT,
    IMPROVE_CLARITY_PROMPT,
)

console = Console()


def reinforce_ideas(book_path: str, prompt: str) -> str:
    """
    Strengthen core ideas and arguments throughout the paper.
    """
    console.print("[bold blue]Reinforcing ideas throughout the paper...[/bold blue]")

    config = load_book_config(book_path)
    paper_title = config.book_name

    content = REINFORCE_IDEAS_PROMPT.format(prompt=prompt, paper_title=paper_title)

    improvements = create_message(book_path, content=content, history=[])

    save_to_markdown(
        book_path, "reviews/improvements.md", "Suggested Improvements", improvements
    )

    console.print("[bold green]✔ Ideas reinforced successfully[/bold green]")
    return improvements


def improve_clarity(book_path: str, prompt: str) -> str:
    """
    Enhance clarity and readability throughout the paper.
    """
    console.print("[bold blue]Improving clarity throughout the paper...[/bold blue]")

    config = load_book_config(book_path)
    paper_title = config.book_name

    content = IMPROVE_CLARITY_PROMPT.format(prompt=prompt, paper_title=paper_title)

    improvements = create_message(book_path, content=content, history=[])

    save_to_markdown(
        book_path,
        "reviews/clarity_improvements.md",
        "Clarity Improvements",
        improvements,
    )

    console.print("[bold green]✔ Clarity improved successfully[/bold green]")
    return improvements
