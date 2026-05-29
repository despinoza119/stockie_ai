# Stockie AI — Cold-Start Context

> **For Claude:** Read this file at the start of every conversation before taking any action.
> **Update rule:** After every completed sprint task, mark it ✅ here and update the "What has been built" table.
> Full backlog → `docs/PLANNING_tasks.md` | Feature plan → `docs/PLANNING_features.md`

---

## Active sprint: Sprint 0 — Scaffolding (Weeks 1–2)

**Goal:** Full stack running locally. No business logic yet.

### Checklist

| # | Status | Owner | Task |
|---|--------|-------|------|
| 1 | ✅ | @bvela | Repo, CLAUDE.md, PLANNING docs, .gitignore, LICENSE |
| 2 | ✅ | @bvela | FastAPI + Pydantic Settings + `/health` endpoint + structlog |
| 3 | ✅ | @bvela | `docker-compose.yml` with TimescaleDB (pg16) + Redis |
| 4 | ✅ | @bvela | Alembic migrations configured + empty initial revision |
| 5 | ✅ | @bvela | Pre-commit (ruff + black + mypy) + pytest skeleton |
| 6 | ✅ | @despinoza | Next.js 14 + TypeScript + Tailwind initialized |
| 7 | ✅ | @despinoza | ESLint + Prettier + shadcn/ui component library |
| 8 | ✅ | @despinoza | Typed API client (`openapi-typescript`) |
| 9 | ✅ | @despinoza | Placeholder landing page calling `/health` |
| 10 | ✅ | @both | GitHub Actions CI — lint + tests on every PR |
| 11 | ✅ | @both | Issue/PR template + branch naming documented |
| 12 | ✅ | @both | End-to-end smoke test (`docker compose up` → frontend reads backend) |

---

## What has been built

### Backend (`backend/`)

| File | Purpose |
|------|---------|
| `app/core/config.py` | `AppSettings` (Pydantic BaseSettings); `get_settings()` singleton |
| `app/core/db.py` | Async engine, `AsyncSessionLocal`, `get_db()` FastAPI dependency |
| `app/core/logging.py` | `configure_logging()` — pretty in dev, JSON in prod (structlog) |
| `app/models/base.py` | `DeclarativeBase` — all future ORM models inherit from this |
| `app/api/v1/health.py` | `GET /health` → `{status, version, environment, timestamp}` |
| `app/main.py` | `create_app()` factory; lifespan hooks; router registration |
| `tests/conftest.py` | Shared fixtures: `client` (sync `TestClient`), `async_client` (httpx) |
| `tests/test_health.py` | 5 tests covering `/health` shape and invariants |
| `alembic/env.py` | Async migration runner; reads `DATABASE_URL` from `AppSettings` |
| `alembic/versions/20260522_…_initial.py` | Empty initial revision |
| `pyproject.toml` | uv project; runtime + dev deps; ruff/black/mypy/pytest config |

**Runtime deps:** `fastapi`, `uvicorn[standard]`, `pydantic-settings`, `structlog`, `sqlalchemy[asyncio]`, `asyncpg`, `alembic`
**Dev deps:** `pytest`, `pytest-asyncio`, `httpx`, `pre-commit`, `ruff`, `black`, `mypy`

### Frontend (`frontend/`)

| File | Purpose |
|------|---------|
| `app/layout.tsx` | Root layout — Geist font, Stockie AI metadata |
| `app/page.tsx` | Sprint 0 placeholder page |
| `components/ui/button.tsx` | shadcn/ui Button component (base-ui primitive + CVA variants) |
| `lib/utils.ts` | `cn()` helper — Tailwind class merge utility |
| `lib/api/schema.d.ts` | Auto-generated TypeScript types from `/openapi.json` (run `npm run generate`) |
| `lib/api/client.ts` | `apiClient` singleton — openapi-fetch typed against `paths` |
| `lib/api/index.ts` | Barrel re-export: `apiClient`, `components`, `paths`, `operations` |
| `components/health-status.tsx` | Async server component: fetches `/health`, renders status card + skeleton |
| `types/css.d.ts` | Ambient CSS module declaration (silences IDE false-positive on CSS side-effect imports) |

**Stack:** Next.js 14.2 (App Router) + TypeScript + Tailwind CSS + ESLint + Prettier + shadcn/ui

### Infrastructure (`infra/`)

| File | Purpose |
|------|---------|
| `docker-compose.yml` | `stockie_db` (TimescaleDB pg16) + `stockie_redis` (Redis 7 Alpine) |
| `postgres/init/01_extensions.sql` | `CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE` |
| `.env.example` | Postgres + Redis credentials/ports with dev defaults |

### Root

| File | Purpose |
|------|---------|
| `.pre-commit-config.yaml` | trailing-whitespace, EOF, YAML/TOML, ruff, black, mypy (all scoped to `backend/`) |

---

## How to run

```bash
# First-time setup
cp backend/.env.example backend/.env
cp infra/.env.example infra/.env
cd backend && uv venv --python 3.12 && uv pip install -e ".[dev]"
pre-commit install           # from repo root

# Daily dev
cd infra && docker compose up -d                            # TimescaleDB + Redis
cd backend && uv run uvicorn app.main:app --reload          # http://localhost:8000
cd frontend && npm run dev                                  # http://localhost:3000

# Tests / linting
cd backend && uv run pytest -v
pre-commit run --all-files

# Migrations (DB must be running)
cd backend && uv run alembic upgrade head
cd backend && uv run alembic revision --autogenerate -m "<message>"
```

---

## Locked architectural decisions

| Decision | Detail |
|----------|--------|
| Package managers | **uv** (backend), **npm** (frontend) |
| DB driver | Always `postgresql+asyncpg://…` — never sync `postgresql://` |
| Config | Always `get_settings()` — never instantiate `AppSettings` directly |
| Alembic URL | Read from `AppSettings` in `env.py` — never hardcode in `alembic.ini` |
| File headers | Every authored file gets the JSDoc/docstring header (CLAUDE.md §File-Level Documentation) |
| Recommendation engine | Rules-based for MVP; ML/LLM is post-MVP |
| Monetization | None during the build phase |
| Launch market | US equities + ETFs first; BVL (Peru) deferred to v1.1 |

---

## Team split

- **@bvela (Bryan)** → backend: Python, FastAPI, data, scoring, migrations
- **@despinoza** → frontend: Next.js, React, charts, UX
- **@both** → tasks requiring a pair session

---

## Next sprint preview

**Sprint 1 (Weeks 3–4):** `MarketDataProvider` + `FundamentalsProvider` abstract interfaces, `YFinanceProvider`, `Ticker` / `PriceBar` / `Fundamentals` SQLAlchemy models, `GET /tickers/search?q=`, ticker search UI.
