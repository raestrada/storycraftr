OUTLINE_SECTIONS_PROMPT_NEW = """
Create a detailed outline for the research paper titled "{paper_title}" based on this input: {prompt}.

The outline should include:
1. Introduction
   - Background and context
   - Problem statement
   - Research objectives
   - Significance of the study

2. Literature Review
   - Theoretical framework
   - Current state of research
   - Research gaps

3. Methodology
   - Research design
   - Data collection methods
   - Analysis approach
   - Validation methods

4. Results
   - Key findings
   - Data analysis
   - Statistical significance

5. Discussion
   - Interpretation of results
   - Implications
   - Limitations
   - Future directions

6. Conclusion
   - Summary of findings
   - Contributions
   - Recommendations

Format the output as a structured markdown document with clear hierarchical relationships and section descriptions.
"""

OUTLINE_SECTIONS_PROMPT_REFINE = """
Refine and enhance the existing outline based on this input: {prompt}.

Focus on:
1. Improving logical flow between sections
2. Strengthening connections between research questions and methods
3. Ensuring comprehensive coverage of key topics
4. Balancing section lengths and depth
5. Incorporating feedback and new insights

Maintain academic rigor while ensuring clarity and coherence.
"""

DEFINE_METHODS_PROMPT_NEW = """
Define the research methodology for the paper titled "{paper_title}" based on this input: {prompt}.

Include detailed descriptions of:
1. Research Design
   - Approach (qualitative, quantitative, mixed)
   - Design rationale
   - Research framework

2. Data Collection
   - Methods and instruments
   - Sampling strategy
   - Data sources
   - Collection procedures

3. Analysis Methods
   - Analytical techniques
   - Tools and software
   - Statistical methods
   - Validation approach

4. Quality Assurance
   - Reliability measures
   - Validity checks
   - Bias control
   - Ethical considerations

Format the output as a comprehensive methodology section with clear justification for each choice.
"""

DEFINE_METHODS_PROMPT_REFINE = """
Refine and improve the existing methodology based on this input: {prompt}.

Focus on:
1. Strengthening justification for methodological choices
2. Improving clarity of procedures
3. Enhancing reliability and validity measures
4. Adding missing details or steps
5. Addressing potential limitations

Ensure the methodology is robust, replicable, and aligned with research objectives.
""" 