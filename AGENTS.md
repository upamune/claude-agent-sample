# Repository Guidelines

## Project Structure & Module Organization
- `main.py` hosts the calculator agent entrypoint and shows the canonical tool wiring plus Rich console UX.
- `examples/` offers runnable agent snippets for hooks, streaming, and MCP integrations.
- `docs/` mirrors upstream Anthropic guidance; treat it as reference material rather than executable code.
- `scripts/fetch_doc.py` is a uv-powered helper for importing external documentation.
- Configuration lives in `pyproject.toml`, `uv.lock`, and `mise.toml`; update these together when dependencies change.

## Build, Test, and Development Commands
- `uv sync` installs or updates Python 3.12 dependencies declared in `pyproject.toml`/`uv.lock`.
- `mise run agent` starts the interactive calculator agent via `uv run ./main.py`.
- `mise run format` applies `ruff format` to the entire workspace.
- `mise run lint` runs `ruff check` with autofix; use before committing to catch typing and style issues early.
- For ad-hoc runs, prefer `uv run <script.py>` to stay inside the managed virtual environment.

## Coding Style & Naming Conventions
- Python code follows 4-space indentation, type-annotated function signatures, and descriptive async tool helpers (`add`, `sub`, etc.).
- Keep user-facing strings friendly and localized when helpful; the prompt currently mixes Japanese guidance with emoji cues.
- Use `ruff check --fix` for linting and `ruff format` for layout; no separate `black` or `isort` runs.
- New MCP tools should use snake_case names and include concise docstrings so they render well in Rich panels.

## Testing Guidelines
- There is no formal test suite yet; place new tests under `tests/` and target `pytest` for consistency with the Python ecosystem.
- Favor deterministic agent transcripts: simulate tool calls with fixtures instead of live API hits.
- Run `uv run pytest` (or `mise run pytest` once added) to validate tool registration paths.

## Commit & Pull Request Guidelines
- Use imperative, English commit subjects (e.g., `Add retry guard for MCP server startup`).
- Reference issue numbers or links when applicable, and summarize visible changes (CLI screenshots, transcript snippets) in the PR description.
- Confirm `mise run format` and `mise run lint` are clean before requesting review; mention any skipped checks explicitly.

## Agent Setup & Configuration
- Export `ANTHROPIC_API_KEY` (and any MCP service credentials) before running the agent; `ClaudeSDKClient` reads them from the environment.
- Never commit secrets—use `.env` files ignored by git or rely on your shell profile for local development.
