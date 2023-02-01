import pytest

from numeral_converter import numeral2int


def test_numeral2int():
    assert numeral2int("сто сорок дві тисячи тридцять один", lang="uk") == 142031
    assert numeral2int("сто сорок две тысячи тридцать один", lang="ru") == 142031
    assert numeral2int("one hundred forty-two thousand thirty-one", lang="en") == 142031
    assert (
        numeral2int("one hundred and forty-two thousand and thirty-one", lang="en")
        == 142031
    )


def test_numeral2int_scale_of_scales():
    assert numeral2int("сто тисяч мільйонів", lang="uk") == 100000000000
    assert numeral2int("сто тисяч", lang="uk") == 100000


def test_numeral2int_scale_of_scales_en():
    assert numeral2int("one hundred thousand million", lang="en") == 100000000000
    assert numeral2int("one hundred thousand", lang="en") == 100000


def test_numeral2int_scale():
    assert numeral2int("три десятки", lang="uk") == 30
    assert numeral2int("три тисячі три сотні три десятки три", lang="uk") == 3333


def test_numeral2int_diff_morph_forms():
    assert numeral2int("сорок два", lang="uk") == 42
    assert numeral2int("сорока двох", lang="uk") == 42
    assert numeral2int("сорок другий", lang="uk") == 42
    assert numeral2int("сорок другій", lang="uk") == 42


def test_numeral2int_invalid_numeral():
    msg = (
        "position 1: order of 1000000000:9 "
        "is less/equal of summary order in next group: 9"
    )
    with pytest.raises(ValueError, match=msg):
        numeral2int("три мільярди тисяча пятдесят пять мільонів", lang="uk")


def test_numeral2int_spelling_invalid_numeral():
    msg = "the number in the middle of the numeral cannot be ordinal"
    with pytest.raises(ValueError, match=msg):
        numeral2int("три мільярди тисячний пятдесят пятий мільон", lang="uk")


def test_numeral2int_not_number():
    msg = 'can\'t convert "роки" to integer'
    with pytest.raises(ValueError, match=msg):
        numeral2int("дві тисячі двадцять три роки", lang="uk")


def test_numeral2int_spelly():
    assert numeral2int("дви тисичи двадцить тре", lang="ru") == 2023

    assert numeral2int("дви тисичи двадцить тре", lang="uk") == 2023

    assert numeral2int("two thousend twenti tree", lang="en") == 2023
