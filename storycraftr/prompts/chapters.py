# prompts/chapters.py

CHAPTER_PROMPT_NEW = """
Write a detailed chapter for the following book premise: {prompt}. Write it in {language}.
"""

CHAPTER_PROMPT_REFINE = """
Use the attached chapter file as a reference to evolve and improve the content based on this prompt: {prompt}. Write it in {language}.
"""

COVER_PROMPT = """
Create a professional book cover in markdown format for the book titled '{title}'. 
Include the title, author ('{author}').
put the placeholder PUT_IMAGE_CODE_HERE replacing all the img md code so then I can replace it with the cover image.
STRICTLY Return only the cover markdown limited only to what should be printed.
Use this prompt as additional context: {prompt}. Write the content in {language}.
"""

BACK_COVER_PROMPT = """
Generate a detailed synopsis for the back cover of the book based on this prompt: {prompt}. Write it in {language}.
Include the title, author ('{author}'), genre ('{genre}'), and alternate languages ('{alternate_languages}').
Return only the back cover markdown.
Include de license of type {license} with its description like a professional book.
Use this prompt as additional context: {prompt}. Write the content in {language}.
"""

EPILOGUE_PROMPT_NEW = """
Generate the epilogue for the book based on this prompt: {prompt}. Write it in {language}.
"""

EPILOGUE_PROMPT_REFINE = """
Use the attached epilogue file as a reference to evolve and improve the content based on this prompt: {prompt}. Write it in {language}.
"""
