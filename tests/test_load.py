import pytest

from numeral_converter import get_available_languages, load


def test_load_unknown_lang():
    with pytest.raises(ValueError):
        load("unknown")


def test_load():
    load("uk")
    assert True


def test_get_available_languages():
    languages = get_available_languages()
    assert len(languages) > 0
    assert "uk" in languages
