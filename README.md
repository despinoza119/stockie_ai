# Stockie AI

AI-powered stock analysis and recommendations for US equities and ETFs.

> **Status:** Sprint 0 — Scaffolding complete. Full stack runs locally; no business logic yet.

---

## What it is

Stockie AI gives retail investors a clear, multi-dimensional view of any US stock or ETF:

- **Fundamental analysis** — valuation ratios, quality metrics, growth CAGRs, simplified DCF
- **Technical analysis** — indicators, support/resistance, trend scoring
- **News & sentiment** — FinBERT-scored article feed with rolling sentiment
- **Recommendations** — rules-based buy/hold/sell verdicts across short, mid, and long horizons

---

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy (async), Alembic |
| Database | PostgreSQL 16 + TimescaleDB |
| Cache / broker | Redis 7 |
| Frontend | Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui |
| Infrastructure | Docker Compose (local dev) |
| CI | GitHub Actions |

---

## Repo layout

```
stockie_ai/
├── backend/          # FastAPI app — API, services, models, scoring
│   ├── app/
│   │   ├── api/      # FastAPI routers
│   │   ├── core/     # config, db, logging
│   │   ├── models/   # SQLAlchemy ORM models
│   │   └── main.py
│   └── tests/
├── frontend/         # Next.js app — UI, components, typed API client
│   ├── app/
│   ├── components/
│   └── lib/api/      # openapi-typescript generated types + fetch client
├── infra/            # docker-compose.yml (TimescaleDB + Redis)
├── docs/             # PLANNING_features.md, PLANNING_tasks.md
└── .github/
    └── workflows/ci.yml
```

---

## Quick start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for the database + Redis)
- [uv](https://docs.astral.sh/uv/) — Python package manager
- Node.js 20+ and npm

### First-time setup

```bash
# 1. Clone
git clone <repo-url>
cd stockie_ai

# 2. Copy env files
cp backend/.env.example backend/.env
cp infra/.env.example infra/.env
cp frontend/.env.example frontend/.env.local

# 3. Install backend deps
cd backend && uv sync --extra dev && cd ..

# 4. Install frontend deps
cd frontend && npm install && cd ..

# 5. Install pre-commit hooks
pre-commit install
```

### Daily dev

```bash
# Terminal 1 — infrastructure (DB + Redis)
cd infra && docker compose up -d

# Terminal 2 — backend  →  http://localhost:8000
cd backend && uv run uvicorn app.main:app --reload

# Terminal 3 — frontend  →  http://localhost:3000
cd frontend && npm run dev
```

Visit `http://localhost:3000` — the landing page calls `GET /health` and shows live backend status.

### Run migrations

```bash
# Apply all pending migrations (DB must be running)
cd backend && uv run alembic upgrade head

# Generate a new migration after changing ORM models
cd backend && uv run alembic revision --autogenerate -m "<description>"
```

### Tests and linting

```bash
# Backend
cd backend
uv run pytest -v
uv run ruff check .
uv run black --check .
uv run mypy app/

# Frontend
cd frontend
npm run lint
npm run format:check
npx tsc --noEmit

# Pre-commit (runs ruff + black + mypy on staged files)
pre-commit run --all-files
```

---

## Team

| Handle | Responsibilities |
|--------|----------------|
| `@bvela` | Backend — Python, FastAPI, data providers, scoring, migrations |
| `@despinoza` | Frontend — Next.js, React, charts, UX |

See [`docs/PLANNING_tasks.md`](docs/PLANNING_tasks.md) for the full sprint backlog and [`docs/PLANNING_features.md`](docs/PLANNING_features.md) for the product spec.

---

## Contributing

1. Branch from `main`: `feat/<short-desc>`, `fix/<short-desc>`, `chore/<short-desc>`
2. Open a PR — the template will guide you through the checklist
3. CI must be green before merge; squash-merge preferred
