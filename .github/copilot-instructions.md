# Copilot Workspace Instructions

**Soc Ops** — Social Bingo game for in-person mixers. Python 3.13+, FastAPI, Jinja2, HTMX.

## Commands

```bash
uv sync                                          # Install dependencies
uv run uvicorn app.main:app --reload --port 8000 # Start dev server
uv run pytest                                    # Run tests
uv run ruff check .                              # Lint
```

> Use a **full browser** at http://localhost:8000 — not the VS Code Simple Browser.

## Architecture

```
app/
├── main.py          # FastAPI routes & HTMX endpoints (always return HTML, not JSON)
├── game_service.py  # GameSession dataclass — mutable session state
├── game_logic.py    # Pure functions: generate_board(), toggle_square(), check_bingo()
├── models.py        # Frozen Pydantic models: GameState, BingoSquareData, BingoLine
├── data.py          # QUESTIONS list (must have exactly 24 entries)
├── templates/       # Jinja2 templates + components/
└── static/css/app.css  # Custom utility classes (see css-utilities.instructions.md)
tests/
├── test_api.py         # Endpoint tests (httpx TestClient)
└── test_game_logic.py  # Unit tests
```

## Conventions

- `snake_case`, type hints on all functions
- Pydantic models are **frozen** — use `.model_copy(update={...})` to mutate
- State is server-side only; sessions via signed cookie (`itsdangerous`)
- HTMX routes must return `HTMLResponse`/template fragments — never JSON

## Checklist

- [ ] `uv run ruff check .` — lint passes
- [ ] `uv run uvicorn app.main:app` — app starts without errors
- [ ] `uv run pytest` — all 25 tests pass
- [ ] Type hints on all new functions, no unused imports
