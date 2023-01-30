import pytest

from numeral_converter.numeral_converter import int2numeral_word


def test_default_value():
    R = int2numeral_word(12, lang="uk")
    assert R["numeral_word"] == "дванадцять"


def test_morph_forms():
    R = int2numeral_word(12, lang="uk", num_class="ordinal", gender="feminine")
    assert R["numeral_word"] == "дванадцята"

    R = int2numeral_word(12, lang="uk", num_class="ordinal", gender="masculine")
    assert R["numeral_word"] == "дванадцятий"

    R = int2numeral_word(
        12, lang="uk", num_class="ordinal", number="plural", gender="masculine"
    )
    assert R["numeral_word"] == "дванадцяті"


def test_not_number():
    with pytest.raises(ValueError):
        int2numeral_word(22)
