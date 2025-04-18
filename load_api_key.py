#!/usr/bin/env python3
"""
Script to load OpenAI API key from StoryCraftr configuration
"""
import os
from pathlib import Path

def load_openai_api_key():
    """
    Loads the OpenAI API key from `.storycraftr` or `.papercraftr` folders
    in the user's home directory, using the first file it finds.
    """
    home_dir = Path.home()
    possible_paths = [
        os.path.join(home_dir, ".storycraftr", "openai_api_key.txt"),
        os.path.join(home_dir, ".papercraftr", "openai_api_key.txt"),
    ]

    print(f"Looking for API key in: {possible_paths}")

    for api_key_file in possible_paths:
        if os.path.exists(api_key_file):
            with open(api_key_file, "r") as file:
                api_key = file.read().strip()
            os.environ["OPENAI_API_KEY"] = api_key
            print(f"OPENAI_API_KEY loaded successfully from {api_key_file}")
            return api_key
    
    print("The file 'openai_api_key.txt' was not found in either .storycraftr or .papercraftr folders.")
    return None

if __name__ == "__main__":
    api_key = load_openai_api_key()
    if api_key:
        masked_key = api_key[:5] + "*" * (len(api_key) - 9) + api_key[-4:]
        print(f"API key loaded: {masked_key}")
    else:
        print("API key not found.") 