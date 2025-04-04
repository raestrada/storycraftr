INTRODUCTION_PROMPT_NEW = """
Generate an introduction section for the paper titled "{paper_title}" based on this input: {prompt}.

Include:
1. Background
   - Field context
   - Current state of knowledge
   - Research gaps

2. Problem Statement
   - Research problem
   - Significance
   - Scope

3. Research Objectives
   - Main objectives
   - Specific goals
   - Research questions/hypotheses

4. Paper Structure
   - Overview of methodology
   - Key contributions
   - Paper organization

Format as a clear, engaging introduction that sets up the paper's narrative.
"""

INTRODUCTION_PROMPT_REFINE = """
Refine the existing introduction based on this input: {prompt}.

Focus on:
1. Clarity and Flow
   - Logical progression
   - Engaging narrative
   - Clear transitions

2. Content Enhancement
   - Stronger motivation
   - Clearer objectives
   - Better context

3. Technical Accuracy
   - Updated references
   - Precise terminology
   - Current state of field
"""

LITERATURE_REVIEW_PROMPT_NEW = """
Generate a literature review section for the paper titled "{paper_title}" based on this input: {prompt}.

Structure:
1. Theoretical Framework
   - Key theories
   - Conceptual models
   - Historical development

2. Current Research
   - Major findings
   - Methodological approaches
   - Research trends

3. Critical Analysis
   - Research gaps
   - Contradictions
   - Limitations
   - Future directions

4. Synthesis
   - Relationships between studies
   - Common themes
   - Emerging patterns

Format as a comprehensive yet focused review that builds the foundation for your research.
"""

LITERATURE_REVIEW_PROMPT_REFINE = """
Refine the existing literature review based on this input: {prompt}.

Enhance:
1. Coverage
   - Recent publications
   - Key papers
   - Different perspectives

2. Analysis
   - Deeper critique
   - Better synthesis
   - Clearer connections

3. Relevance
   - Focus on research questions
   - Support for methodology
   - Context for results
"""

METHODOLOGY_PROMPT_NEW = """
Generate a methodology section for the paper titled "{paper_title}" based on this input: {prompt}.

Include:
1. Research Design
   - Approach justification
   - Design framework
   - Variables/constructs

2. Data Collection
   - Methods
   - Instruments
   - Procedures
   - Sample selection

3. Analysis Methods
   - Analytical techniques
   - Statistical tests
   - Tools/software
   - Data processing

4. Validation
   - Quality measures
   - Reliability checks
   - Bias control
   - Ethical considerations

Format as a detailed, replicable methodology section.
"""

METHODOLOGY_PROMPT_REFINE = """
Refine the existing methodology based on this input: {prompt}.

Improve:
1. Clarity
   - Clearer procedures
   - Better explanations
   - More detail where needed

2. Rigor
   - Stronger justification
   - Better validation
   - More robust methods

3. Replicability
   - Complete procedures
   - Specific parameters
   - Clear conditions
"""

RESULTS_PROMPT_NEW = """
Generate a results section for the paper titled "{paper_title}" based on this input: {prompt}.

Present:
1. Main Findings
   - Key results
   - Statistical analyses
   - Data patterns

2. Data Presentation
   - Tables
   - Figures
   - Charts
   - Statistical summaries

3. Observations
   - Patterns
   - Trends
   - Anomalies
   - Relationships

4. Validation
   - Robustness checks
   - Error analysis
   - Confidence measures

Format as a clear, objective presentation of research findings.
"""

RESULTS_PROMPT_REFINE = """
Refine the existing results based on this input: {prompt}.

Enhance:
1. Clarity
   - Better organization
   - Clearer presentation
   - Improved flow

2. Completeness
   - Additional analyses
   - Missing details
   - Supporting data

3. Visualization
   - Better figures
   - Clearer tables
   - More effective displays
"""

DISCUSSION_PROMPT_NEW = """
Generate a discussion section for the paper titled "{paper_title}" based on this input: {prompt}.

Include:
1. Interpretation
   - Results meaning
   - Context
   - Implications

2. Comparison
   - Prior research
   - Theoretical framework
   - Expected outcomes

3. Implications
   - Theoretical impact
   - Practical applications
   - Future directions

4. Limitations
   - Study constraints
   - Methodological limits
   - Generalizability

Format as an insightful discussion that connects results to broader context.
"""

DISCUSSION_PROMPT_REFINE = """
Refine the existing discussion based on this input: {prompt}.

Strengthen:
1. Analysis
   - Deeper insights
   - Better connections
   - Stronger arguments

2. Context
   - Broader implications
   - Field impact
   - Future directions

3. Balance
   - Limitations vs. strengths
   - Theory vs. practice
   - Current vs. future
"""

CONCLUSION_PROMPT_NEW = """
Generate a conclusion section for the paper titled "{paper_title}" based on this input: {prompt}.

Include:
1. Summary
   - Key findings
   - Main contributions
   - Research answers

2. Implications
   - Theoretical impact
   - Practical applications
   - Field advancement

3. Future Work
   - Research directions
   - Open questions
   - Recommendations

Format as a strong conclusion that reinforces the paper's value.
"""

CONCLUSION_PROMPT_REFINE = """
Refine the existing conclusion based on this input: {prompt}.

Enhance:
1. Impact
   - Stronger contributions
   - Clearer implications
   - Better recommendations

2. Synthesis
   - Better summary
   - Clearer message
   - Stronger ending

3. Future Vision
   - More specific directions
   - Better opportunities
   - Clearer next steps
""" 