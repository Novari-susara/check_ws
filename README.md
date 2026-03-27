# Soc Ops

**Social Bingo for in-person mixers.** Players find colleagues who match fun prompts — first to get 5 in a row wins!

🎮 **[Play the Game](https://madebygps.github.io/vscode-github-copilot-agent-lab/)** • 📚 **[View Lab Guide](https://madebygps.github.io/vscode-github-copilot-agent-lab/docs/)**

---

## 📚 Lab Guide

| Part | Title |
|------|-------|
| [**00**](https://madebygps.github.io/vscode-github-copilot-agent-lab/docs/step.html?step=00-overview) | Overview & Checklist |
| [**01**](https://madebygps.github.io/vscode-github-copilot-agent-lab/docs/step.html?step=01-setup) | Setup & Context Engineering |
| [**02**](https://madebygps.github.io/vscode-github-copilot-agent-lab/docs/step.html?step=02-design) | Design-First Frontend |
| [**03**](https://madebygps.github.io/vscode-github-copilot-agent-lab/docs/step.html?step=03-quiz-master) | Custom Quiz Master |
| [**04**](https://madebygps.github.io/vscode-github-copilot-agent-lab/docs/step.html?step=04-multi-agent) | Multi-Agent Development |

> 📝 Lab guides are also available in the [`.lab/`](.lab/) folder for offline reading.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) (Python 3.13+) |
| Templating | [Jinja2](https://jinja.palletsprojects.com/) |
| Interactivity | [HTMX](https://htmx.org/) |
| Sessions | Signed cookies via [itsdangerous](https://itsdangerous.palletsprojects.com/) |
| Package manager | [uv](https://docs.astral.sh/uv/) |
| Linting | [Ruff](https://docs.astral.sh/ruff/) |

---

## Architecture

```
app/
├── main.py          # FastAPI routes & HTMX endpoints (returns HTML fragments)
├── game_service.py  # GameSession dataclass — server-side session state
├── game_logic.py    # Pure functions: generate_board(), toggle_square(), check_bingo()
├── models.py        # Frozen Pydantic models: GameState, BingoSquareData, BingoLine
├── data.py          # QUESTIONS list (exactly 24 entries for a 5×5 board)
├── templates/       # Jinja2 templates and HTMX partials
└── static/          # CSS utilities
tests/
├── test_api.py      # Endpoint tests (httpx TestClient)
└── test_game_logic.py  # Unit tests for pure game logic
```

**Key design decisions:**
- All state is server-side; the browser holds only a signed session cookie.
- HTMX endpoints always return HTML — never JSON.
- Pydantic models are frozen; use `.model_copy(update={...})` to produce new state.

---

## Prerequisites

- [Python 3.13+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) package manager

## Quick Start

```bash
# 1. Install dependencies
uv sync

# 2. Start the development server
uv run uvicorn app.main:app --reload --port 8000
```

Then open <http://localhost:8000> in your browser.

## Development

### Run tests

```bash
uv run pytest
```

### Lint & format

```bash
uv run ruff check .   # check for lint errors
uv run ruff format .  # auto-format code
```

### Checklist before committing

- [ ] `uv run ruff check .` passes with no errors
- [ ] `uv run pytest` — all tests pass
- [ ] Type hints on all new functions, no unused imports

---

Deploys automatically to GitHub Pages on push to `main`.
