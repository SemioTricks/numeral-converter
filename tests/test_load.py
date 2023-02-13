import pytest

from numeral_converter import (
    get_available_languages,
    load_numeral_data,
    maximum_number_order_to_convert,
)


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


def test_maximum_number_order_to_convert():
    assert maximum_number_order_to_convert("uk") > 10
    assert maximum_number_order_to_convert("ru") > 10
    assert maximum_number_order_to_convert("en") > 10
