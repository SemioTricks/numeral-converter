import pytest

from numeral_converter import get_available_languages, load_numeral_data


def test_load_unknown_lang():
    with pytest.raises(ValueError):
        load_numeral_data("unknown")


def test_load_uk():
    load_numeral_data("uk")
    assert True


def test_load_ru():
    load_numeral_data("ru")
    assert True


def test_load_en():
    load_numeral_data("en")
    assert True


def test_get_available_languages():
    languages = get_available_languages()
    assert len(languages) > 0
    assert "uk" in languages
    assert "en" in languages
    assert "ru" in languages
