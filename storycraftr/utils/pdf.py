from __future__ import annotations

from pathlib import Path

from rich.console import Console

from storycraftr.pdf import build_theme_css, render_markdown_to_pdf
from storycraftr.utils.core import load_book_config
from storycraftr.utils.markdown import consolidate_book_md

console = Console()


def _read_optional_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _format_cover(config, cover_md: str) -> str:
    authors = getattr(config, "authors", None) or []
    if not authors and getattr(config, "default_author", None):
        authors = [config.default_author]
    author_line = ", ".join(authors) if authors else "Anonymous"

    page_break = '\n\n<div style="page-break-after: always;"></div>\n'
    content = (
        f"# {config.book_name}\n\n"
        f"### {author_line}\n\n"
        f"_{getattr(config, 'genre', '').title()}_\n"
    )
    if cover_md:
        content += f"\n{cover_md.strip()}\n"
    return content.strip() + page_break


def _format_license(config, book_path: Path) -> str:
    license_text = (
        getattr(config, "license", "All rights reserved.") or "All rights reserved."
    )
    license_file = book_path / "LICENSE"
    if license_file.exists():
        license_text += "\n\n" + license_file.read_text(encoding="utf-8").strip()
    page_break = '\n\n<div style="page-break-after: always;"></div>\n'
    return f"## Licencia\n\n{license_text.strip()}" + page_break


def _format_back_cover(back_md: str) -> str:
    if not back_md.strip():
        return ""
    return f"## Contraportada\n\n{back_md.strip()}"


def to_pdf(
    book_path: str,
    primary_language: str,
    translate: str | None = None,
    theme: str | None = None,
) -> str:
    console.print(
        f"[bold]Generating PDF for[/bold] [cyan]{book_path}[/cyan] (language: {primary_language})"
    )

    config = load_book_config(book_path)
    book_root = Path(book_path)
    chapters_dir = book_root / "chapters"

    body_markdown_path = consolidate_book_md(
        book_path,
        primary_language,
        translate,
        include_cover=False,
        include_back_matter=False,
    )
    body_text = Path(body_markdown_path).read_text(encoding="utf-8")

    cover_md = _read_optional_markdown(chapters_dir / "cover.md")
    back_md = _read_optional_markdown(chapters_dir / "back-cover.md")

    sections = [
        (_format_cover(config, cover_md), False),
        (_format_license(config, book_root), False),
        (body_text, True),
    ]

    back_section = _format_back_cover(back_md)
    if back_section:
        sections.append((back_section, False))

    output_pdf_path = Path(body_markdown_path).with_suffix(".pdf")
    css = build_theme_css(book_path, theme)
    render_markdown_to_pdf(
        sections,
        output_pdf_path,
        assets_root=book_root,
        css=css,
    )

    console.print(f"[green]PDF written to[/green] {output_pdf_path}")
    return str(output_pdf_path)
