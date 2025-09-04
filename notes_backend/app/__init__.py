from flask import Flask, jsonify
from flask_cors import CORS
from flask_smorest import Api
from .config import Config
from .routes.health import blp as health_blp
from .routes.notes import blp as notes_blp
from .models.note import db


def create_app() -> Flask:
    # PUBLIC_INTERFACE
    """Create and configure the Flask application with API, DB, and routes."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Load configuration
    app.config.from_object(Config)

    # CORS
    CORS(app, resources={r"/*": {"origins": app.config.get('CORS_ORIGINS', '*')}})

    # OpenAPI / Smorest
    app.config["API_TITLE"] = app.config.get("API_TITLE", "Personal Notes API")
    app.config["API_VERSION"] = app.config.get("API_VERSION", "v1")
    app.config["OPENAPI_VERSION"] = app.config.get("OPENAPI_VERSION", "3.0.3")
    app.config["OPENAPI_URL_PREFIX"] = app.config.get("OPENAPI_URL_PREFIX", "/docs")
    app.config["OPENAPI_SWAGGER_UI_PATH"] = app.config.get("OPENAPI_SWAGGER_UI_PATH", "")
    app.config["OPENAPI_SWAGGER_UI_URL"] = app.config.get(
        "OPENAPI_SWAGGER_UI_URL", "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    # Init DB
    db.init_app(app)

    # Initialize Api and register blueprints
    api = Api(app)
    api.register_blueprint(health_blp)
    api.register_blueprint(notes_blp)

    # Error handlers for better JSON errors
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"message": "Not Found"}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"message": "Bad Request"}), 400

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"message": "Internal Server Error"}), 500

    # Create tables if using SQLite or when DB is empty.
    with app.app_context():
        db.create_all()

    return app


# Expose default 'app' for run.py compatibility
app = create_app()
