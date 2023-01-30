import pytest

from numeral_converter import numeral2int


def test_correct():
    assert numeral2int("сто сорок дві тисячи тридцять один", lang="uk") == 142031

    assert numeral2int("сто тисяч мільйонів", lang="uk") == 100000000000

    assert numeral2int("сто тисяч", lang="uk") == 100000

    assert numeral2int("три десятки", lang="uk") == 30
    assert numeral2int("три тисячі три сотні три десятки три", lang="uk") == 3333


def test_correct_diff_morph_forms():
    assert numeral2int("сорок два", lang="uk") == 42
    assert numeral2int("сорока двох", lang="uk") == 42
    assert numeral2int("сорок другий", lang="uk") == 42
    assert numeral2int("сорок другій", lang="uk") == 42


def test_non_correct():
    msg = (
        "position 1: order of 1000000000:9 "
        "is less/equal of summary order in next group: 9"
    )
    with pytest.raises(ValueError, match=msg):
        numeral2int("три мільярди тисяча пятдесят пять мільонів", lang="uk")
