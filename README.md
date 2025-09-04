# Personal Notes Manager

## Introduction

The Personal Notes Manager is a web application that allows users to create, edit, view, and manage personal notes. The backend service implemented with Flask exposes RESTful JSON endpoints with OpenAPI documentation and includes full CRUD operations with persistent storage using SQLAlchemy.

## Project Overview

The backend service (`notes_backend`) is a Flask application that:
- Sets up CORS to permit access from any origin (configurable).
- Configures OpenAPI 3.0.3 documentation using `flask-smorest`.
- Provides a health check endpoint (`GET /`).
- Implements CRUD for notes at `/notes` and `/notes/{id}` with pagination, search, and an `archived` flag.
- Persists data using SQLAlchemy with SQLite by default or a configurable `DATABASE_URL`.

## Architecture

### Components and Responsibilities

- `notes_backend/app/__init__.py`
  - App factory `create_app()`, wiring config, CORS, OpenAPI, SQLAlchemy, and blueprints.
- `notes_backend/app/config.py`
  - Central configuration class with defaults and environment variable support.
- `notes_backend/app/models/note.py`
  - SQLAlchemy model for `Note` and DB instance.
- `notes_backend/app/models/__init__.py`
  - Model package export.
- `notes_backend/app/routes/health.py`
  - Health check blueprint and route.
- `notes_backend/app/routes/notes.py`
  - Notes blueprint implementing list/create/get/put/patch/delete.
- `notes_backend/app/schemas.py`
  - Marshmallow schemas for validation and serialization.
- `notes_backend/interfaces/openapi.json`
  - Snapshot OpenAPI spec for quick inspection.
- `notes_backend/run.py`
  - Entrypoint for running the app locally.

## Configuration

Environment variables (set in your environment or via a `.env` loader in your runtime):
- `DATABASE_URL`: SQLAlchemy database URI. Defaults to a local SQLite file `notes.db` within the `notes_backend` directory if not provided.
- `CORS_ORIGINS`: Comma-separated origins for CORS (default `*`).

A `.env.example` is provided at `notes_backend/.env.example`.

## How to Run

### Prerequisites
- Python 3.11+
- A virtual environment is recommended

### Setup and Start (Development)

1. Create and activate a virtual environment:
   - macOS/Linux:
     ```
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell):
     ```
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

2. Install dependencies:
   ```
   pip install -r notes_backend/requirements.txt
   ```

3. Run the application:
   ```
   python notes_backend/run.py
   ```
   Flask will start at `http://127.0.0.1:5000`.

4. OpenAPI and Swagger UI:
   - Swagger UI: `http://127.0.0.1:5000/docs`
   - OpenAPI JSON: `http://127.0.0.1:5000/openapi.json`

## API Summary

- `GET /` — Health check. Returns `{"message": "Healthy"}`.

Notes endpoints:
- `GET /notes` — List notes with pagination and optional `q` (search) and `archived` filter.
  - Query: `page` (default 1), `per_page` (default 10, max 100), `q`, `archived`.
- `POST /notes` — Create a new note.
  - Body: `{ "title": "string", "content": "string" }`.
- `GET /notes/{id}` — Retrieve a note by ID.
- `PUT /notes/{id}` — Replace note fields (any subset of `title`, `content`, `archived`).
- `PATCH /notes/{id}` — Partially update note (any subset of fields).
- `DELETE /notes/{id}` — Delete note by ID.

All endpoints return/accept JSON. Validation and documentation via `flask-smorest` and Marshmallow.

## Development Notes

- Code Style: `flake8` included.
- Tests: `pytest` included; add tests under `tests/`.
- Database: Uses SQLite by default. Switch to an external DB by setting `DATABASE_URL`.

## Future Improvements

- Authentication/authorization.
- Migrations (e.g., Alembic).
- Advanced search and tagging.
- Bulk operations and archival policies.
- Rate limiting and request logging.
- Comprehensive test suite and CI workflows.

## License

Add a suitable license (e.g., MIT) in a `LICENSE` file.
