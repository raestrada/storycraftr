# prompts/chapters.py

CHAPTER_PROMPT_NEW = """
Write a detailed and engaging chapter for the following book premise: {prompt}.
Ensure the chapter contributes meaningfully to the plot, character development, and overall progression of the story.
Return only the markdown content of the chapter, ready for direct inclusion in the book.

Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""


CHAPTER_PROMPT_REFINE = """
Refine and enhance the attached chapter file.
Improve the narrative flow, character development, and pacing, based on the following prompt: {prompt}.
Ensure that the refined chapter maintains consistency with the story's tone, themes, and existing character arcs.

Return the refined markdown content, ready for direct inclusion in the book, without adding any extra explanations, notes, or comments.
Write the content in {language}.
"""


COVER_PROMPT = """
Create a professional book cover in markdown format for the book titled '{title}'.
Include only the title and author ('{author}').
Replace any image markdown with the placeholder PUT_IMAGE_CODE_HERE so it can be replaced with the cover image later.
Do not include any explanations, notes, or additional comments in the output.
Strictly return only the cover content in markdown format, ready for direct use in the book.

Use the following as additional context: {prompt}.
Write the content in {language}.
"""


BACK_COVER_PROMPT = """
Generate a detailed and engaging synopsis for the back cover of the book titled '{title}', written by '{author}'.
Include the genre ('{genre}') and any alternate languages ('{alternate_languages}') where the book is available.
Also, include the license type '{license}', along with a professional description of the license.

Return only the back cover in markdown format, with all the required elements for direct use in the book.
Do not include any additional explanations, notes, or comments.

Use the following as additional context: {prompt}.
Write the content in {language}.
"""


EPILOGUE_PROMPT_NEW = """
Generate a complete and compelling epilogue for the book based on the following context: {prompt}.
The epilogue should tie up loose ends and provide closure in a way that complements the main storyline.
Return only the markdown content of the epilogue, formatted and ready for direct inclusion in the book.

Do not include any additional explanations, notes, or comments.
Write the content in {language}.
"""


EPILOGUE_PROMPT_REFINE = """
Refine and enhance the epilogue using the attached file as a reference.
Improve its narrative flow, tie up remaining plot points, and evolve the content based on this prompt: {prompt}.
Ensure that the refined epilogue maintains the tone and themes of the story.

Return the refined markdown content, ready for direct inclusion in the book, without adding any extra explanations, notes, or comments.
Write the content in {language}.
"""
