import io
from flask import Blueprint, jsonify, request, current_app
from werkzeug.exceptions import BadRequest

# blueprint
bp = Blueprint("genres", __name__, url_prefix="/v1/genres")


def _parse_int(value, default=None, minimum=None, maximum=None, name="value"):
    """Parse an integer query/form value with optional bounds. """
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
    """GET /v1/genres — minimal model metadata.

    Returns the available genres and the current model version
    """
    svc = current_app.config["SERVICE"]
    return (
        jsonify({"data": {"genres": getattr(svc, "labels", []), "model_version": getattr(svc, "version", "unknown")}}),
        200,
    )


@bp.route("/music", methods=("GET", "POST"), strict_slashes=False)
def music():
    """/v1/genres/music — genre prediction endpoint.

    - GET (dummy mode only): return demo predictions for quick UI testing.
    - POST (multipart): accept an audio file and return top-k genres.
    """
    svc = current_app.config["SERVICE"]
    if request.method == "GET":
        # Demo predictions in dummy mode; usage help otherwise
        top_k = _parse_int(
            request.args.get("top_k"),
            default=5,
            minimum=1,
            maximum=getattr(svc, "max_top_k", None),
            name="top_k",
        )
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
                            "max": getattr(svc, "max_top_k", None),
                        },
                    },
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
        maximum=getattr(svc, "max_top_k", None),
        name="top_k",
    )

    # Route audio to the service; use the file stream
    preds = svc.predict_genres(file.stream, top_k=top_k)

    # Ensure JSON-safe types and schema
    results = [
        {"genre": str(label), "confidence": float(score)} for (label, score) in preds
    ]

    return jsonify({"predictions": results, "top_k": top_k}), 200


@bp.route("/recommendations", methods=("GET", "POST"), strict_slashes=False)
def recommendations():
    """/v1/genres/recommendations — similar songs endpoint.

    - GET (dummy mode only): return demo recommendations.
    - POST (multipart): accept an audio file and return recommendations.
    """
    svc = current_app.config["SERVICE"]

    if request.method == "GET":
        # Demo recommendations in dummy mode; usage help otherwise
        limit = _parse_int(request.args.get("limit"), default=5, minimum=1, name="limit")
        if bool(current_app.config.get("USE_DUMMY_SERVICE", False)):
            recs = svc.get_recommendations(io.BytesIO(b""), num_recommendations=limit)
            payload = [
                {
                    "title": str(r.get("title")),
                    "artist": str(r.get("artist")),
                    "genre": str(r.get("genre")),
                    "similarity_score": float(r.get("similarity_score", 0.0)),
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

    # Coerce to JSON-safe primitives
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
