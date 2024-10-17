# prompts/chapters.py

CHAPTER_PROMPT_NEW = """
Write a detailed and engaging chapter for the following book premise: {prompt}.
Ensure the chapter contributes meaningfully to the plot, character development, and overall progression of the story.
Write the content in {language}.
"""


CHAPTER_PROMPT_REFINE = """
Refine and evolve the content based on this prompt: {prompt}.
Improve the narrative flow, character development, and pacing, based on the following prompt: {prompt}.
Write the content in {language}.
"""


COVER_PROMPT = """
Create a professional book cover in markdown format for the book titled '{title}'.
Include only the title and author ('{author}').
Strictly return only the cover content in markdown format, ready for direct use in the book.

Use the following as additional context: {prompt}.
Write the content in {language}.
"""


BACK_COVER_PROMPT = """
Generate a detailed and engaging synopsis for the back cover of the book titled '{title}', written by '{author}'.
Include the genre ('{genre}') and any alternate languages ('{alternate_languages}') where the book is available.
Also, include the license type '{license}', along with a professional description of the license.
Use the following as additional context: {prompt}.
Write the content in {language}.
"""


EPILOGUE_PROMPT_NEW = """
Generate a complete and compelling epilogue for the book based on the following context: {prompt}.
The epilogue should tie up loose ends and provide closure in a way that complements the main storyline.
Write the content in {language}.
"""


EPILOGUE_PROMPT_REFINE = """
Refine and evolve the content based on this prompt: {prompt}.
Improve its narrative flow, tie up remaining plot points, and evolve the content based on this prompt: {prompt}.
Ensure that the refined epilogue maintains the tone and themes of the story.
Write the content in {language}.
"""
