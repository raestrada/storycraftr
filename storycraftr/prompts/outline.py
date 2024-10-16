GENERAL_OUTLINE_PROMPT_NEW = """
Create a general outline for a book based on this prompt: {prompt}.
Return only the general outline in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

GENERAL_OUTLINE_PROMPT_REFINE = """
Use the attached general outline file to refine and evolve the content based on this prompt: {prompt}.
Return the refined outline in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

CHARACTER_SUMMARY_PROMPT_NEW = """
Generate a detailed character summary for the book based on this prompt: {prompt}.
Return only the character summary in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

CHARACTER_SUMMARY_PROMPT_REFINE = """
Use the attached character summary file to refine and evolve the content based on this prompt: {prompt}.
Return the refined character summary in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

PLOT_POINTS_PROMPT_NEW = """
Generate the main plot points for the book based on this prompt: {prompt}.
Return only the plot points in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

PLOT_POINTS_PROMPT_REFINE = """
Use the attached plot points file to refine and evolve the content based on this prompt: {prompt}.
Return the refined plot points in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

CHAPTER_SYNOPSIS_PROMPT_NEW = """
Generate a chapter-by-chapter synopsis for the book based on this prompt: {prompt}.
Return only the chapter-by-chapter synopsis in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""

CHAPTER_SYNOPSIS_PROMPT_REFINE = """
Use the attached chapter-by-chapter synopsis file to refine and evolve the content based on this prompt: {prompt}.
Return the refined chapter-by-chapter synopsis in markdown format, ready for direct inclusion in the book.
Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""
