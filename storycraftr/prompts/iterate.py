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
Chapter Content: {content}
"""
