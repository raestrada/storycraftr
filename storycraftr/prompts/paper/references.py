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
   - Multiple authors
   - Organization authors
   - No author cases

3. Citation Format
   - Parenthetical vs. narrative citations
   - Multiple citations
   - Page numbers when needed
   - Special cases (e.g., personal communications)

Format the output as a properly formatted citation.
"""

GENERATE_BIBTEX_PROMPT = """
Generate a complete BibTeX file for the paper titled "{paper_title}" using the {bibtex_style} style.

The BibTeX file should include all references cited in the paper, formatted according to the {bibtex_style} style.

Consider:
1. BibTeX Entry Types
   - @article for journal articles
   - @inproceedings for conference papers
   - @book for books
   - @incollection for book chapters
   - @techreport for technical reports
   - @misc for other sources

2. Required Fields
   - author: Author names in "Last, First" format
   - title: Title of the work
   - journal/booktitle: Publication venue
   - year: Publication year
   - volume: Volume number
   - number: Issue number
   - pages: Page range
   - doi: Digital Object Identifier
   - url: URL if available

3. BibTeX Formatting
   - Proper key generation (e.g., author:year)
   - Consistent formatting
   - Proper escaping of special characters
   - Complete information for each entry

4. Special Cases
   - Multiple authors
   - Organization authors
   - Missing information
   - Non-English sources

Format the output as a complete BibTeX file with all necessary entries.
""" 