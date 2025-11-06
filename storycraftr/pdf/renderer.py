from __future__ import annotations

from pathlib import Path
from typing import Optional

from typing import Iterable, Tuple

from markdown_pdf import MarkdownPdf, Section

THEMES_DIR = Path(__file__).resolve().parent / "themes"


def load_theme(theme_name: Optional[str] = None) -> str:
    name = (theme_name or "classic").strip()
    path = THEMES_DIR / f"{name}.css"
    if not path.exists():
        if theme_name:
            raise FileNotFoundError(f"Theme '{theme_name}' not found at {path}")
        return ""
    return path.read_text(encoding="utf-8")


def build_theme_css(book_path: str, theme_name: Optional[str] = None) -> str:
    css = load_theme(theme_name)
    override_path = Path(book_path) / "pdf-theme.css"
    if override_path.exists():
        css += "\n" + override_path.read_text(encoding="utf-8")
    return css


SectionSpec = Tuple[str, bool]


def render_markdown_to_pdf(
    sections: Iterable[SectionSpec],
    output_path: Path,
    *,
    assets_root: Path,
    css: str,
    toc_level: int = 4,
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf = MarkdownPdf(toc_level=toc_level)
    for text, toc in sections:
        section = Section(text, toc=toc, root=str(assets_root))
        pdf.add_section(section, user_css=css or None)

    pdf.save(str(output_path))
    return output_path
