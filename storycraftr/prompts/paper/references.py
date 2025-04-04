ADD_REFERENCE_PROMPT = """
Format and add the following reference for the paper titled "{paper_title}" based on this input: {prompt}.

Consider:
1. Citation Style
   - Format according to specified style guide
   - Required elements for reference type
   - Proper ordering of elements
   - Punctuation and spacing

2. Reference Details
   - Author names and ordering
   - Publication year
   - Title formatting
   - Source information
   - DOI/URL if available
   - Volume/Issue numbers
   - Page numbers

3. Reference Categories
   - Journal articles
   - Conference papers
   - Books/book chapters
   - Technical reports
   - Web resources
   - Preprints/working papers

Format the output as a properly structured reference entry.
"""

FORMAT_REFERENCES_PROMPT = """
Format all references for the paper titled "{paper_title}" according to this style guide: {prompt}.

Ensure:
1. Consistency
   - Uniform formatting
   - Consistent style application
   - Proper alphabetization
   - Complete information

2. Style Requirements
   - Author name format
   - Title capitalization
   - Journal abbreviations
   - Publication details
   - Electronic source handling

3. Special Cases
   - Multiple authors
   - Organization authors
   - Non-English sources
   - Online resources
   - Preprints and working papers

Format the output as a complete reference list.
"""

CHECK_CITATIONS_PROMPT = """
Review and check all citations in the paper titled "{paper_title}" based on this input: {prompt}.

Analyze:
1. Citation Accuracy
   - Match with reference list
   - Author name consistency
   - Year consistency
   - Page numbers when needed

2. Citation Style
   - In-text citation format
   - Multiple author handling
   - Repeated citations
   - Citation grouping

3. Citation Coverage
   - Key claims supported
   - Methods cited
   - Data sources credited
   - Software/tools cited

4. Citation Balance
   - Recent vs. classic works
   - Primary vs. secondary sources
   - Self-citation ratio
   - Field representation

Provide a detailed report of citation issues and suggested corrections.
"""

GENERATE_CITATION_PROMPT = """
Generate a proper citation for the following reference in the paper titled "{paper_title}" using this format: {prompt}.

Consider:
1. Citation Components
   - Author names
   - Publication year
   - Title elements
   - Source details

2. Citation Context
   - First vs. subsequent citations
   - Multiple authors handling
   - Page numbers if needed
   - Parenthetical vs. narrative

3. Special Cases
   - No author
   - No date
   - Secondary sources
   - Multiple works same author/year

Format the output as both in-text citation and reference list entry.
""" 