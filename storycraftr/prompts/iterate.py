# prompts/iterate.py

CHECK_NAMES_PROMPT = """
You have access to the entire text of the book, which has been loaded for analysis. 
Your task is to correct any inconsistencies in character names throughout the entire text. 
Ensure that each character's name is used consistently and appropriately based on the context. 

Return the corrected text without adding any extra explanations, notes, or comments. 
The output should be ready for use in the book directly, with all character name inconsist
"""

FIX_NAME_PROMPT = """
Update all instances of the character name '{original_name}' to '{new_name}' throughout the text, taking into account context.
Ensure that any diminutives, nicknames, or variations of the name '{original_name}' are also replaced appropriately with contextually fitting forms of '{new_name}'.
Preserve the tone, style, and flow of the text as much as possible.
Return the corrected text without adding any extra explanations, notes, or comments.
The output should be ready for use in the book directly, with the names fixed.
"""

REFINE_MOTIVATION_PROMPT = """
Refine the motivations of the character '{character_name}' throughout the story, ensuring that their actions, dialogue, and thoughts are aligned with a well-defined character arc.
The character is involved in a story about '{story_context}'.
Ensure the motivations are coherent with the plot and character development, maintaining the tone and style of the original text.
Return the refined text without adding any extra explanations, notes, or comments. 
The output should be ready for use in the book directly, with refined character motivations.
"""

STRENGTHEN_ARGUMENT_PROMPT = """
Ensure that the core argument of the story, '{argument}', is clearly articulated throughout this chapter.
Make sure the theme and message are consistent, reinforcing the central idea.
Return the revised markdown without adding any explanations, notes, or comments.
"""

INSERT_CHAPTER_PROMPT = """
Insert a new chapter at position {position} in the book.
Use the retrieval system to access the chapters before and after this position, ensuring that the new chapter fits seamlessly with the narrative, themes, and character arcs.
Use this prompt for context: {prompt}.
Return the new chapter in markdown format, ready for inclusion in the book without adding any explanations, notes, or comments.
"""

REWRITE_SURROUNDING_CHAPTERS_PROMPT = """
Rewrite the chapters {chapter}, ensuring that they fit seamlessly with the newly inserted chapter {position}.
Utilize the retrieval system to gather context from the full book, making sure the tone, style, and character arcs remain consistent.
Use this prompt for context: {prompt}.
Return the rewritten chapters in markdown format, without adding any explanations, notes, or comments.
"""
