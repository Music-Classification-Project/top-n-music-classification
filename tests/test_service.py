import io
import pytest

from backend.model_interface.music_model_service import (
    MusicModelService,
    DummyMusicModelService,
    ModelLoadError,
)

"""
Validates predict and recommend functions

"""



def test_service_type_error():
    with pytest.raises(TypeError):
        MusicModelService(model_path=123)  # type: ignore[arg-type]


def test_service_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        MusicModelService(tmp_path / "missing.keras")


def test_service_model_load_success_and_methods(tmp_path):
    p = tmp_path / "exists.keras"
    p.write_bytes(b"x")
    svc = MusicModelService(p)
    assert svc.loaded is True
    assert svc.model_path == p
    # Call pass-through methods to cover bodies
    assert svc.predict_genres(io.BytesIO(b"abc"), top_k=1) is None
    assert svc.get_recommendations(io.BytesIO(b"abc"), num_recommendations=1) is None


def test_service_model_load_error(tmp_path, monkeypatch):
    p = tmp_path / "exists.keras"
    p.write_bytes(b"x")

    from backend.model_interface import music_model_service as mms

    class Broken(mms.MusicModelService):
        def _load_model(self, path):  # noqa: N802 - test override
            raise RuntimeError("boom")

    with pytest.raises(ModelLoadError):
        Broken(p)


def test_dummy_predict_respects_top_k():
    svc = DummyMusicModelService("any")
    out = svc.predict_genres("ignored", top_k=2)
    assert len(out) == 2 and out[0][0] == "rock" and isinstance(out[0][1], float)


def test_dummy_recommendations_respects_limit_and_shape():
    svc = DummyMusicModelService("any")
    out = svc.get_recommendations("ignored", num_recommendations=3)
    assert len(out) == 3
    keys = {"title", "artist", "genre", "similarity_score"}
    assert set(out[0].keys()) == keys
    assert isinstance(out[0]["similarity_score"], float)
