import runpy


def test_music_model_service_main_executes(capsys):
    runpy.run_path("backend/model_interface/music_model_service.py", run_name="__main__")
    out = capsys.readouterr().out
    assert "Results for predict_genres()" in out
    assert "Results for get_recommendations()" in out

