CHECK_CONSISTENCY_PROMPT = """
Review and check the consistency of the paper titled "{paper_title}" based on this input: {prompt}.

Analyze the following aspects:
1. Logical Flow
   - Coherence between sections
   - Progression of arguments
   - Transition quality
   - Alignment with research objectives

2. Methodological Consistency
   - Methods align with research questions
   - Analysis matches methodology
   - Results support conclusions
   - Limitations properly addressed

3. Technical Consistency
   - Terminology usage
   - Variable naming
   - Statistical reporting
   - Citation style

4. Structural Consistency
   - Section organization
   - Heading hierarchy
   - Format compliance
   - Figure/table numbering

Provide a detailed report of inconsistencies and suggested improvements.
"""

FINALIZE_FORMAT_PROMPT = """
Format and polish the paper titled "{paper_title}" based on this input: {prompt}.

Focus on:
1. Academic Style
   - Formal language
   - Active/passive voice balance
   - Technical terminology
   - Clear and concise writing

2. Formatting Standards
   - Section headers
   - Figure/table captions
   - Citation format
   - Reference style
   - Page layout

3. Content Organization
   - Abstract structure
   - Section flow
   - Paragraph structure
   - List formatting

4. Visual Elements
   - Table formatting
   - Figure placement
   - Equation display
   - Margin consistency

Ensure compliance with academic standards while maintaining readability.
"""

GENERATE_ABSTRACT_PROMPT_NEW = """
Generate a comprehensive abstract for the paper titled "{paper_title}" based on this input: {prompt}.

Include:
1. Background/Context
   - Research field
   - Current knowledge gap
   - Problem statement

2. Objectives
   - Research questions
   - Study aims
   - Hypotheses

3. Methods
   - Research approach
   - Key methodologies
   - Analysis techniques

4. Results
   - Key findings
   - Statistical significance
   - Main outcomes

5. Conclusions
   - Primary implications
   - Contributions
   - Future directions

Format as a concise, informative abstract following academic standards.
Maximum length: 250 words.
"""

GENERATE_ABSTRACT_PROMPT_REFINE = """
Refine and enhance the existing abstract based on this input: {prompt}.

Focus on:
1. Clarity and Concision
   - Clear problem statement
   - Precise methodology description
   - Key results emphasis
   - Impactful conclusions

2. Structure and Flow
   - Logical progression
   - Smooth transitions
   - Essential information
   - Word economy

3. Impact and Relevance
   - Research significance
   - Key contributions
   - Practical implications
   - Target audience appeal

Maintain academic rigor while ensuring accessibility.
Maximum length: 250 words.
""" 