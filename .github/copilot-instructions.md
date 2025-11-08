## Purpose
Repository-specific guidance for AI coding agents to be productive working on the RAG Chatbot project (FastAPI backend, Agno agents, NiceGUI UI).

## Project Context
This project implements a minimal RAG Chatbot with:
- **FastAPI** for backend streaming endpoints
- **Agno** for agent orchestration, session, and history
- **NiceGUI** for a thin UI layer
- **OpenAI** as the LLM provider (API key via `.env`)

Key features:
- Streaming responses via FastAPI
- PDF upload & parsing
- Async status signals in the UI
- Tests using pytest and pytest-check

## Repository Structure
```
src/
  backend/    # FastAPI endpoints
  agent/      # Agno orchestration
  ui/         # NiceGUI views
  parsing/    # PDF parsing logic
tests/
  unit/
  integration/
  data/       # sample PDFs
pyproject.toml
requirements.txt
.env.example
README.md
```

## Coding Standards
- Python 3.13+, modern typing (`list[str]`, `str | None`)
- Use **Pydantic models** for structured inputs/outputs (no raw dicts)
- Format with **Ruff + Black**; lint on save or CI
- Run **mypy** regularly; prefer explicit types on public functions
- Keep functions small and single-responsibility

## Testing Guidelines
- Framework: **pytest + pytest-check**
- Unit tests per module: backend, agent, parsing
- Integration tests: streaming endpoints + PDF upload flows
- Place real PDFs in `tests/data/` for deterministic runs
- Fail loudly—do not swallow errors with broad try/except

## Architecture Reminders
- Clear separation of concerns:
  - `backend` → FastAPI endpoints/streaming
  - `agent` → Agno orchestration/session/history
  - `ui` → NiceGUI views
  - `parsing` → PDF loaders/parsers
- Prefer Agno’s built-in primitives; only add custom abstractions when justified and documented

## Productivity Notes
- Scaffold FastAPI endpoints and streaming patterns (async generators + StreamingResponse)
- Suggest Agno agent wiring (session creation, call patterns)
- Generate pytest skeletons (happy-path + edge cases)
- Include docstrings and full type hints on public functions
- Propose async patterns for streaming and non-blocking UI

## Useful Commands
```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt  # install formatting/linting/testing tools

# format & lint
ruff check . && black .

# type check
mypy .

# run tests
pytest -q
```

- Configure CI to run linting, type checks, and tests
- Keep this file updated as project structure or standards evolve

## Commit & Branching Guidelines

- **Commit Frequently**: Remember the developer to make many small, working commits. Each commit should represent a single, testable unit of functionality (feature, fix, docs, test). Avoid one large "final" commit.
- **Branching Strategy**:
  - For this project, a **single branch (`main`) with multiple commits** is recommended to keep history simple and transparent.
  - Optional: Suggest short-lived branches for larger changes if the feature is longer enough
  Suggested prefixes:
    - `feature/...` (new functionality)
    - `fix/...` (bug fixes)
    - `chore/...` (tooling, config, dependencies)
    - `docs/...` (documentation updates)
    - `test/...` (testing improvements)
  - Examples: `feature/streaming-sse`, `fix/pdf-parser`.

- **Commit Style**: Follow [Conventional Commits] - <a href="https://www.conventionalcommits.org/" target="_blank" rel="noopener noreferrer">Conventional Commits</a> for clarity:
  - `feat:` → new feature
  - `fix:` → bug fix
  - `chore:` → tooling/config
  - `docs:` → documentation
  - `test:` → test-related changes
  - Include a short scope when helpful: `feat(parsing): add pdf extractor`.

### Pre-Commit Checklist
Before committing, run:
- **Format & Lint**: `ruff check .` and `black .` (or via pre-commit hooks).
- **Type Check**: `mypy .` (or at least on changed modules).
- **Tests**: Run affected tests: `pytest tests/unit/... -q`.
- **Secrets**: Verify no secrets are committed; update `README`/`CHANGELOG` if behavior changes.

### Example Workflow (Windows CMD)
```cmd
git checkout -b feature/add-pdf-parser
git add src/parsing/pdf_extractor.py tests/parsing/test_extractor.py
git commit -m "feat(parsing): add pdf text extractor" -m "Add a pdf extractor wrapper using pdfplumber. Includes unit tests and docs."
git push -u origin feature/add-pdf-parser

```

Commit message template (recommended):

Header: `<type>(<scope>): short summary`  (<= 50 chars)

Body: one or two paragraphs explaining what and why, plus any migration steps or other notes.

Example:

```
feat(parsing): add PDF extractor wrapper

Add a small wrapper around pdfplumber that returns a list[str] of page texts
so parsing is easy to mock in tests. Add unit tests under tests/parsing/.

No breaking changes.
```

For every feature or bugfix, suggest a matching test file and a commit message that can be used. Unless a strict commit format (Conventional Commits) is preferred.

---
