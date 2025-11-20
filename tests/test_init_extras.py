"""
Covers factory wiring, config flags, and blueprint logic to test the espected routes
and settings.

"""


def test_create_app_handles_oserror(monkeypatch):
    from backend.model_interface.flask_app.__init__ import create_app
    import os as real_os

    called = {"made": False}

    def bad_makedirs(path, exist_ok=False):
        called["made"] = True
        raise OSError("boom")

    monkeypatch.setattr(real_os, "makedirs", bad_makedirs)
    app = create_app({"TESTING": True, "USE_DUMMY_SERVICE": True})
    assert app is not None and called["made"] is True


def test_create_app_fallback_to_dummy_on_service_error(monkeypatch, tmp_path):
    from backend.model_interface.flask_app.__init__ import create_app

    # Force real service path and failure by using a non-existent file
    bad_path = tmp_path / "missing_model.keras"
    assert not bad_path.exists()
    app = create_app({"TESTING": True, "USE_DUMMY_SERVICE": False, "MODEL_PATH": str(bad_path)})
    svc = app.config["SERVICE"]
    # Should be DummyMusicModelService due to fallback
    assert getattr(svc, "dummy_mode", False) is True


def test_testing_app_route():
    # Import module and use the testing-only app
    import backend.model_interface.flask_app.__init__ as init_mod

    client = init_mod.test_app.test_client()
    rv = client.get("/test")
    assert rv.status_code == 200
    assert rv.get_json()["message"].startswith("You've reached Flask testing!")
