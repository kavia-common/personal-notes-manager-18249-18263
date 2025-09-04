import os
from dataclasses import dataclass


@dataclass
class Config:
    """Base configuration for the Flask application."""
    # Database URI. Use env var DATABASE_URL if provided; fallback to SQLite file.
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(__file__)), 'notes.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # Smorest / OpenAPI config
    API_TITLE: str = "Personal Notes API"
    API_VERSION: str = "v1"
    OPENAPI_VERSION: str = "3.0.3"
    OPENAPI_URL_PREFIX: str = "/docs"
    OPENAPI_SWAGGER_UI_PATH: str = ""
    OPENAPI_SWAGGER_UI_URL: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")
