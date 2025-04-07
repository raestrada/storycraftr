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
from storycraftr.prompts.paper.generate_section import (
    INTRODUCTION_PROMPT_NEW,
    INTRODUCTION_PROMPT_REFINE,
    METHODOLOGY_PROMPT_NEW,
    METHODOLOGY_PROMPT_REFINE,
    RESULTS_PROMPT_NEW,
    RESULTS_PROMPT_REFINE,
    DISCUSSION_PROMPT_NEW,
    DISCUSSION_PROMPT_REFINE,
    CONCLUSION_PROMPT_NEW,
    CONCLUSION_PROMPT_REFINE,
    CUSTOM_SECTION_PROMPT_NEW,
    CUSTOM_SECTION_PROMPT_REFINE,
)

console = Console()

def _generate_section(book_path: str, prompt: str, section_name: str,
                     new_prompt_template: str, refine_prompt_template: str) -> str:
    """
    Generic function to generate or refine a paper section.
    """
    console.print(f"[bold blue]Generating {section_name} section...[/bold blue]")

    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "sections", f"{section_name}.md")
    paper_title = config.book_name

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        console.print(f"[yellow]Refining existing {section_name}...[/yellow]")
        content = refine_prompt_template.format(
            prompt=prompt,
            paper_title=paper_title
        )
    else:
        console.print(f"[yellow]Generating new {section_name}...[/yellow]")
        content = new_prompt_template.format(
            prompt=prompt,
            paper_title=paper_title
        )

    section_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path
    )

    save_to_markdown(
        book_path,
        f"sections/{section_name}.md",
        section_name.title(),
        section_content
    )
    
    console.print(f"[bold green]✔ {section_name.title()} generated successfully[/bold green]")
    update_agent_files(book_path, assistant)
    return section_content

def generate_introduction(book_path: str, prompt: str) -> str:
    """Generate or refine the introduction section."""
    return _generate_section(book_path, prompt, "introduction",
                           INTRODUCTION_PROMPT_NEW, INTRODUCTION_PROMPT_REFINE)

def generate_methodology(book_path: str, prompt: str) -> str:
    """Generate or refine the methodology section."""
    return _generate_section(book_path, prompt, "methodology",
                           METHODOLOGY_PROMPT_NEW, METHODOLOGY_PROMPT_REFINE)

def generate_results(book_path: str, prompt: str) -> str:
    """Generate or refine the results section."""
    return _generate_section(book_path, prompt, "results",
                           RESULTS_PROMPT_NEW, RESULTS_PROMPT_REFINE)

def generate_discussion(book_path: str, prompt: str) -> str:
    """Generate or refine the discussion section."""
    return _generate_section(book_path, prompt, "discussion",
                           DISCUSSION_PROMPT_NEW, DISCUSSION_PROMPT_REFINE)

def generate_conclusion(book_path: str, prompt: str) -> str:
    """Generate or refine the conclusion section."""
    return _generate_section(book_path, prompt, "conclusion",
                           CONCLUSION_PROMPT_NEW, CONCLUSION_PROMPT_REFINE)

def generate_custom_section(book_path: str, prompt: str, section_title: str, order: int) -> str:
    """
    Generate or refine a custom section with a specified title and order.
    
    Args:
        book_path (str): Path to the book directory
        prompt (str): Instructions for the section content
        section_title (str): Title of the custom section
        order (int): Order number for the section (between methodology and results)
        
    Returns:
        str: Generated section content
    """
    # Create a sanitized filename from the section title
    section_name = f"custom_{order}_{section_title.lower().replace(' ', '_')}"
    
    # Format the prompts with the section title
    new_prompt = CUSTOM_SECTION_PROMPT_NEW.format(
        section_title=section_title,
        paper_title=load_book_config(book_path).book_name,
        prompt=prompt
    )
    
    refine_prompt = CUSTOM_SECTION_PROMPT_REFINE.format(
        section_title=section_title,
        prompt=prompt
    )
    
    return _generate_section(book_path, prompt, section_name, new_prompt, refine_prompt) 