# prompts/outline.py

GENERAL_OUTLINE_PROMPT_NEW = """
Create a general outline for a book based on this prompt: {prompt}. Write it in {language}.
"""

GENERAL_OUTLINE_PROMPT_REFINE = """
Use the attached general outline file to evolve the content based on this prompt: {prompt}. Write it in {language}.
"""

CHARACTER_SUMMARY_PROMPT_NEW = """
Generate a character summary for the book based on this prompt: {prompt}. Write it in {language}.
"""

CHARACTER_SUMMARY_PROMPT_REFINE = """
Use the attached character summary file to evolve the content based on this prompt: {prompt}. Write it in {language}.
"""

PLOT_POINTS_PROMPT_NEW = """
Generate the main plot points for the book based on this prompt: {prompt}. Write it in {language}.
"""

PLOT_POINTS_PROMPT_REFINE = """
Use the attached plot points file to evolve the content based on this prompt: {prompt}. Write it in {language}.
"""

CHAPTER_SYNOPSIS_PROMPT_NEW = """
Generate a chapter-by-chapter synopsis for the book based on this prompt: {prompt}. Write it in {language}.
"""

CHAPTER_SYNOPSIS_PROMPT_REFINE = """
Use the attached chapter-by-chapter synopsis file to evolve the content based on this prompt: {prompt}. Write it in {language}.
"""
