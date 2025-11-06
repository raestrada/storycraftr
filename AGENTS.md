# Repository Guidelines

## Project Structure & Module Organization
StoryCraftr currently ships a Python CLI (the VS Code extension is being rebuilt). Python sources live in `storycraftr/` (agents, CLI entrypoints, prompts, templates) with tests under `tests/` partitioned into `unit/` and `integration/`. Shared documentation belongs in `docs/`, while runnable samples and starter outlines live in `examples/`. Treat `behavior.txt` as the canonical agent contract when adjusting automated behaviors.

## Build, Test, and Development Commands
- Python: `poetry install` bootstraps dependencies; `poetry run storycraftr --help` validates the CLI loads; `poetry run pytest` runs the full suite. Use `poetry run pre-commit run --all-files` before pushing.
- Extension: (coming soon) — after the JSONL event stream stabilizes, a new VS Code extension will be published with its own build instructions.

## Coding Style & Naming Conventions
Python code is formatted with Black (88-character lines) and linted via Bandit and detect-secrets through pre-commit; prefer snake_case for functions and lower-case package names mirroring directory structure (for example, `storycraftr.agent.*`). Keep prompts and template YAMLs declarative, mirroring existing filenames.

## Testing Guidelines
Place new Python tests under `tests/unit/` or `tests/integration/` using `test_<feature>.py` naming; assert CLI flows with fixtures in `tests/utils/`. When modifying agents, cover both deterministic parsing helpers and end-to-end flows. Aim to keep pytest coverage from regressing; add regression cases for bugs alongside fixes.

## Commit & Pull Request Guidelines
Adopt Conventional Commit prefixes observed in history (`feat(agents):`, `fix(cli):`, `sec:`) and keep messages imperative and concise. Each PR should describe the user-facing change, list manual or automated test runs, and mention any docs, templates, or prompts updated. Link GitHub issues where applicable and attach screenshots or CLI transcripts when changing UX.

## Security & Configuration Tips
Never commit API keys or `.env` files; the CLI picks up provider secrets (for example, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, `OLLAMA_API_KEY`) from environment variables or the `~/.storycraftr/` folder. Run `poetry run detect-secrets scan` or rely on pre-commit hooks after touching config files. Review `SECURITY.md` when shipping authentication or networking changes, and call out potential token usage impacts in release notes.
