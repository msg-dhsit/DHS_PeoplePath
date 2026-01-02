# PeoplePath Resource Management Portal

A minimalistic, end-to-end portal for resources, timesheets, AI assistance, and Microsoft Teams integration. Delivered as a monorepo with FastAPI backend, Next.js frontend, and a Teams bot/manifest.

## Prerequisites
- Docker and Docker Compose
- Node.js 18+ and npm (for frontend dev without Docker)
- Python 3.11+ (for backend dev without Docker)

## Quickstart (Docker Compose)
1. Copy `.env.example` to `.env` and adjust values if needed.
2. Run `docker-compose up --build`.
3. API available at `http://localhost:8000`, frontend at `http://localhost:3000`.
4. Apply migrations: `docker-compose exec backend alembic upgrade head`.
5. Seed sample data: `docker-compose exec backend python -m app.seed.seed_data`.

### Sample users
- admin@example.com / admin123
- manager@example.com / manager123
- hr@example.com / hr123
- resource@example.com / resource123

## Backend (FastAPI)
- Location: `/backend`
- Run locally: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload`
- Tests: `cd backend && pytest`
- Key modules:
  - `app/main.py`: FastAPI entrypoint
  - `app/routers/*`: domain routers (auth, resources, dashboard, timesheets, ai, teams)
  - `app/services/*`: business logic (AI provider abstraction, timesheet workflows, dashboard aggregation)
  - `app/models/models.py`: SQLAlchemy models
  - `alembic/versions/0001_initial.py`: migration defining schema in the spec

## Frontend (Next.js + Tailwind)
- Location: `/frontend`
- Run locally: `cd frontend && npm install && npm run dev`
- Env: set `NEXT_PUBLIC_API_URL` to the backend URL.
- Pages: dashboard, resources list/detail, timesheet with AI suggest modal, approvals queue, login page.
- Tests: `cd frontend && npm test`.

## AI Providers
- Provider-agnostic design with mock provider default.
- Configure Azure OpenAI by setting `AI_PROVIDER=azure`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_DEPLOYMENT`.
- Safety: suggestions require explicit confirmation token when applying.

## Microsoft Teams
- Bot located in `/teams/server.js` using Bot Framework.
- Manifest in `/teams/manifest/manifest.json` defines tab (points to frontend) and bot commands.
- Run bot: `cd teams && npm install && npm start` (port 3978).
- Update manifest URLs with your tunneling endpoint (e.g., `https://<ngrok>.ngrok.io`).

## Database
- PostgreSQL by default (see `DATABASE_URL`).
- Apply migrations using Alembic.

## Extending Azure OpenAI & Graph integration
- Implement `AzureOpenAiProvider` credentials in env to enable real completions.
- For Microsoft Graph calendar enrichment, add a background fetcher that stores sanitized event summaries, filter sensitive terms, and pass into the AI prompt payload before calling the provider.

