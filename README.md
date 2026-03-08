# EditPro Ultra API

EditPro Ultra is a **workable FastAPI backend** for an editing product. It includes a curated 40-feature catalog plus APIs for filtering, health checks, and rollout planning.

## What this app provides

- Feature catalog endpoint with 40 advanced editing capabilities.
- Category/tier filtering to support search and dashboards.
- Feature summary counts by category and plan tier.
- Goal-based rollout planner that returns phased milestones.
- Health and metadata endpoints for deployment checks.

## Quick start (local Python)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

- API: `http://127.0.0.1:8000`
- Docs: `http://127.0.0.1:8000/docs`

## Quick start (Docker)

```bash
docker compose up --build
```

The backend runs on `http://127.0.0.1:8000`.

## API endpoints

- `GET /` – app metadata and feature count
- `GET /health` – runtime health status
- `GET /features` – list all features
- `GET /features?category=AI&tier=Ultra` – filter features
- `GET /features/summary` – category/tier counts
- `GET /features/{feature_id}` – fetch one feature
- `POST /plans/generate` – generate a phased rollout plan

Planner goals are validated; use one or more of: `speed`, `quality`, `ai`, `collaboration`, `social`.

Example request:

```json
{
  "goals": ["speed", "ai", "collaboration"],
  "timeline_weeks": 12
}
```
