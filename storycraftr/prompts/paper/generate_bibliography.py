GENERATE_BIBLIOGRAPHY_PROMPT = """
Generate a bibliography file in {format} format for all references in {references_path}.
Follow these rules:
1. Use proper {format} syntax
2. Include all required fields
3. Ensure consistent formatting
4. Sort entries alphabetically by author
5. Use unique citation keys

The bibliography should be ready to use with LaTeX.
"""

VALIDATE_BIBLIOGRAPHY_PROMPT = """
Validate the following {format} bibliography content:

{bibliography_content}

Check for:
1. Syntax correctness
2. Required fields presence
3. Consistent formatting
4. Valid citation keys

Respond with 'VALID' if everything is correct, or list the errors found.
"""
