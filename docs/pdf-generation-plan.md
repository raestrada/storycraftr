# PDF Generation Refactor Plan

## Objectives
- Produce predictable, high-quality PDFs from StoryCraftr markdown without requiring LaTeX, Pandoc, or external tooling that complicates installation.
- Simplify the generation stack so it can run in common environments (pipx, CI, containers) with minimal dependencies.
- Maintain stylistic control (fonts, headings, table of contents) directly from Python.

## Current Pain Points
1. **Pandoc/LaTeX dependency** – Requires system packages, varies by OS, and breaks in isolated environments.
2. **Inconsistent output** – Layout or fonts shift depending on local LaTeX installs; users report unpredictable PDF rendering.
3. **Limited customization** – Styling tweaks require custom templates or LaTeX knowledge, slowing iteration.

## Target Approach
- Adopt a pure-Python Markdown → PDF pipeline using a maintained library (initial candidate: [`markdown-pdf`](https://pypi.org/project/markdown-pdf/)).
- Wrap the renderer so StoryCraftr controls document options (title page, metadata, optional cover art) through a simple config.
- Keep the output consistent across platforms by bundling CSS/themes alongside the renderer.

## Evaluation of Libraries
| Library | Pros | Cons | Decision |
| ------- | ---- | ---- | -------- |
| `markdown-pdf` | Actively maintained, pure Python, supports CSS themes, simple API | Requires evaluation of font embedding, image support | **Preferred** |
| `weasyprint` | Powerful CSS engine | Pulls in Cairo/Pango system deps | Consider if we need advanced layout |
| `reportlab` | Full control, PDF native | Manual layout (no Markdown parser) | Not ideal |

## Workstreams
1. **Prototype Renderer**
   - Create `storycraftr/pdf/renderer.py` using `markdown-pdf`.
   - Test with sample chapters (headings, tables, images, code blocks).
   - Bundle default CSS (matching StoryCraftr brand) in `storycraftr/pdf/themes/`.
2. **CLI Integration**
   - Update `storycraftr/cmd/story/publish.py` (and paper equivalent) to call the new renderer.
   - Provide CLI flags for theme selection, cover inclusion, frontmatter metadata.
3. **Configuration & Templates**
   - Allow per-project overrides (e.g., `<book>/pdf-theme.css`).
   - Document how authors can add CSS tweaks or custom fonts.
4. **Testing & QA**
   - Add unit tests verifying renderer is invoked and outputs a PDF.
   - Create integration tests comparing output size/checksum for known samples.
   - Manual regression for multi-language content and large chapters.
5. **Docs & Migration**
   - Document the new pipeline in `docs/pdf.md` (requirements, customization).
   - Update README / Getting Started instructions to reflect pure-Python flow.
   - Note Pandoc/LaTeX is no longer required (or only optional for legacy flows).

## Risks & Mitigations
- **Rendering Fidelity**: Markdown → PDF engines vary; test complex constructs early (tables, blockquotes, images).
  - Mitigation: Maintain sample Markdown fixtures and compare outputs during CI.
- **CSS Complexity**: Authors may want heavy customization.
  - Mitigation: Provide layered themes (base + optional overrides) and document best practices.
- **Binary Assets**: Ensure `markdown-pdf` handles embedded images/fonts; otherwise add post-processing step.

## Success Metrics
- PDF generation works via `poetry run storycraftr publish pdf ...` on a clean pipx install (no Pandoc/LaTeX).
- Automated tests validate output is created and is non-empty for sample books.
- Users report consistent rendering across macOS/Linux/Windows (tracked via issue reduction).
