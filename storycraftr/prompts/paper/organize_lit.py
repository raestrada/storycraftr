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

CONCEPT_MAP_PROMPT_NEW = """
Create a detailed concept map for the research paper titled "{paper_title}" based on this input: {prompt}.

Include:
1. Core concepts and theories
2. Relationships between concepts
3. Key variables and their interactions
4. Theoretical frameworks
5. Research gaps and opportunities

Format the output as a structured markdown document that clearly shows:
- Hierarchical relationships
- Cross-connections between concepts
- Supporting evidence from literature
- Potential research directions
"""

CONCEPT_MAP_PROMPT_REFINE = """
Refine and enhance the existing concept map based on this input: {prompt}.

Focus on:
1. Strengthening conceptual relationships
2. Adding missing connections
3. Clarifying hierarchies
4. Incorporating new insights
5. Improving visual clarity in the markdown structure

Ensure the concept map effectively communicates the theoretical framework while maintaining academic rigor.
""" 