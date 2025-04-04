GENERATE_LATEX_PROMPT = """
Generate LaTeX content for the paper in {language} using the {template} template.
The paper content is located in {paper_path}.

Follow these rules:
1. Use proper {template} template structure
2. Include all necessary packages
3. Set up proper language settings for {language}
4. Include all paper sections in correct order
5. Handle references and citations properly
6. Include proper metadata (title, author, etc.)

The LaTeX should be ready to compile into a PDF.
"""

VALIDATE_LATEX_PROMPT = """
Validate the following LaTeX content:

{latex_content}

Check for:
1. Syntax correctness
2. Required structure elements
3. Package dependencies
4. Bibliography setup
5. Language settings

Respond with 'VALID' if everything is correct, or list the errors found.
"""
