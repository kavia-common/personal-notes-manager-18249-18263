# Personal Notes Manager

## Introduction

The Personal Notes Manager is a web application intended to allow users to create, edit, view, and manage personal notes. This repository currently contains the backend service implemented with Flask, exposing RESTful JSON endpoints and serving OpenAPI documentation. Although the long-term goal is to provide full CRUD operations on notes with persistent storage, the current codebase includes a basic health check endpoint and the scaffolding for API documentation and future endpoints.

## Project Overview

The backend service (`notes_backend`) is a Flask application that:
- Sets up CORS to permit access from any origin.
- Configures OpenAPI 3.0.3 documentation using `flask-smorest`.
- Exposes a health check endpoint (`GET /`) to verify that the service is running.
- Serves an OpenAPI JSON specification and an interactive Swagger UI via the configured docs prefix.

This service is described at a high level as providing RESTful JSON APIs for CRUD operations on notes, with an architectural dependency on a database service (referred to as `notes_database`). However, no database code or note-specific routes have yet been implemented in the current code snapshot.

## Architecture

### High-Level Architecture

- Application Layer: Flask app configured in `app/__init__.py`. It wires up CORS, creates the `flask_smorest.Api`, and registers blueprints.
- Routing Layer: Flask blueprints are used to define endpoints as modular components. The existing `health` blueprint demonstrates the pattern.
- API Documentation: `flask-smorest` generates OpenAPI, which is available via a docs prefix and Swagger UI.
- Container Dependencies: The backend service is intended to depend on a `notes_database` service for persistence, although database integration is not yet present in code.

### Components and Responsibilities

- `notes_backend/app/__init__.py`
  - Initializes the Flask app (`app`).
  - Configures CORS for all routes.
  - Sets API metadata such as title, version, and OpenAPI version.
  - Configures the docs prefix `/docs` and Swagger UI resource URL.
  - Instantiates the `Api` object (`flask_smorest.Api`) and registers blueprints.

- `notes_backend/app/routes/health.py`
  - Defines a simple blueprint with a single `GET /` endpoint returning `{ "message": "Healthy" }`.
  - Demonstrates the use of `MethodView` and `flask_smorest.Blueprint`.

- `notes_backend/interfaces/openapi.json`
  - A generated (or example) OpenAPI 3.0.3 specification reflecting the title (`My Flask API`), version (`v1`), tag(s), and error schemas used as defaults by the API.
  - Includes a path for the health check endpoint.

- `notes_backend/run.py`
  - Entrypoint for running the Flask application by importing `app` and calling `app.run()`.

## Backend (Flask, RESTful JSON APIs)

The backend is built on:
- Flask 3.x
- flask-smorest (for OpenAPI generation and request/response schema management)
- flask-cors (for Cross-Origin Resource Sharing)
- marshmallow and webargs (brought in by flask-smorest for schema validation)

Key configuration options set in `app/__init__.py`:
- API title: "My Flask API"
- API version: "v1"
- OpenAPI version: "3.0.3"
- Docs prefix: `/docs`
- Swagger UI URL: served from a CDN (`https://cdn.jsdelivr.net/npm/swagger-ui-dist/`)

These settings allow the API to serve an interactive Swagger UI and expose an OpenAPI JSON document. The health endpoint shows how endpoints are defined and tagged.

## Container Structure and Dependencies

- Container name: `notes_backend`
- Role: Backend API server for managing notes, user requests, and data processing.
- Interfaces: Intended RESTful JSON APIs for CRUD operations on notes.
- Dependencies: `notes_database` (referenced at the work item level as the persistence layer dependency; not implemented in code here).

Directory layout:
- `notes_backend/app/__init__.py` — Flask app factory and API configuration
- `notes_backend/app/routes/health.py` — health check blueprint and route
- `notes_backend/interfaces/openapi.json` — OpenAPI spec snapshot
- `notes_backend/requirements.txt` — Python dependencies for the backend
- `notes_backend/run.py` — development entrypoint to run Flask

Note: There is no `.env` in this container at present and no specific environment variables are required for the current health check functionality. If/when database integration is added, environment variables such as database URI, credentials, and feature flags will likely be introduced.

## How to Run

### Prerequisites
- Python 3.11+ (recommended to match modern Flask versions)
- A virtual environment is recommended

### Setup and Start (Development)

1. Create and activate a virtual environment:
   - On macOS/Linux:
     ```
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - On Windows (PowerShell):
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
   By default, Flask will start at `http://127.0.0.1:5000`. The health endpoint will be available at `/` and should return:
   ```
   {"message": "Healthy"}
   ```

4. OpenAPI and Swagger UI:
   - The Swagger UI is served at the `/docs` prefix. With the current configuration, the UI root path is the docs prefix itself:
     ```
     http://127.0.0.1:5000/docs
     ```
   - The OpenAPI JSON can be retrieved from:
     ```
     http://127.0.0.1:5000/openapi.json
     ```
     or as included snapshot at `notes_backend/interfaces/openapi.json`.

Note: In certain managed or containerized environments, the application may be exposed under different URLs. For example, if the service is deployed with a gateway proxy, its API spec may be reachable at `/openapi.json` with an externally provided base URL. Adjust the host and port accordingly.

## API Summary

The current implementation includes:
- `GET /` — Health check. Returns `{"message": "Healthy"}` on success.

Planned/expected endpoints for a complete Personal Notes Manager (not yet implemented in this code):
- `GET /notes` — List notes
- `POST /notes` — Create a new note
- `GET /notes/{id}` — Retrieve a note by ID
- `PUT /notes/{id}` — Replace an existing note
- `PATCH /notes/{id}` — Partially update a note
- `DELETE /notes/{id}` — Delete a note by ID

These would each return and accept JSON bodies, with validation handled by `flask-smorest` and associated `marshmallow` schemas. The backing storage would be provided by the `notes_database` dependency.

## Development Notes

- Code Style and Linting: `flake8` is included in `requirements.txt` and can be used to enforce style checks.
- Testing: `pytest` is present in `requirements.txt`. Add tests under a `tests/` directory and run `pytest` once tests are implemented.
- API Documentation: The project uses `flask-smorest` to define and generate OpenAPI documentation. As routes are added, ensure they are registered via blueprints and include appropriate request/response schemas and tags.

## Future Improvements

- Implement full CRUD routes for notes, with proper request/response schemas.
- Integrate a real database layer (`notes_database`) and configuration via environment variables (e.g., `DATABASE_URL`), including migrations and connection pooling.
- Add authentication and authorization for accessing and modifying notes.
- Implement pagination, filtering, and search for listing notes.
- Add unit and integration tests, including contract tests for the API.
- Provide dockerization and compose files to run `notes_backend` alongside `notes_database`.
- Expand documentation for the data model, error handling, and versioning strategy.

## License

Add a license suitable for your project (e.g., MIT), and include a `LICENSE` file at the repository root if desired.
