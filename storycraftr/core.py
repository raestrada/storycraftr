import os
import json
from typing import NamedTuple

# Define the structure for the book using NamedTuple
class BookConfig(NamedTuple):
    book_name: str
    primary_language: str
    alternate_languages: list
    default_author: str
    genre: str

# Function to load the JSON file and convert it into a BookConfig object
def load_book_config(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        # Create an instance of BookConfig with the values from the JSON
        book_config = BookConfig(
            book_name=data['book_name'],
            primary_language=data['primary_language'],
            alternate_languages=data['alternate_languages'],
            default_author=data['default_author'],
            genre=data['genre']
        )
    return book_config

# Function that receives the book directory and loads the storycraftr.json file
def get_config(book_name):
    # Generate the full path to the storycraftr.json file inside the book_name directory
    config_path = os.path.join(book_name, 'storycraftr.json')
    
    # Check if the storycraftr.json file exists
    if os.path.exists(config_path):
        # Load and return the configuration using load_book_config
        return load_book_config(config_path)
    else:
        # Raise an error if the config file doesn't exist
        raise FileNotFoundError(f"The configuration file '{config_path}' does not exist.")

# Example usage
try:
    config = get_config('La_purga_de_los_dioses')
    print(config)
except FileNotFoundError as e:
    print(e)

def file_has_more_than_three_lines(file_path):
    """Check if a file has more than three lines."""
    with open(file_path, 'r') as file:
        # Iterate through the first 4 lines and stop if we reach 4 lines
        for i, _ in enumerate(file, 1):
            if i > 3:
                return True
    return False