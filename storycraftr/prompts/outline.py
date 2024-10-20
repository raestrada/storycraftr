GENERAL_OUTLINE_PROMPT_NEW = """
Create a general outline for the book {book_name} based on this prompt: {prompt}.
Focus on general outline, then I will request help on plot-points, character-summary and chapt-synopsis.
"""

GENERAL_OUTLINE_PROMPT_REFINE = """
Refine and evolve the content based on this prompt: {prompt}.
Focus on improving the structure and flow of the outline, ensuring clarity and coherence throughout.
Focus on general outline, then I will request help on plot-points, character-summary and chapt-synopsis.
"""

CHARACTER_SUMMARY_PROMPT_NEW = """
Generate a detailed character summary for the book {book_name} based on this prompt: {prompt}.
Define most important characters startign for the main characters and continuing with secondaries.
Focus on character-summary, then I will request help on plot-points, general-outline and chapt-synopsis.
"""

CHARACTER_SUMMARY_PROMPT_REFINE = """
Refine and evolve the content based on this prompt: {prompt}.
Enhance character depth, motivation, and consistency with the overall narrative.
Focus on character-summary, then I will request help on plot-points, general-outline and chapt-synopsis.
"""

PLOT_POINTS_PROMPT_NEW = """
Generate the main plot points for the book {book_name} based on this prompt: {prompt}.
Focus on plot-points, then I will request help on plot-points, character-summary and chapt-synopsis.
"""

PLOT_POINTS_PROMPT_REFINE = """
Refine and evolve the content based on this prompt: {prompt}.
Ensure logical progression between plot points and strengthen the links between key events.
Focus on plot-points, then I will request help on plot-points, character-summary and chapt-synopsis.
"""

CHAPTER_SYNOPSIS_PROMPT_NEW = """
Generate a chapter-by-chapter synopsis for the book {book_name} based on this prompt: {prompt}.
List all chapters and its synopsis.
Focus on chapter-synopsis, then I will request help on gemneral-outline, character-summary and chapt-synopsis.
"""

CHAPTER_SYNOPSIS_PROMPT_REFINE = """
Refine and evolve the content based on this prompt: {prompt}.
Focus on improving chapter summaries by clarifying pivotal moments and enhancing narrative tension.
Focus on chapter-synopsis, then I will request help on gemneral-outline, character-summary and chapt-synopsis.
"""
