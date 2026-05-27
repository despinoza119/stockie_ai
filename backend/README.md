# Stockie AI — Backend

FastAPI service for market data, fundamental/technical analysis, and recommendations.

> See the root [`README.md`](../README.md) for full-stack quick-start instructions.

---

## Stack

- **Python 3.12** managed by [uv](https://docs.astral.sh/uv/)
- **FastAPI** + **Uvicorn** — async HTTP server
- **SQLAlchemy 2 (async)** + **asyncpg** — database ORM and driver
- **Alembic** — schema migrations
- **Pydantic Settings** — typed config loaded from `.env`
- **structlog** — structured logging (pretty in dev, JSON in prod)

---

## Setup

```bash
# From the backend/ directory

# Install all deps including dev tools
uv sync --extra dev

# Copy and edit the env file
cp .env.example .env
```

The database and Redis must be running before starting the server:

```bash
cd ../infra && docker compose up -d
```

---

## Running the server

```bash
# Hot-reload dev server  →  http://localhost:8000
uv run uvicorn app.main:app --reload

# OpenAPI docs  →  http://localhost:8000/docs
# OpenAPI JSON  →  http://localhost:8000/openapi.json  (used by frontend codegen)
```

---

## Environment variables

All config is in `.env` (copy from `.env.example`). Never commit `.env`.

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | `development` / `staging` / `production` |
| `APP_VERSION` | `0.1.0` | Reported by `GET /health` |
| `APP_DEBUG` | `true` | Enables debug-level logging |
| `DATABASE_URL` | `postgresql+asyncpg://stockie:stockie@localhost:5432/stockie_ai` | Must use `asyncpg` driver |
| `REDIS_URL` | `redis://localhost:6379/0` | Cache and Celery broker (Sprint 2+) |

**Rule:** Always use `get_settings()` to read config. Never instantiate `AppSettings` directly.

---

## Migrations

```bash
# Apply all pending migrations
uv run alembic upgrade head

# Roll back one revision
uv run alembic downgrade -1

# Generate a new revision after editing ORM models
uv run alembic revision --autogenerate -m "<description>"
```

Alembic reads `DATABASE_URL` from `AppSettings` — never from `alembic.ini`.

---

## Tests

```bash
# Run all tests with verbose output
uv run pytest -v

# Run a single file
uv run pytest tests/test_health.py -v
```

Tests use FastAPI's in-process `TestClient` — no live database required for the current suite.

---

## Linting

```bash
uv run ruff check .          # import sorting + lint rules
uv run black --check .       # code formatting
uv run mypy app/             # type checking
```

Or run everything at once via pre-commit (from the repo root):

```bash
pre-commit run --all-files
```

---

## Project layout

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── health.py      # GET /health
│   ├── core/
│   │   ├── config.py          # AppSettings (Pydantic BaseSettings)
│   │   ├── db.py              # async engine + get_db() dependency
│   │   └── logging.py         # configure_logging()
│   ├── models/
│   │   └── base.py            # DeclarativeBase — all ORM models inherit this
│   └── main.py                # create_app() factory
├── alembic/
│   ├── env.py                 # async migration runner
│   └── versions/              # migration files
├── tests/
│   ├── conftest.py            # shared fixtures
│   └── test_health.py
├── .env.example
├── alembic.ini
└── pyproject.toml
```
