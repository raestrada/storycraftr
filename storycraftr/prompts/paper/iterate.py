REINFORCE_IDEAS_PROMPT = """
Review and strengthen the paper titled "{paper_title}" based on this input: {prompt}.

Focus on:
1. Argument Strength
   - Core ideas
   - Supporting evidence
   - Logical flow

2. Technical Depth
   - Methodology details
   - Results interpretation
   - Analysis rigor

3. Impact Enhancement
   - Contribution clarity
   - Practical implications
   - Theoretical significance

4. Writing Quality
   - Academic style
   - Technical precision
   - Clarity and flow

Provide specific suggestions for improvement while maintaining the paper's core message.
"""

IMPROVE_CLARITY_PROMPT = """
Enhance the clarity of the paper titled "{paper_title}" based on this input: {prompt}.

Address:
1. Structure
   - Section organization
   - Paragraph flow
   - Transitions

2. Language
   - Technical terminology
   - Sentence structure
   - Academic style

3. Explanation
   - Complex concepts
   - Methodology details
   - Result interpretation

4. Presentation
   - Visual elements
   - Data representation
   - Format consistency

Focus on making the content more accessible while maintaining academic rigor.
""" 