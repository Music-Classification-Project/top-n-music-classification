import io
from flask import Blueprint, jsonify, request, current_app
from werkzeug.exceptions import BadRequest

# Blueprint
bp = Blueprint("genres", __name__, url_prefix="/v1/genres")


# Healper function to return metadata
def _feature_meta(service):
    cfg = getattr(service, "feature_config", {}) or {}
    return {
        "feature_types": getattr(service, "feature_types", []),
        "sample_rate": getattr(service, "sample_rate", cfg.get("sample_rate")),
        "input_duration_sec": getattr(service, "input_duration_sec", cfg.get("input_duration_sec")),
        "n_fft": getattr(service, "n_fft", cfg.get("n_fft")),
        "hop_length": getattr(service, "hop_length", cfg.get("hop_length")),
        "n_mels": getattr(service, "n_mels", cfg.get("n_mels")),
        "n_mfcc": getattr(service, "n_mfcc", cfg.get("n_mfcc")),
        "normalize_per_feature": cfg.get("normalize_per_feature"),
    }


def _parse_int(value, default=None, minimum=None, maximum=None, name="value"):
    """Parse int with optional bounds; BadRequest on error."""
    if value is None or value == "":
        return default
    try:
        iv = int(value)
    except (TypeError, ValueError):
        raise BadRequest(f"{name} must be an integer")
    if minimum is not None and iv < minimum:
        raise BadRequest(f"{name} must be >= {minimum}")
    if maximum is not None and iv > maximum:
        raise BadRequest(f"{name} must be <= {maximum}")
    return iv


def _require_file():
    """Fetch and validate an uploaded file from the current request."""
    if "file" not in request.files:
        raise BadRequest("Missing file in form-data with key 'file'")
    file = request.files["file"]
    if file.filename == "":
        raise BadRequest("Empty filename")
    return file


@bp.route("", methods=("GET",), strict_slashes=False)
def info():
    """GET /v1/genres: model metadata.

    Returns available genres and model version.
    """
    svc = current_app.config["SERVICE"]
    return (
        jsonify({
            "data": {
                "genres": getattr(svc, "labels", []),
                "model_version": getattr(svc, "version", "unknown"),
                "features": _feature_meta(svc),
            }
        }),
        200,
    )


@bp.route("/music", methods=("GET", "POST"), strict_slashes=False)
def music():
    """/v1/genres/music: genre prediction endpoint.

    - GET: Return mock predictions for UI testing.
    - POST: Accept audio file; return top-k genres.
    """
    svc = current_app.config["SERVICE"]
    max_top_k = getattr(svc, "max_top_k", len(getattr(svc, "labels", [])) or None)
    if request.method == "GET":
        # Parse top_k from query
        top_k = _parse_int(
            request.args.get("top_k"),
            default=5,
            minimum=1,
            maximum=max_top_k,
            name="top_k",
        )
        # Dummy mode: Return mock predictions for UI testing
        if bool(current_app.config.get("USE_DUMMY_SERVICE", False)):
            preds = svc.predict_genres(io.BytesIO(b""), top_k=top_k)
            results = [
                {"genre": str(label), "confidence": float(score)} for (label, score) in preds
            ]
            return jsonify({"predictions": results, "top_k": top_k, "demo": True}), 200
        return (
            jsonify(
                {
                    "usage": "POST multipart/form-data with 'file' and optional 'top_k'",
                    "fields": {
                        "file": {"type": "binary", "required": True},
                        "top_k": {
                            "type": "integer",
                            "required": False,
                            "default": 5,
                            "min": 1,
                            "max": max_top_k,
                        },
                    },
                    "features": _feature_meta(svc),
                    "example_curl": "curl -F file=@clip.wav -F top_k=5 http://127.0.0.1:5000/v1/genres/music",
                }
            ),
            200,
        )

    # POST: multipart/form-data with 'file' + optional 'top_k'
    file = _require_file()

    top_k = _parse_int(
        request.form.get("top_k", request.args.get("top_k")),
        default=5,
        minimum=1,
        maximum=max_top_k,
        name="top_k",
    )

    # Route audio to the service; use the file stream
    preds = svc.predict_genres(file.stream, top_k=top_k)

    # Ensure JSON-safe types
    results = [
        {"genre": str(label), "confidence": float(score)} for (label, score) in preds
    ]

    return jsonify({"predictions": results, "top_k": top_k}), 200


@bp.route("/recommendations", methods=("GET", "POST"), strict_slashes=False)
def recommendations():
    """/v1/genres/recommendations: similar songs endpoint.

    - GET: Return mock recommendations for UI testing.
    - POST: Accept audio file; return recommendations.
    """
    svc = current_app.config["SERVICE"]

    if request.method == "GET":
        # Parse limit from query
        limit = _parse_int(request.args.get("limit"), default=5, minimum=1, name="limit")

        # Dummy mode: Return mock recommendations for UI testing
        if bool(current_app.config.get("USE_DUMMY_SERVICE", False)):
            recs = svc.get_recommendations(io.BytesIO(b""), num_recommendations=limit)
            payload = [
                {
                    "title": str(r.get("title")),
                    "artist": str(r.get("artist")),
                    "genre": str(r.get("genre")),
                    "image_url": str(r.get("image_url"))
                    # "similarity_score": float(r.get("similarity_score", 0.0)),
                }
                for r in recs
            ]
            return jsonify({"recommendations": payload, "limit": limit, "demo": True}), 200
        return (
            jsonify(
                {
                    "usage": "POST multipart/form-data with 'file' and optional 'limit'",
                    "fields": {
                        "file": {"type": "binary", "required": True},
                        "limit": {"type": "integer", "required": False, "default": 5, "min": 1},
                    },
                    "features": _feature_meta(svc),
                    "example_curl": "curl -F file=@clip.wav -F limit=5 http://127.0.0.1:5000/v1/genres/recommendations",
                }
            ),
            200,
        )

    # POST below
    file = _require_file()

    limit = _parse_int(
        request.form.get("limit", request.args.get("limit")),
        default=5,
        minimum=1,
        name="limit",
    )

    recs = svc.get_recommendations(file.stream, num_recommendations=limit)

    # Normalize each recommendation to JSON-safe types
    payload = [
        {
            "title": str(r.get("title")),
            "artist": str(r.get("artist")),
            "genre": str(r.get("genre")),
            "similarity_score": float(r.get("similarity_score", 0.0)),
        }
        for r in recs
    ]
    return jsonify({"recommendations": payload, "limit": limit}), 200

