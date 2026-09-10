# GOharveST

Public-web frontend harvester. Paste a URL, get a structured snapshot: HTML, CSS, JS, assets, detected stack, and a downloadable ZIP.

This repository is a Django + DRF + Celery backend with a Vite/React dashboard.

## What works today

- Authenticated harvest jobs (`POST /api/jobs/`)
- Playwright page fetch with robots.txt check
- Public-URL / SSRF guard (blocks private IPs and localhost)
- Asset download into `media/harvests/<job-id>/`
- HTML rewrite so snapshot files point at local assets
- ZIP export on the job (`GET /api/jobs/<id>/download/`)
- Tech detection from HTML signatures

## What is still scaffolded

AI analysis, Lighthouse scores, recurring schedules, and most secondary React pages are placeholders. Use the single-URL harvest path first.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env   # or export DJANGO_SECRET_KEY yourself
python manage.py migrate
python manage.py runserver
```

In another terminal, with Redis running:

```bash
celery -A goharvest worker -l info
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173, register, then harvest a public URL.

## Docker

```bash
docker compose up --build
```

`frontend/node_modules` was committed earlier. After pulling this branch, run:

```bash
git rm -r --cached frontend/node_modules
```

## API

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/jobs/` body: `{ "url": "https://example.com", "options": { "mode": "full" } }`
- `GET /api/jobs/<id>/`
- `GET /api/jobs/<id>/result/`
- `GET /api/jobs/<id>/download/`

## Ethics

Only public pages. The scraper honors robots.txt, refuses non-http(s) URLs, and refuses hosts that resolve to private addresses. Check the site ToS before you harvest.
