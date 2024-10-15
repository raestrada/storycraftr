import os
from rich.console import Console

console = Console()

# Function to save content to a markdown file
def save_to_markdown(book_name, file_name, header, content):
    """Save the generated content to the specified markdown file."""
    file_path = os.path.join(book_name, 'outline', file_name)
    console.print(f"[bold blue]Saving content to {file_path}...[/bold blue]")  # Progress message
    with open(file_path, 'w') as f:
        f.write(f"# {header}\n\n{content}")
    console.print(f"[bold green]Content saved successfully to {file_path}[/bold green]")  # Success message
    return file_path  # Return the path for reuse

# Function to append content to an existing markdown file
def append_to_markdown(book_name, folder_name, file_name, content):
    """Append content to an existing markdown file."""
    file_path = os.path.join(book_name, folder_name, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, 'a') as f:
            f.write(f"\n\n{content}")
        print(f"Appended content to {file_path}")
    else:
        raise FileNotFoundError(f"File {file_path} does not exist.")

# Function to read content from a markdown file
def read_from_markdown(book_name, folder_name, file_name):
    """Read content from the specified markdown file."""
    file_path = os.path.join(book_name, folder_name, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        print(f"Read content from {file_path}")
        return content
    else:
        raise FileNotFoundError(f"File {file_path} does not exist.")
