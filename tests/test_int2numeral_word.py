import pytest

from numeral_converter.numeral_converter import int2numeral_word


def test_int2numeral_word_existing_number_word_with_one_form():
    R = int2numeral_word(12, lang="uk")
    assert R.default == "дванадцять"
    assert len(R.alt) == 0


def test_int2numeral_word_existing_number_word_with_several_forms():
    R = int2numeral_word(7, lang="uk", case="dative")
    assert len(R.alt) == 1
    assert R.alt == [
        "сімом",
    ]


def test_int2numeral_word_converting_in_different_morph_forms():
    R = int2numeral_word(12, lang="uk", num_class="ordinal", gender="feminine")
    assert R.default == "дванадцята"

    R = int2numeral_word(12, lang="uk", num_class="ordinal", gender="masculine")
    assert R.default == "дванадцятий"

    R = int2numeral_word(
        12, lang="uk", num_class="ordinal", number="plural", gender="masculine"
    )
    assert R.default == "дванадцяті"


def test_int2numeral_word_converting_in_not_full_morph_form():
    msg = r"There are more then one values for number 1000 .+"
    with pytest.raises(ValueError, match=msg):
        int2numeral_word(1000, lang="uk")


def test_int2numeral_word_number_without_data():
    msg = "no data for number 42"
    with pytest.raises(ValueError, match=msg):
        int2numeral_word(42, lang="uk")
