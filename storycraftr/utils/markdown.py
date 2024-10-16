import os
from storycraftr.agent.agents import create_or_get_assistant, get_thread, create_message
from rich.console import Console
from rich.progress import track

console = Console()


# Function to save content to a markdown file
def save_to_markdown(book_name, file_name, header, content):
    """Save the generated content to the specified markdown file."""
    file_path = os.path.join(book_name, file_name)
    console.print(
        f"[bold blue]Saving content to {file_path}...[/bold blue]"
    )  # Progress message
    with open(file_path, "w") as f:
        f.write(f"# {header}\n\n{content}")
    console.print(
        f"[bold green]Content saved successfully to {file_path}[/bold green]"
    )  # Success message
    return file_path  # Return the path for reuse


# Function to append content to an existing markdown file
def append_to_markdown(book_name, folder_name, file_name, content):
    """Append content to an existing markdown file."""
    file_path = os.path.join(book_name, folder_name, file_name)

    if os.path.exists(file_path):
        with open(file_path, "a") as f:
            f.write(f"\n\n{content}")
        print(f"Appended content to {file_path}")
    else:
        raise FileNotFoundError(f"File {file_path} does not exist.")


# Function to read content from a markdown file
def read_from_markdown(book_name, folder_name, file_name):
    """Read content from the specified markdown file."""
    file_path = os.path.join(book_name, folder_name, file_name)

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            content = f.read()
        print(f"Read content from {file_path}")
        return content
    else:
        raise FileNotFoundError(f"File {file_path} does not exist.")


import os
import re
from storycraftr.agent.agents import create_or_get_assistant, get_thread, create_message
from rich.console import Console
from rich.progress import track

console = Console()


def consolidate_book_md(
    book_name: str, primary_language: str, translate: str = None
) -> str:
    chapters_dir = os.path.join(book_name, "chapters")
    output_file_name = (
        f"book-{primary_language}.md" if not translate else f"book-{translate}.md"
    )
    output_file_path = os.path.join(book_name, "book", output_file_name)

    # Ensure the "book" folder exists
    book_dir = os.path.join(book_name, "book")
    os.makedirs(book_dir, exist_ok=True)

    # Create or get the assistant and thread
    assistant = create_or_get_assistant(book_name)
    thread = get_thread()

    # Files to process in the specified order
    files_to_process = []

    # Add cover.md and back-cover.md
    if os.path.exists(os.path.join(chapters_dir, "cover.md")):
        files_to_process.append("cover.md")
    if os.path.exists(os.path.join(chapters_dir, "back-cover.md")):
        files_to_process.append("back-cover.md")

    # Add chapters in chapter-[number].md format in ascending order
    chapter_files = [
        f for f in os.listdir(chapters_dir) if re.match(r"chapter-\d+\.md", f)
    ]
    chapter_files.sort(
        key=lambda x: int(re.findall(r"\d+", x)[0])
    )  # Sort by chapter number
    files_to_process.extend(chapter_files)

    # Add epilogue.md
    if os.path.exists(os.path.join(chapters_dir, "epilogue.md")):
        files_to_process.append("epilogue.md")

    # Log start of consolidation and translation status
    if translate:
        console.print(
            f"Consolidating chapters for [bold]{book_name}[/bold] and translating to [bold]{translate}[/bold]..."
        )
    else:
        console.print(
            f"Consolidating chapters for [bold]{book_name}[/bold] without translation..."
        )

    with open(output_file_path, "w", encoding="utf-8") as consolidated_md:
        # Process each file in the specified order
        for chapter_file in track(
            files_to_process, description="Consolidating chapters..."
        ):
            chapter_path = os.path.join(chapters_dir, chapter_file)

            if chapter_file.endswith(".md"):
                console.print(f"Processing [bold]{chapter_file}[/bold]...")

                with open(chapter_path, "r", encoding="utf-8") as chapter_md:
                    content = chapter_md.read()

                    # If 'translate' is not None, translate the content using OpenAI
                    if translate:
                        console.print(
                            f"Translating [bold]{chapter_file}[/bold] to [bold]{translate}[/bold]..."
                        )
                        content = create_message(
                            thread_id=thread.id, content=content, assistant=assistant
                        )

                    # Write the (translated or original) content into the consolidated file
                    consolidated_md.write(content)
                    consolidated_md.write("\n\\newpage\n")

    # Log the completion of the consolidation
    console.print(
        f"[green bold]Book consolidated[/green bold] at [bold]{output_file_path}[/bold]"
    )
    return output_file_path
