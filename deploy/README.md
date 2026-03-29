# OpenOA Interview Deployment Adapter

This folder adds a lightweight web deployment wrapper around the OpenOA library.

## What This Adds

- Backend API (FastAPI):
  - `GET /api/health`
  - `GET /api/version`
  - `GET /api/methods`
- Frontend UI:
  - `GET /` serves a static dashboard that calls the API and renders live responses.

Note: The `/api/version` endpoint reads `openoa/__init__.py` directly for `__version__`.
This avoids installing the full scientific OpenOA dependency stack in the runtime container.

## Local Run (Docker)

From repository root:

```bash
docker build -t openoa-interview:local .
docker run --rm -p 8080:8080 openoa-interview:local
```

Validate in another terminal:

```bash
curl http://localhost:8080/api/health
curl http://localhost:8080/api/version
curl http://localhost:8080/api/methods
```

Open in browser:

```text
http://localhost:8080/
```

## Cloud Run Deploy (Google Cloud)

Set your project and region:

```bash
export PROJECT_ID="openoa-interview-260217"
export REGION="asia-south1"
```

Authenticate and select project:

```bash
gcloud auth login
gcloud config set project "$PROJECT_ID"
```

Enable required services:

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

Deploy:

```bash
gcloud run deploy openoa-interview \
  --source . \
  --region "$REGION" \
  --allow-unauthenticated \
  --port 8080
```

After deploy, capture the printed service URL. This is the primary submission link.

## Post-Deploy Checks

```bash
curl "<PRIMARY_URL>/api/health"
curl "<PRIMARY_URL>/api/version"
curl "<PRIMARY_URL>/api/methods"
```

Then open `<PRIMARY_URL>/` and verify the UI displays API values.

## Smoke Tests

Tests are in `deploy/tests/test_api.py`.

If running locally with Python environment configured:

```bash
pytest deploy/tests/test_api.py
```
