RUN_ANALYSIS_PROMPT_NEW = """
Generate a comprehensive data analysis plan for the research paper titled "{paper_title}" based on this input: {prompt}.

Include detailed descriptions of:
1. Data Preparation
   - Data cleaning procedures
   - Variable transformations
   - Handling missing data
   - Data validation steps

2. Statistical Analysis
   - Descriptive statistics
   - Inferential statistics
   - Statistical tests and justification
   - Effect size calculations
   - Power analysis (if applicable)

3. Advanced Analytics (if applicable)
   - Machine learning models
   - Feature selection/engineering
   - Model validation
   - Performance metrics

4. Visualization Plan
   - Key visualizations
   - Chart types and justification
   - Visual representation of relationships

Format the output as a structured analysis plan with clear steps and justifications.
"""

RUN_ANALYSIS_PROMPT_REFINE = """
Refine and enhance the existing analysis plan based on this input: {prompt}.

Focus on:
1. Improving analytical rigor
2. Adding missing analyses
3. Strengthening statistical approaches
4. Enhancing visualization methods
5. Addressing potential limitations

Ensure all analyses align with research objectives and methodological framework.
"""

SUMMARIZE_RESULTS_PROMPT_NEW = """
Generate a comprehensive summary of research results for the paper titled "{paper_title}" based on this input: {prompt}.

Structure the summary to include:
1. Key Findings
   - Primary outcomes
   - Statistical significance
   - Effect sizes
   - Confidence intervals

2. Data Patterns
   - Trends and relationships
   - Unexpected findings
   - Subgroup analyses

3. Visual Results
   - Key figures and tables
   - Data visualization descriptions
   - Interpretation guidelines

4. Technical Details
   - Statistical test results
   - Model performance metrics
   - Validation outcomes

Format the output as a clear, academic results section with proper statistical reporting.
"""

SUMMARIZE_RESULTS_PROMPT_REFINE = """
Refine and enhance the existing results summary based on this input: {prompt}.

Focus on:
1. Clarifying key findings
2. Strengthening statistical reporting
3. Improving data visualization descriptions
4. Adding context to results
5. Addressing any gaps or inconsistencies

Ensure results are presented clearly and support research objectives.
""" 