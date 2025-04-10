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
   - Framework description
   - Study scope

2. Methods
   - Data collection procedures
   - Analysis techniques
   - Tools and instruments
   - Validation methods

3. Implementation
   - Step-by-step process
   - Controls and measures
   - Quality assurance

4. Ethical Considerations
   - Data handling
   - Privacy measures
   - Compliance standards

Format as a detailed, replicable methodology that supports your research objectives.
"""

METHODOLOGY_PROMPT_REFINE = """
Refine the existing methodology based on this input: {prompt}.

Enhance:
1. Clarity
   - Procedural details
   - Technical specifications
   - Process flow

2. Rigor
   - Validation methods
   - Control measures
   - Error handling

3. Justification
   - Method selection
   - Tool choices
   - Analysis approaches
"""

RESULTS_PROMPT_NEW = """
Generate a results section for the paper titled "{paper_title}" based on this input: {prompt}.

Structure:
1. Key Findings
   - Primary outcomes
   - Statistical results
   - Data patterns

2. Analysis
   - Interpretation of data
   - Statistical significance
   - Trends and correlations

3. Visual Elements
   - Tables and figures
   - Data visualization
   - Key metrics

4. Validation
   - Reliability measures
   - Error analysis
   - Robustness checks

Present results objectively, focusing on the data and findings.
"""

RESULTS_PROMPT_REFINE = """
Refine the existing results based on this input: {prompt}.

Improve:
1. Clarity
   - Data presentation
   - Statistical reporting
   - Visual elements

2. Organization
   - Logical flow
   - Result grouping
   - Priority ordering

3. Technical Accuracy
   - Statistical precision
   - Data interpretation
   - Error reporting
"""

DISCUSSION_PROMPT_NEW = """
Generate a discussion section for the paper titled "{paper_title}" based on this input: {prompt}.

Include:
1. Interpretation
   - Key findings analysis
   - Context within field
   - Theoretical implications

2. Implications
   - Practical applications
   - Theoretical contributions
   - Field impact

3. Limitations
   - Study constraints
   - Data limitations
   - Method restrictions

4. Future Directions
   - Research opportunities
   - Methodology improvements
   - Extended applications

Connect findings to broader research context while maintaining academic rigor.
"""

DISCUSSION_PROMPT_REFINE = """
Refine the existing discussion based on this input: {prompt}.

Enhance:
1. Analysis Depth
   - Deeper insights
   - Broader implications
   - Theoretical connections

2. Critical Evaluation
   - Stronger arguments
   - Better limitations
   - Clearer implications

3. Future Directions
   - More specific recommendations
   - Practical suggestions
   - Research opportunities
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

Provide a strong closing that reinforces the paper's significance.
"""

CONCLUSION_PROMPT_REFINE = """
Refine the existing conclusion based on this input: {prompt}.

Strengthen:
1. Impact
   - Clearer contributions
   - Stronger implications
   - Better recommendations

2. Synthesis
   - Tighter integration
   - Better flow
   - Comprehensive coverage

3. Future Vision
   - Specific directions
   - Research opportunities
   - Field advancement
"""

CUSTOM_SECTION_PROMPT_NEW = """
Generate a custom section titled "{section_title}" for the paper titled "{paper_title}" based on this input: {prompt}.

Include:
1. Main Content
   - Key concepts
   - Supporting evidence
   - Analysis and interpretation

2. Structure
   - Clear organization
   - Logical flow
   - Appropriate transitions

3. Integration
   - Connection to methodology
   - Preparation for results
   - Alignment with research objectives

Format as a cohesive section that fits naturally between the methodology and results sections.
"""

CUSTOM_SECTION_PROMPT_REFINE = """
Refine the existing custom section titled "{section_title}" based on this input: {prompt}.

Enhance:
1. Content Quality
   - Depth of analysis
   - Supporting evidence
   - Technical accuracy

2. Structure
   - Logical flow
   - Clear transitions
   - Appropriate organization

3. Integration
   - Connection to other sections
   - Alignment with research objectives
   - Preparation for results section
"""
