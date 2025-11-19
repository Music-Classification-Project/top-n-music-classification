import pytest
from werkzeug.exceptions import BadRequest
from backend.model_interface.flask_app import genres as genres_mod

"""
Focuses on the helper utilities behind genre handling (label lists, validation helpers, 
etc.),ensuring they return the expected data structures and raise on invalid inputs.

"""
def test_parse_int_defaults():
    assert genres_mod._parse_int(None, default=7) == 7
    assert genres_mod._parse_int("", default=3) == 3


def test_parse_int_valid():
    assert (
        genres_mod._parse_int("5", default=1, minimum=1, maximum=10, name="top_k")
        == 5
    )


def test_parse_int_invalid_type():
    with pytest.raises(BadRequest):
        genres_mod._parse_int("abc", name="top_k")


def test_parse_int_below_minimum():
    with pytest.raises(BadRequest):
        genres_mod._parse_int("0", minimum=1, name="top_k")


def test_parse_int_above_maximum():
    with pytest.raises(BadRequest):
        genres_mod._parse_int("11", maximum=10, name="top_k")
