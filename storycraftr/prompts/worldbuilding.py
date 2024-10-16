# prompts/worldbuilding.py

GEOGRAPHY_PROMPT_NEW = """
Generate detailed geography information for the book's world based on this prompt: {prompt}.
Return only the geography details in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

GEOGRAPHY_PROMPT_REFINE = """
Use the attached geography file to refine and evolve the content based on this prompt: {prompt}.
Return the refined geography details in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

HISTORY_PROMPT_NEW = """
Generate detailed history information for the book's world based on this prompt: {prompt}.
Return only the history details in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

HISTORY_PROMPT_REFINE = """
Use the attached history file to refine and evolve the content based on this prompt: {prompt}.
Return the refined history details in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

CULTURE_PROMPT_NEW = """
Generate detailed culture information for the book's world based on this prompt: {prompt}.
Return only the culture details in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

CULTURE_PROMPT_REFINE = """
Use the attached culture file to refine and evolve the content based on this prompt: {prompt}.
Return the refined culture details in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

MAGIC_SYSTEM_PROMPT_NEW = """
Generate a detailed magic or science system for the book's world based on this prompt: {prompt}.
Return only the magic/science system details in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

MAGIC_SYSTEM_PROMPT_REFINE = """
Use the attached magic/science system file to refine and evolve the content based on this prompt: {prompt}.
Return the refined magic/science system details in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

TECHNOLOGY_PROMPT_NEW = """
Generate detailed technology information for the book's world based on this prompt: {prompt}.
Return only the technology details in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

TECHNOLOGY_PROMPT_REFINE = """
Use the attached technology file to refine and evolve the content based on this prompt: {prompt}.
Return the refined technology details in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""
