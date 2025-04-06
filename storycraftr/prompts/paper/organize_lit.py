LIT_SUMMARY_PROMPT_NEW = """
Generate a comprehensive literature summary for the research paper titled "{paper_title}" based on this input: {prompt}.

Focus on:
1. Key theories and concepts in the field
2. Major research findings and their implications
3. Current gaps in the literature
4. How existing research relates to your research question
5. Critical analysis of methodologies used

Format the output in a clear, academic style with proper citations and references.
Ensure to highlight the relationships between different works and their relevance to your research.
"""

LIT_SUMMARY_PROMPT_REFINE = """
Refine and improve the existing literature summary based on this input: {prompt}.

Consider:
1. Strengthening connections between different works
2. Identifying additional research gaps
3. Clarifying theoretical frameworks
4. Enhancing critical analysis
5. Improving flow and coherence

Maintain academic rigor while ensuring clarity and readability.
""" 