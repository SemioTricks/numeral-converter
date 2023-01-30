import pytest

from numeral_converter import load


def test_unknown_lang():
    with pytest.raises(ValueError):
        load("unknown")


def test_load():
    load("uk")
    assert True
