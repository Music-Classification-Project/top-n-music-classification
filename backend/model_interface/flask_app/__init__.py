import os
from typing import Any, Dict

from flask import Flask, jsonify, request, Response
from flask_cors import CORS

# Import the service layer
try:
    # If package import path works
    from model_interface.music_model_service import (
        MusicModelService,
        DummyMusicModelService,
    )
except Exception:  # pragma: no cover - fallback if import path differs during dev
    # Fallback relative import if running directly
    from ..music_model_service import (  # type: ignore
        MusicModelService,
        DummyMusicModelService,
    )


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "bad_request", "message": str(e)}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "not_found", "message": "Not found"}), 404

    @app.errorhandler(413)
    def too_large(e):
        return jsonify({"error": "payload_too_large", "message": "File too large"}), 413

    @app.errorhandler(500)
    def internal_error(e):
        return (
            jsonify({"error": "internal_server_error", "message": "Unexpected error"}),
            500,
        )
    
    @app.errorhandler(405)
    def method_not_allowed(e):  # type: ignore[unused-ignore]
        allowed = []
        try:
            allowed = list(e.valid_methods or [])  # type: ignore[attr-defined]
        except Exception:  # pragma: no cover - defensive fallback
            pass  # pragma: no cover
        return jsonify({"error": "method_not_allowed", "allowed": allowed}), 405


def _enable_cors(app: Flask) -> None:
    # Lightweight CORS allow-all for dev; replace with Flask-CORS if desired.
    @app.after_request
    def add_cors_headers(response):
        response.headers.setdefault("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
        response.headers.setdefault("Vary", "Origin")
        response.headers.setdefault("Access-Control-Allow-Credentials", "true")
        response.headers.setdefault(
            "Access-Control-Allow-Headers",
            request.headers.get("Access-Control-Request-Headers", "Authorization, Content-Type"),
        )
        response.headers.setdefault(
            "Access-Control-Allow-Methods",
            request.headers.get("Access-Control-Request-Method", "GET, POST, OPTIONS"),
        )
        return response


def _build_openapi(app: Flask) -> Dict[str, Any]:
    # Minimal OpenAPI contract served at /openapi.json
    service = app.config.get("SERVICE")
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "Music Model API",
            "version": "v1",
            "description": "Endpoints for genre prediction and recommendations.",
        },
        "paths": {
            "/v1/health": {
                "get": {
                    "summary": "Health/metadata",
                    "responses": {
                        "200": {
                            "description": "Service health",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/HealthResponse"}}},
                        },
                        "500": {"description": "Server error", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}},
                    },
                }
            },
            "/v1/genres": {
                "get": {
                    "summary": "Get genres and model version",
                    "responses": {
                        "200": {"description": "OK", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/GenreInfoResponse"}}}},
                        "500": {"description": "Server error", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}},
                    },
                }
            },
            "/v1/genres/music": {
                "get": {
                    "summary": "Demo predictions when USE_DUMMY_SERVICE=true; usage otherwise",
                    "parameters": [
                        {
                            "name": "top_k",
                            "in": "query",
                            "schema": {"type": "integer", "minimum": 1},
                            "required": False,
                        }
                    ],
                    "responses": {
                        "200": {"description": "OK", "content": {"application/json": {"schema": {"oneOf": [
                            {"$ref": "#/components/schemas/PredictionsResponse"},
                            {"$ref": "#/components/schemas/UsageResponse"}
                        ]}}}},
                        "500": {"description": "Server error", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}},
                    },
                },
                "post": {
                    "summary": "Predict top genres for an audio file",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "multipart/form-data": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "file": {"type": "string", "format": "binary"},
                                        "top_k": {"type": "integer", "minimum": 1},
                                    },
                                    "required": ["file"],
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "OK", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PredictionsResponse"}}}},
                        "400": {"description": "Bad request", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}},
                        "413": {"description": "Payload too large", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}},
                        "405": {"description": "Method not allowed", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}},
                        "500": {"description": "Server error", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}},
                    },
                }
            },
            "/v1/genres/recommendations": {
                "get": {
                    "summary": "Demo recommendations when USE_DUMMY_SERVICE=true; usage otherwise",
                    "parameters": [
                        {
                            "name": "limit",
                            "in": "query",
                            "schema": {"type": "integer", "minimum": 1},
                            "required": False,
                        }
                    ],
                    "responses": {
                        "200": {"description": "OK", "content": {"application/json": {"schema": {"oneOf": [
                            {"$ref": "#/components/schemas/RecommendationsResponse"},
                            {"$ref": "#/components/schemas/UsageResponse"}
                        ]}}}},
                        "500": {"description": "Server error", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}},
                    },
                },
                "post": {
                    "summary": "Get song recommendations for an audio file",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "multipart/form-data": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "file": {"type": "string", "format": "binary"},
                                        "limit": {"type": "integer", "minimum": 1},
                                    },
                                    "required": ["file"],
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "OK", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/RecommendationsResponse"}}}},
                        "400": {"description": "Bad request", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}},
                        "413": {"description": "Payload too large", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}},
                        "405": {"description": "Method not allowed", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}},
                        "500": {"description": "Server error", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}},
                    },
                }
            },
            "/docs": {
                "get": {
                    "summary": "Swagger UI",
                    "responses": {"200": {"description": "HTML"}},
                }
            },
        },
        "x-service-meta": {
            "loaded": bool(getattr(service, "loaded", False)),
            "genres": getattr(service, "labels", []),
            "version": getattr(service, "version", "unknown"),
            "model_name": getattr(service, "model_name", None),
            "dummy_mode": bool(getattr(service, "dummy_mode", False)),
            "class_count": getattr(service, "class_count", None),
            "sample_rate": getattr(service, "sample_rate", None),
            "input_duration_sec": getattr(service, "input_duration_sec", None),
            "channels": getattr(service, "channels", None),
            "feature_types": getattr(service, "feature_types", None),
            "n_mels": getattr(service, "n_mels", None),
            "n_mfcc": getattr(service, "n_mfcc", None),
            "n_fft": getattr(service, "n_fft", None),
            "hop_length": getattr(service, "hop_length", None),
            "max_file_mb": getattr(service, "max_file_mb", None),
            "max_top_k": getattr(service, "max_top_k", None),
        },
        "components": {
            "schemas": {
                "Error": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"},
                        "message": {"type": "string"},
                        "allowed": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["error"],
                },
                "Prediction": {
                    "type": "object",
                    "properties": {
                        "genre": {"type": "string"},
                        "confidence": {"type": "number"},
                    },
                    "required": ["genre", "confidence"],
                },
                "PredictionsResponse": {
                    "type": "object",
                    "properties": {
                        "predictions": {"type": "array", "items": {"$ref": "#/components/schemas/Prediction"}},
                        "top_k": {"type": "integer"},
                        "demo": {"type": "boolean"},
                    },
                    "required": ["predictions", "top_k"],
                },
                "RecommendationItem": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "artist": {"type": "string"},
                        "genre": {"type": "string"},
                        "similarity_score": {"type": "number"},
                    },
                    "required": ["title", "artist", "genre", "similarity_score"],
                },
                "RecommendationsResponse": {
                    "type": "object",
                    "properties": {
                        "recommendations": {"type": "array", "items": {"$ref": "#/components/schemas/RecommendationItem"}},
                        "limit": {"type": "integer"},
                        "demo": {"type": "boolean"},
                    },
                    "required": ["recommendations", "limit"],
                },
                "GenreInfoResponse": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "genres": {"type": "array", "items": {"type": "string"}},
                                "model_version": {"type": "string"},
                            },
                            "required": ["genres", "model_version"],
                        }
                    },
                    "required": ["data"],
                },
                "HealthResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "loaded": {"type": "boolean"},
                        "version": {"type": "string"},
                        "genres": {"type": "array", "items": {"type": "string"}},
                        "model_name": {"type": "string"},
                        "dummy_mode": {"type": "boolean"},
                        "class_count": {"type": "integer"},
                        "sample_rate": {"type": "integer"},
                        "input_duration_sec": {"type": "integer"},
                        "channels": {"type": "integer"},
                        "feature_types": {"type": "array", "items": {"type": "string"}},
                        "n_mels": {"type": "integer"},
                        "n_mfcc": {"type": "integer"},
                        "n_fft": {"type": "integer"},
                        "hop_length": {"type": "integer"},
                        "max_file_mb": {"type": "integer"},
                        "max_top_k": {"type": "integer"},
                    },
                    "required": ["status", "loaded", "version", "genres"],
                },
                "UsageResponse": {
                    "type": "object",
                    "properties": {
                        "usage": {"type": "string"},
                        "fields": {"type": "object"},
                        "example_curl": {"type": "string"},
                    },
                    "required": ["usage"],
                },
            }
        },
    }


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    # basic config
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        MAX_CONTENT_LENGTH=int(os.environ.get("MAX_CONTENT_LENGTH", 32 * 1024 * 1024)),  # 32MB
        MODEL_PATH=os.environ.get("MODEL_PATH", os.path.join(os.getcwd(), "src", "preprocess", "best_model.keras")),
        USE_DUMMY_SERVICE=os.environ.get("USE_DUMMY_SERVICE", "true").lower() in {"1", "true", "yes"},
    )

    if test_config is not None:
        # allow tests to override
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize service and store on app config
    model_path = app.config["MODEL_PATH"]
    use_dummy = app.config["USE_DUMMY_SERVICE"]
    if use_dummy:
        service = DummyMusicModelService(model_path)
    else:
        try:
            service = MusicModelService(model_path)
        except Exception:
            # Fallback to dummy if load fails; log minimal info
            service = DummyMusicModelService(model_path)
    app.config["SERVICE"] = service

    # Register blueprints
    from .genres import bp as genres_bp  # type: ignore

    app.register_blueprint(genres_bp)

    # Status endpoint (preferred)
    @app.get("/v1/status", strict_slashes=False)
    def status():
        svc = app.config.get("SERVICE")
        return (
            jsonify(
                {
                    "status": "ok",
                    "loaded": bool(getattr(svc, "loaded", False)),
                    "version": getattr(svc, "version", "unknown"),
                    "genres": getattr(svc, "labels", []),
                    "model_name": getattr(svc, "model_name", None),
                    "dummy_mode": bool(getattr(svc, "dummy_mode", False)),
                    "class_count": getattr(svc, "class_count", None),
                    "sample_rate": getattr(svc, "sample_rate", None),
                    "input_duration_sec": getattr(svc, "input_duration_sec", None),
                    "channels": getattr(svc, "channels", None),
                    "feature_types": getattr(svc, "feature_types", None),
                    "n_mels": getattr(svc, "n_mels", None),
                    "n_mfcc": getattr(svc, "n_mfcc", None),
                    "n_fft": getattr(svc, "n_fft", None),
                    "hop_length": getattr(svc, "hop_length", None),
                    "max_file_mb": getattr(svc, "max_file_mb", None),
                    "max_top_k": getattr(svc, "max_top_k", None),
                }
            ),
            200,
        )

    # Back-compat alias for older clients
    @app.get("/v1/health", strict_slashes=False)
    def health():
        return status()

    # OpenAPI contract
    @app.get("/openapi.json")
    def openapi():
        return jsonify(_build_openapi(app))


    # Minimal Swagger UI (uses CDN)
    @app.get("/docs")
    def docs():
        html = """
<!doctype html>
<html>
  <head>
    <meta charset=\"utf-8\" />
    <title>Music Model API Docs</title>
    <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css\" />
  </head>
  <body>
    <div id=\"swagger-ui\"></div>
    <script src=\"https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.min.js\"></script>
    <script>
      window.onload = () => {
        window.ui = SwaggerUIBundle({
          url: '/openapi.json',
          dom_id: '#swagger-ui',
          presets: [SwaggerUIBundle.presets.apis],
          layout: 'BaseLayout'
        });
      };
    </script>
  </body>
</html>
"""
        return Response(html, mimetype="text/html")

    _register_error_handlers(app)
    _enable_cors(app)

    return app

# # Testing Only 
# test_app = Flask(__name__)
# CORS(test_app)
# @test_app.route('/test', methods=['GET'])
# def test_endpoint():
#     return jsonify(message="You've reached Flask testing!")

# if __name__ == '__main__' and os.getenv == 'development':
#     test_app.run(debug=True)