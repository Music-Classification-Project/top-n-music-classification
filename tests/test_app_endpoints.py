import io

"""
Exercises every Flask HTTP endpoint under /v1 including: docs/openapi routes, 
dummy-mode responses when correct inputs are provided, error checks(bad top_k/limit, missing uploads, 
empty filenames), and error handlers for 404/405/413/500 to confirm proper JSON payloads 
and CORS headers.

"""


def test_status_and_health(client_dummy):
    rv = client_dummy.get("/v1/status")
    assert rv.status_code == 200
    j = rv.get_json()
    assert j.get("status") == "ok"
    assert "genres" in j and "version" in j

    rv2 = client_dummy.get("/v1/health")
    assert rv2.status_code == 200
    assert rv2.get_json() == j


def test_openapi_and_docs(client_dummy):
    rv = client_dummy.get("/openapi.json")
    assert rv.status_code == 200
    j = rv.get_json()
    assert "openapi" in j and "paths" in j and "components" in j
    assert "/v1/genres" in j["paths"]

    rv2 = client_dummy.get("/docs")
    assert rv2.status_code == 200
    assert "text/html" in rv2.content_type
    assert b"SwaggerUIBundle" in rv2.data


def test_genres_info(client_dummy):
    rv = client_dummy.get("/v1/genres")
    assert rv.status_code == 200
    j = rv.get_json()
    assert "data" in j and "genres" in j["data"] and "model_version" in j["data"]


def test_music_get_dummy_happy_path_default_top_k(client_dummy):
    rv = client_dummy.get("/v1/genres/music")
    assert rv.status_code == 200
    j = rv.get_json()
    assert j.get("demo") is True
    assert "predictions" in j
    assert j["top_k"] == 5


def test_music_get_dummy_with_top_k_and_validation(client_dummy):
    rv = client_dummy.get("/v1/genres/music?top_k=2")
    assert rv.status_code == 200
    j = rv.get_json()
    assert j["top_k"] == 2
    assert isinstance(j["predictions"], list) and len(j["predictions"]) == 2

    rv_bad = client_dummy.get("/v1/genres/music?top_k=0")
    assert rv_bad.status_code == 400
    assert rv_bad.get_json()["error"] == "bad_request"

    rv_bad2 = client_dummy.get("/v1/genres/music?top_k=abc")
    assert rv_bad2.status_code == 400
    assert rv_bad2.get_json()["error"] == "bad_request"

    rv_bad3 = client_dummy.get("/v1/genres/music?top_k=11")
    assert rv_bad3.status_code == 400


def test_music_get_usage_when_not_dummy(client_nodummy):
    rv = client_nodummy.get("/v1/genres/music")
    assert rv.status_code == 200
    j = rv.get_json()
    assert "usage" in j and "fields" in j and "example_curl" in j


def test_music_post_success_and_missing_file(client_dummy):
    data = {"file": (io.BytesIO(b"fake-wav"), "clip.wav"), "top_k": "3"}
    rv = client_dummy.post(
        "/v1/genres/music",
        data=data,
        content_type="multipart/form-data",
    )
    assert rv.status_code == 200
    j = rv.get_json()
    assert j["top_k"] == 3
    assert all(set(p.keys()) == {"genre", "confidence"} for p in j["predictions"])

    rv2 = client_dummy.post(
        "/v1/genres/music", data={}, content_type="multipart/form-data"
    )
    assert rv2.status_code == 400
    assert rv2.get_json()["error"] == "bad_request"


def test_music_post_empty_filename(client_dummy):
    data = {"file": (io.BytesIO(b"abc"), "")}
    rv = client_dummy.post(
        "/v1/genres/music",
        data=data,
        content_type="multipart/form-data",
    )
    assert rv.status_code == 400
    assert rv.get_json()["error"] == "bad_request"


def test_music_post_invalid_top_k(client_dummy):
    data = {"file": (io.BytesIO(b"abc"), "clip.wav"), "top_k": "0"}
    rv = client_dummy.post(
        "/v1/genres/music",
        data=data,
        content_type="multipart/form-data",
    )
    assert rv.status_code == 400


def test_recommendations_get_dummy_and_validation(client_dummy):
    rv = client_dummy.get("/v1/genres/recommendations?limit=4")
    assert rv.status_code == 200
    j = rv.get_json()
    assert j.get("demo") is True
    assert len(j["recommendations"]) == 4

    rv_bad = client_dummy.get("/v1/genres/recommendations?limit=0")
    assert rv_bad.status_code == 400
    assert rv_bad.get_json()["error"] == "bad_request"

    rv_bad2 = client_dummy.get("/v1/genres/recommendations?limit=abc")
    assert rv_bad2.status_code == 400


def test_recommendations_get_usage_when_not_dummy(client_nodummy):
    rv = client_nodummy.get("/v1/genres/recommendations")
    assert rv.status_code == 200
    j = rv.get_json()
    assert "usage" in j and "fields" in j and "example_curl" in j


def test_recommendations_post_success_and_missing_file(client_dummy):
    data = {"file": (io.BytesIO(b"fake-wav"), "clip.wav"), "limit": "2"}
    rv = client_dummy.post(
        "/v1/genres/recommendations",
        data=data,
        content_type="multipart/form-data",
    )
    assert rv.status_code == 200
    j = rv.get_json()
    assert len(j["recommendations"]) == 2
    first = j["recommendations"][0]
    assert set(first.keys()) == {"title", "artist", "genre", "similarity_score"}
    assert isinstance(first["similarity_score"], float)

    rv2 = client_dummy.post(
        "/v1/genres/recommendations", data={}, content_type="multipart/form-data"
    )
    assert rv2.status_code == 400
    assert rv2.get_json()["error"] == "bad_request"


def test_recommendations_post_empty_filename(client_dummy):
    data = {"file": (io.BytesIO(b"abc"), "")}
    rv = client_dummy.post(
        "/v1/genres/recommendations",
        data=data,
        content_type="multipart/form-data",
    )
    assert rv.status_code == 400
    assert rv.get_json()["error"] == "bad_request"


def test_404_and_405_and_cors(client_dummy):
    rv = client_dummy.get("/nope")
    assert rv.status_code == 404
    assert rv.get_json()["error"] == "not_found"

    rv2 = client_dummy.post("/v1/genres")
    assert rv2.status_code == 405
    j = rv2.get_json()
    assert j["error"] == "method_not_allowed"
    assert "GET" in j.get("allowed", [])

    rv3 = client_dummy.get("/v1/genres")
    assert "Access-Control-Allow-Origin" in rv3.headers
    assert rv3.headers.get("Vary") == "Origin"


def test_413_payload_too_large():
    from backend.model_interface.flask_app.__init__ import create_app

    app = create_app(
        {"TESTING": True, "USE_DUMMY_SERVICE": True, "MAX_CONTENT_LENGTH": 10}
    )
    client = app.test_client()
    big = b"x" * 100
    rv = client.post(
        "/v1/genres/music",
        data={"file": (io.BytesIO(big), "big.wav")},
        content_type="multipart/form-data",
    )
    assert rv.status_code == 413
    assert rv.get_json()["error"] == "payload_too_large"


def test_500_error_handler_on_service_exception(app_dummy):
    class BoomService:
        max_top_k = 10

        def predict_genres(self, stream, top_k=5):
            raise RuntimeError("explode")

    app_dummy.config["SERVICE"] = BoomService()
    # Ensure exceptions are handled by error handler (not propagated)
    app_dummy.config["TESTING"] = False
    app_dummy.config["PROPAGATE_EXCEPTIONS"] = False
    client = app_dummy.test_client()
    # GET path calls predict_genres in dummy mode
    rv = client.get("/v1/genres/music")
    assert rv.status_code == 500
    j = rv.get_json()
    assert j["error"] == "internal_server_error"
