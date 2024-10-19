# prompts/iterate.py

CHECK_NAMES_PROMPT = """
You have access to the entire text of the book, which has been loaded for analysis. 
Your task is to correct any inconsistencies in character names throughout the entire text. 
Ensure that each character's name is used consistently and appropriately based on the context. 
"""

FIX_NAME_PROMPT = """
Update all instances of the character name '{original_name}' to '{new_name}' throughout the text, taking into account context.
Ensure that any diminutives, nicknames, or variations of the name '{original_name}' are also replaced appropriately with contextually fitting forms of '{new_name}'.
Preserve the tone, style, and flow of the text as much as possible.
"""

REFINE_MOTIVATION_PROMPT = """
Refine the motivations of the character '{character_name}' throughout the story, ensuring that their actions, dialogue, and thoughts are aligned with a well-defined character arc.
The character is involved in a story about '{story_context}'.
Ensure the motivations are coherent with the plot and character development, maintaining the tone and style of the original text.
"""

STRENGTHEN_ARGUMENT_PROMPT = """
Ensure that the core argument of the story, '{argument}', is clearly articulated throughout this chapter.
Make sure the theme and message are consistent, reinforcing the central idea.
"""

INSERT_CHAPTER_PROMPT = """
Insert a new chapter at position {position} in the book. When a new chapter is inserted at position {position}, 
all subsequent chapters will be renumbered accordingly. 
For example, if a new chapter is inserted at position 3, the current chapter 3 will become chapter 4, chapter 4 will become chapter 5, and so on.
Use the retrieval system to access the chapters before and after this position, ensuring that the new chapter fits seamlessly with the narrative, themes, and character arcs.
Generate content only for the newly inserted chapter, not for the surrounding chapters.
Use this prompt for context: {prompt}.
"""

REWRITE_SURROUNDING_CHAPTERS_PROMPT = """
Write the chapters {chapter}, ensuring that they fit seamlessly with the previous and next chapter.
Utilize the retrieval system to gather context from the full book, making sure the tone, style, and character arcs remain consistent.
Generate content only for the requested chapter, without altering or including content from other chapters.
Use this prompt for context: {prompt}.
"""

INSERT_FLASHBACK_CHAPTER_PROMPT = """
Insert a new chapter at position {position} in the book, ensuring that the inserted chapter serves as a meaningful flashback.
The flashback should provide essential backstory or context that deepens the reader's understanding of the characters, themes, or events. 
All subsequent chapters will be renumbered accordingly. 
For example, if a new chapter is inserted at position 3, the current chapter 3 will become chapter 4, chapter 4 will become chapter 5, and so on.
Use the retrieval system to access the chapters before and after this position, ensuring that the new flashback fits seamlessly with the narrative, 
maintaining the tone and character arcs established in the book.
Generate content only for the newly inserted flashback chapter, not for the surrounding chapters.
Use this prompt for context: {prompt}.
"""

REWRITE_SURROUNDING_CHAPTERS_FOR_FLASHBACK_PROMPT = """
Write the chapters {chapter}, ensuring that they fit seamlessly with the previous and next chapter, 
and that the newly inserted flashback enhances the overall narrative flow.
Utilize the retrieval system to gather context from the full book, ensuring that the tone, style, and character arcs remain consistent.
The flashback should feel integral to the story, adding depth without disrupting the pacing or narrative.
Generate content only for the requested chapter, without altering or including content from other chapters.
Use this prompt for context: {prompt}.
"""

CHECK_CHAPTER_CONSISTENCY_PROMPT = """
Check the consistency of chapter with the entire book, ensuring that the events, tone, and character developments align with the overall narrative.
Use the retrieval system to access all relevant information from the entire book to maintain coherence in plot, character arcs, and themes.
Execute this check chapter by chapter, making sure each chapter fits seamlessly into the full story, and that there are no inconsistencies with the previous and subsequent chapters.
Ensure that the writing style and tone remain consistent throughout.
"""
