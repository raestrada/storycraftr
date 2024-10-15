import os

# Function to save content to a markdown file
def save_to_markdown(book_name, folder_name, file_name, header, content):
    """Save the generated content to the specified markdown file."""
    directory = os.path.join(book_name, folder_name)
    os.makedirs(directory, exist_ok=True)  # Ensure the directory exists

    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w') as f:
        f.write(f"# {header}\n\n{content}")
    
    print(f"Saved content to {file_path}")

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
