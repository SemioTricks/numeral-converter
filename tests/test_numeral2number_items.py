import pytest

from numeral_converter.numeral_converter import numeral2number_items


def test_numeral2number_items_uk():

    R = numeral2number_items(
        "двісти тридцать чотири тисячі шістот п’ятнадцять", lang="uk"
    )
    assert len(R) == 6
    assert R[0].value == 200
    assert R[1].value == 30
    assert R[2].value == 4
    assert R[3].value == 1000
    assert R[4].value == 600
    assert R[5].value == 15

    R = numeral2number_items(
        "три мільони шість тисяч шістдесят сім мільон двісті двадцясь "
        "сім тисяч сто тридцять чотири",
        lang="uk",
    )
    assert len(R) == 14

    R = numeral2number_items("сто сорок дві тисячі тридцять один", lang="uk")
    assert len(R) == 6
    assert R[0].value == 100
    assert R[1].value == 40
    assert R[2].value == 2
    assert R[3].value == 1000
    assert R[4].value == 30
    assert R[5].value == 1

    R = numeral2number_items("тисяча сорок дві тисячі", lang="uk")
    assert len(R) == 4
    assert R[0].value == 1000
    assert R[1].value == 40
    assert R[2].value == 2
    assert R[3].value == 1000

    R = numeral2number_items("дванадцять сотня", lang="uk")
    assert len(R) == 2
    assert R[0].value == 12
    assert R[1].value == 100

    R = numeral2number_items("one hundred forty-two thousand thirty-one", lang="en")
    assert R[0].value == 1
    assert R[1].value == 100
    assert R[1].scale
    assert R[2].value == 40
    assert R[3].value == 2
    assert R[4].value == 1000
    assert R[4].scale
    assert R[5].value == 30
    assert R[6].value == 1


def test_numeral2number_items_ru():

    R = numeral2number_items(
        "двести тридцать четыре тысячи шестьсот пятнадцать", lang="ru"
    )
    assert len(R) == 6
    assert R[0].value == 200
    assert R[1].value == 30
    assert R[2].value == 4
    assert R[3].value == 1000
    assert R[4].value == 600
    assert R[5].value == 15

    R = numeral2number_items(
        "три миллиона шесть тысяч шестдесят семь миллионов двести двадцать семь тысяч "
        "сто тридцать четыре",
        lang="ru",
    )
    assert len(R) == 14

    R = numeral2number_items("сто сорок две тисячи тридцать один", lang="ru")
    assert len(R) == 6
    assert R[0].value == 100
    assert R[1].value == 40
    assert R[2].value == 2
    assert R[3].value == 1000
    assert R[4].value == 30
    assert R[5].value == 1

    R = numeral2number_items("тысяча сорок две тысячи", lang="ru")
    assert len(R) == 4
    assert R[0].value == 1000
    assert R[1].value == 40
    assert R[2].value == 2
    assert R[3].value == 1000

    R = numeral2number_items("двенадцать сто", lang="ru")
    assert len(R) == 2
    assert R[0].value == 12
    assert R[1].value == 100


def test_numeral2number_items_with_not_number():
    msg = 'can\'t convert "варіант" to integer'
    with pytest.raises(ValueError, match=msg):
        numeral2number_items("перший варіант", lang="uk")
