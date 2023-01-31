import re

import pytest

from numeral_converter import int2numeral
from numeral_converter.numeral_converter import MORPH_FORMS


def test_int2numeral_invalid_label():
    msg = re.escape(f"Invalid label; use one of {MORPH_FORMS.keys()}")
    with pytest.raises(ValueError, match=msg):
        int2numeral(2023, lang="uk", form="nominative", num_class="quantitative")


def test_int2numeral_invalid_label_value():
    msg = re.escape(f'Invalid label case value; use one of {MORPH_FORMS["case"]}')
    with pytest.raises(ValueError, match=msg):
        int2numeral(2023, lang="uk", case="nominate", num_class="quantitative")


def test_int2numeral_empty_label_value():
    int2numeral(2023, lang="uk", case=None, num_class=None)
    assert True


def test_int2numeral_one_numeral_form_uk():
    R = int2numeral(2023, lang="uk", case="nominative", num_class="quantitative")
    assert R["numeral"] == "дві тисячі двадцять три"
    assert len(R["numeral_forms"]) == 1
    assert R["numeral_forms"] == [
        R["numeral"],
    ]

    R = int2numeral(5000, lang="uk", case="nominative", num_class="quantitative")
    assert R["numeral"] == "п’ять тисяч"
    assert len(R["numeral_forms"]) == 1
    assert R["numeral_forms"] == [
        R["numeral"],
    ]


def test_int2numeral_one_numeral_form_ru():
    R = int2numeral(2023, lang="ru", case="nominative", num_class="quantitative")
    assert R["numeral"] == "две тысячи двадцать три"
    assert len(R["numeral_forms"]) == 1
    assert R["numeral_forms"] == [
        R["numeral"],
    ]

    R = int2numeral(5000, lang="ru", case="nominative", num_class="quantitative")
    assert R["numeral"] == "пять тысяч"
    assert len(R["numeral_forms"]) == 1
    assert R["numeral_forms"] == [
        R["numeral"],
    ]


def test_int2numeral_several_numeral_forms():
    R = int2numeral(
        2021, lang="uk", case="nominative", gender="neuter", num_class="quantitative"
    )
    assert len(R["numeral_forms"]) == 2
    assert R["numeral_forms"] == [
        "дві тисячі двадцять одне",
        "дві тисячі двадцять одно",
    ]

    R = int2numeral(89, lang="uk", case="prepositional", num_class="quantitative")
    assert len(R["numeral_forms"]) == 4
    assert R["numeral_forms"] == [
        "вісімдесяти дев’яти",
        "вісімдесяти дев’ятьох",
        "вісімдесятьох дев’яти",
        "вісімдесятьох дев’ятьох",
    ]


def test_int2numeral_unknown_number():
    unknown_value = 10 ** (3 * 20)
    msg = f"no data for number {unknown_value}"
    with pytest.raises(ValueError, match=msg):
        int2numeral(
            unknown_value, lang="uk", case="nominative", num_class="quantitative"
        )


def test_int2numeral_invalid_number_form():
    with pytest.warns(UserWarning):
        int2numeral(200, lang="uk", num_class="collective")


def test_int2numeral_numbers_morph_forms():
    # Auto collected from https://www.kyivdictionary.com/uk/words/number-spelling
    assert (
        int2numeral(
            666777888999, lang="uk", case="nominative", num_class="quantitative"
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ять"
    )

    assert (
        int2numeral(666777888999, lang="uk", case="genetive", num_class="quantitative")[
            "numeral"
        ]
        == "шестисот шістдесяти (шістдесятьох) шести (шістьох) мільярдів семисот "
        "сімдесяти (сімдесятьох) семи (сімох) мільйонів восьмисот вісімдесяти "
        "(вісімдесятьох) восьми (вісьмох) тисяч дев’ятисот дев’яноста дев’яти "
        "(дев’ятьох)"
    )

    assert (
        int2numeral(666777888999, lang="uk", case="dative", num_class="quantitative")[
            "numeral"
        ]
        == "шестистам шістдесяти (шістдесятьом) шести (шістьом) мільярдам семистам "
        "сімдесяти (сімдесятьом) семи (сімом) мільйонам восьмистам вісімдесяти "
        "(вісімдесятьом) восьми (вісьмом) тисячам дев’ятистам дев’яноста "
        "дев’яти (дев’ятьом)"
    )

    assert (
        int2numeral(
            666777888999, lang="uk", case="accusative", num_class="quantitative"
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ять (дев’ятьох)"
    )

    assert (
        int2numeral(
            666777888999, lang="uk", case="instrumental", num_class="quantitative"
        )["numeral"]
        == "шістьмастами (шістьомастами) шістдесятьма (шістдесятьома) шістьма "
        "(шістьома) мільярдами сьомастами (сімомастами) сімдесятьма (сімдесятьома) "
        "сімома (сьома) мільйонами вісьмастами (вісьмомастами) вісімдесятьма "
        "(вісімдесятьома) вісьма (вісьмома) тисячами дев’ятьмастами "
        "(дев’ятьомастами) дев’яноста дев’ятьма (дев’ятьома)"
    )

    assert (
        int2numeral(
            666777888999, lang="uk", case="prepositional", num_class="quantitative"
        )["numeral"]
        == "шестистах шістдесяти (шістдесятьох) шести (шістьох) мільярдах семистах "
        "сімдесяти (сімдесятьох) семи (сімох) мільйонах восьмистах вісімдесяти "
        "(вісімдесятьох) восьми (вісьмох) тисячах дев’ятистах дев’яноста дев’яти "
        "(дев’ятьох)"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятий"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ята"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’яте"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’яті"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятого"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятої"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятого"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятих"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="dative",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятому"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="dative",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятій"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="dative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятому"
    )

    assert (
        int2numeral(
            666777888999, lang="uk", case="dative", num_class="ordinal", number="plural"
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятим"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятий (дев’ятого)"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’яту"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’яте"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’яті (дев’ятих)"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятим"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятою"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятим"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятими"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятому (дев’ятім)"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятій"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятому (дев’ятім)"
    )

    assert (
        int2numeral(
            666777888999,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "шістсот шістдесят шість мільярдів сімсот сімдесят сім мільйонів вісімсот "
        "вісімдесят вісім тисяч дев’ятсот дев’яносто дев’ятих"
    )

    assert (
        int2numeral(
            221222333444555, lang="uk", case="nominative", num_class="quantitative"
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста тридцять "
        "три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ять"
    )

    assert (
        int2numeral(
            221222333444555, lang="uk", case="genetive", num_class="quantitative"
        )["numeral"]
        == "двохсот двадцяти (двадцятьох) одного трильйона двохсот двадцяти "
        "(двадцятьох) двох мільярдів трьохсот тридцяти (тридцятьох) трьох мільйонів "
        "чотирьохсот сорока чотирьох тисяч п’ятисот п’ятдесяти (п’ятдесятьох) "
        "п’яти (п’ятьох)"
    )

    assert (
        int2numeral(
            221222333444555, lang="uk", case="dative", num_class="quantitative"
        )["numeral"]
        == "двомстам двадцяти (двадцятьом) одному трильйону (трильйонові) двомстам "
        "двадцяти (двадцятьом) двом мільярдам трьомстам тридцяти (тридцятьом) "
        "трьом мільйонам чотирьомстам сорока чотирьом тисячам п’ятистам п’ятдесяти "
        "(п’ятдесятьом) п’яти (п’ятьом)"
    )

    assert (
        int2numeral(
            221222333444555, lang="uk", case="accusative", num_class="quantitative"
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста тридцять "
        "три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят "
        "(п’ятдесятьох) п’ять (п’ятьох)"
    )

    assert (
        int2numeral(
            221222333444555, lang="uk", case="instrumental", num_class="quantitative"
        )["numeral"]
        == "двомастами двадцятьма (двадцятьома) одним трильйоном двомастами "
        "двадцятьма (двадцятьома) двома мільярдами трьомастами тридцятьма "
        "(тридцятьома) трьома мільйонами чотирмастами сорока чотирма тисячами "
        "п’ятьмастами (п’ятьомастами) п’ятдесятьма (п’ятдесятьома) п’ятьма (п’ятьома)"
    )

    assert (
        int2numeral(
            221222333444555, lang="uk", case="prepositional", num_class="quantitative"
        )["numeral"]
        == "двохстах двадцяти (двадцятьох) одному (однім) трильйоні двохстах двадцяти "
        "(двадцятьох) двох мільярдах трьохстах тридцяти (тридцятьох) трьох "
        "мільйонах чотирьохстах сорока чотирьох тисячах п’ятистах п’ятдесяти "
        "(п’ятдесятьох) п’яти (п’ятьох)"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятий"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ята"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’яте"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’яті"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятого"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятої"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятого"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятих"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="dative",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятому"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="dative",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятій"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="dative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятому"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="dative",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятим"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят "
        "п’ятий (п’ятого)"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’яту"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’яте"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят "
        "п’яті (п’ятих)"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятим"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятою"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятим"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятими"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят "
        "п’ятому (п’ятім)"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятій"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят "
        "п’ятому (п’ятім)"
    )

    assert (
        int2numeral(
            221222333444555,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "двісті двадцять один трильйон двісті двадцять два мільярди триста "
        "тридцять три мільйони чотириста сорок чотири тисячі п’ятсот п’ятдесят п’ятих"
    )

    assert (
        int2numeral(
            111212313415515, lang="uk", case="nominative", num_class="quantitative"
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцять"
    )

    assert (
        int2numeral(
            111212313415515, lang="uk", case="genetive", num_class="quantitative"
        )["numeral"]
        == "ста одинадцяти (одинадцятьох) трильйонів двохсот дванадцяти (дванадцятьох) "
        "мільярдів трьохсот тринадцяти (тринадцятьох) мільйонів чотирьохсот "
        "п’ятнадцяти (п’ятнадцятьох) тисяч п’ятисот п’ятнадцяти (п’ятнадцятьох)"
    )

    assert (
        int2numeral(
            111212313415515, lang="uk", case="dative", num_class="quantitative"
        )["numeral"]
        == "ста одинадцяти (одинадцятьом) трильйонам двомстам дванадцяти "
        "(дванадцятьом) мільярдам трьомстам тринадцяти (тринадцятьом) мільйонам "
        "чотирьомстам п’ятнадцяти (п’ятнадцятьом) тисячам п’ятистам "
        "п’ятнадцяти (п’ятнадцятьом)"
    )

    assert (
        int2numeral(
            111212313415515, lang="uk", case="accusative", num_class="quantitative"
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцять (п’ятнадцятьох)"
    )

    assert (
        int2numeral(
            111212313415515, lang="uk", case="instrumental", num_class="quantitative"
        )["numeral"]
        == "ста одинадцятьма (одинадцятьома) трильйонами двомастами дванадцятьма "
        "(дванадцятьома) мільярдами трьомастами тринадцятьма (тринадцятьома) "
        "мільйонами чотирмастами п’ятнадцятьма (п’ятнадцятьома) тисячами "
        "п’ятьмастами (п’ятьомастами) п’ятнадцятьма (п’ятнадцятьома)"
    )

    assert (
        int2numeral(
            111212313415515, lang="uk", case="prepositional", num_class="quantitative"
        )["numeral"]
        == "ста одинадцяти (одинадцятьох) трильйонах двохстах дванадцяти "
        "(дванадцятьох) мільярдах трьохстах тринадцяти (тринадцятьох) мільйонах "
        "чотирьохстах п’ятнадцяти (п’ятнадцятьох) тисячах п’ятистах п’ятнадцяти "
        "(п’ятнадцятьох)"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятий"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцята"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцяте"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцяті"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятого"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятої"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятого"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятих"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="dative",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятому"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="dative",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятій"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="dative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятому"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="dative",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятим"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятий (п’ятнадцятого)"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцяту"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцяте"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцяті (п’ятнадцятих)"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятим"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятою"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятим"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятими"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятому (п’ятнадцятім)"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятій"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятому (п’ятнадцятім)"
    )

    assert (
        int2numeral(
            111212313415515,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "сто одинадцять трильйонів двісті дванадцять мільярдів триста тринадцять "
        "мільйонів чотириста п’ятнадцять тисяч п’ятсот п’ятнадцятих"
    )

    assert (
        int2numeral(
            616717818919, lang="uk", case="nominative", num_class="quantitative"
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцять"
    )

    assert (
        int2numeral(616717818919, lang="uk", case="genetive", num_class="quantitative")[
            "numeral"
        ]
        == "шестисот шістнадцяти (шістнадцятьох) мільярдів семисот сімнадцяти "
        "(сімнадцятьох) мільйонів восьмисот вісімнадцяти (вісімнадцятьох) "
        "тисяч дев’ятисот дев’ятнадцяти (дев’ятнадцятьох)"
    )

    assert (
        int2numeral(616717818919, lang="uk", case="dative", num_class="quantitative")[
            "numeral"
        ]
        == "шестистам шістнадцяти (шістнадцятьом) мільярдам семистам сімнадцяти "
        "(сімнадцятьом) мільйонам восьмистам вісімнадцяти (вісімнадцятьом) тисячам "
        "дев’ятистам дев’ятнадцяти (дев’ятнадцятьом)"
    )

    assert (
        int2numeral(
            616717818919, lang="uk", case="accusative", num_class="quantitative"
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцять (дев’ятнадцятьох)"
    )

    assert (
        int2numeral(
            616717818919, lang="uk", case="instrumental", num_class="quantitative"
        )["numeral"]
        == "шістьмастами (шістьомастами) шістнадцятьма (шістнадцятьома) мільярдами "
        "сьомастами (сімомастами) сімнадцятьма (сімнадцятьома) мільйонами "
        "вісьмастами (вісьмомастами) вісімнадцятьма (вісімнадцятьома) тисячами "
        "дев’ятьмастами (дев’ятьомастами) дев’ятнадцятьма (дев’ятнадцятьома)"
    )

    assert (
        int2numeral(
            616717818919, lang="uk", case="prepositional", num_class="quantitative"
        )["numeral"]
        == "шестистах шістнадцяти (шістнадцятьох) мільярдах семистах сімнадцяти "
        "(сімнадцятьох) мільйонах восьмистах вісімнадцяти (вісімнадцятьох) "
        "тисячах дев’ятистах дев’ятнадцяти (дев’ятнадцятьох)"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятий"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцята"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцяте"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="nominative",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцяті"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятого"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятої"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятого"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="genetive",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятих"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="dative",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятому"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="dative",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятій"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="dative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятому"
    )

    assert (
        int2numeral(
            616717818919, lang="uk", case="dative", num_class="ordinal", number="plural"
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятим"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятий (дев’ятнадцятого)"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцяту"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцяте"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцяті (дев’ятнадцятих)"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятим"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятою"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятим"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="instrumental",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятими"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятому (дев’ятнадцятім)"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятій"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятому (дев’ятнадцятім)"
    )

    assert (
        int2numeral(
            616717818919,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            number="plural",
        )["numeral"]
        == "шістсот шістнадцять мільярдів сімсот сімнадцять мільйонів вісімсот "
        "вісімнадцять тисяч дев’ятсот дев’ятнадцятих"
    )

    assert (
        int2numeral(
            1,
            lang="uk",
            case="nominative",
            num_class="quantitative",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "одне (одно)"
    )

    assert (
        int2numeral(
            1,
            lang="uk",
            case="instrumental",
            num_class="quantitative",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "однією (одною)"
    )

    assert (
        int2numeral(
            3,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "третій"
    )

    assert (
        int2numeral(
            4,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "четверте"
    )

    assert (
        int2numeral(7, lang="uk", case="instrumental", num_class="quantitative")[
            "numeral"
        ]
        == "сімома (сьома)"
    )

    assert (
        int2numeral(9, lang="uk", case="prepositional", num_class="quantitative")[
            "numeral"
        ]
        == "дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(
            13, lang="uk", case="accusative", num_class="ordinal", number="plural"
        )["numeral"]
        == "тринадцяті (тринадцятих)"
    )

    assert (
        int2numeral(
            21,
            lang="uk",
            case="nominative",
            num_class="quantitative",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "двадцять одне (одно)"
    )

    assert (
        int2numeral(
            21,
            lang="uk",
            case="instrumental",
            num_class="quantitative",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "двадцятьма (двадцятьома) однією (одною)"
    )

    assert (
        int2numeral(
            23,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "двадцять третій"
    )

    assert (
        int2numeral(
            24,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "двадцять четверте"
    )

    assert (
        int2numeral(27, lang="uk", case="instrumental", num_class="quantitative")[
            "numeral"
        ]
        == "двадцятьма (двадцятьома) сімома (сьома)"
    )

    assert (
        int2numeral(29, lang="uk", case="prepositional", num_class="quantitative")[
            "numeral"
        ]
        == "двадцяти (двадцятьох) дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(30, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "тридцять (тридцятьох)"
    )

    assert (
        int2numeral(
            31,
            lang="uk",
            case="nominative",
            num_class="quantitative",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "тридцять одне (одно)"
    )

    assert (
        int2numeral(
            31,
            lang="uk",
            case="accusative",
            num_class="quantitative",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "тридцять (тридцятьох) один (одного)"
    )

    assert (
        int2numeral(
            31,
            lang="uk",
            case="accusative",
            num_class="quantitative",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "тридцять (тридцятьох) одну"
    )

    assert (
        int2numeral(
            31,
            lang="uk",
            case="accusative",
            num_class="quantitative",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "тридцять (тридцятьох) одне"
    )

    assert (
        int2numeral(
            31, lang="uk", case="accusative", num_class="quantitative", number="plural"
        )["numeral"]
        == "тридцять (тридцятьох) одні (одних)"
    )

    assert (
        int2numeral(
            31,
            lang="uk",
            case="instrumental",
            num_class="quantitative",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "тридцятьма (тридцятьома) однією (одною)"
    )

    assert (
        int2numeral(32, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "тридцять (тридцятьох) два (двох)"
    )

    assert (
        int2numeral(
            32,
            lang="uk",
            case="accusative",
            num_class="quantitative",
            gender="feminine",
        )["numeral"]
        == "тридцять (тридцятьох) дві (двох)"
    )

    assert (
        int2numeral(33, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "тридцять (тридцятьох) три (трьох)"
    )

    assert (
        int2numeral(
            33,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "тридцять третій"
    )

    assert (
        int2numeral(34, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "тридцять (тридцятьох) чотири (чотирьох)"
    )

    assert (
        int2numeral(
            34,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "тридцять четверте"
    )

    assert (
        int2numeral(35, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "тридцять (тридцятьох) п’ять (п’ятьох)"
    )

    assert (
        int2numeral(36, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "тридцять (тридцятьох) шість (шістьох)"
    )

    assert (
        int2numeral(37, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "тридцять (тридцятьох) сім (сімох)"
    )

    assert (
        int2numeral(37, lang="uk", case="instrumental", num_class="quantitative")[
            "numeral"
        ]
        == "тридцятьма (тридцятьома) сімома (сьома)"
    )

    assert (
        int2numeral(38, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "тридцять (тридцятьох) вісім (вісьмох)"
    )

    assert (
        int2numeral(39, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "тридцять (тридцятьох) дев’ять (дев’ятьох)"
    )

    assert (
        int2numeral(39, lang="uk", case="prepositional", num_class="quantitative")[
            "numeral"
        ]
        == "тридцяти (тридцятьох) дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(40, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "сорок"
    )

    assert (
        int2numeral(
            41,
            lang="uk",
            case="nominative",
            num_class="quantitative",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "сорок одне (одно)"
    )

    assert (
        int2numeral(
            41,
            lang="uk",
            case="accusative",
            num_class="quantitative",
            gender="masculine",
            number="singular",
        )["numeral"]
        == "сорок один (одного)"
    )

    assert (
        int2numeral(
            41,
            lang="uk",
            case="accusative",
            num_class="quantitative",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "сорок одну"
    )

    assert (
        int2numeral(
            41,
            lang="uk",
            case="accusative",
            num_class="quantitative",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "сорок одне"
    )

    assert (
        int2numeral(
            41, lang="uk", case="accusative", num_class="quantitative", number="plural"
        )["numeral"]
        == "сорок одні (одних)"
    )

    assert (
        int2numeral(
            41,
            lang="uk",
            case="instrumental",
            num_class="quantitative",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "сорока однією (одною)"
    )

    assert (
        int2numeral(42, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "сорок два (двох)"
    )

    assert (
        int2numeral(
            42,
            lang="uk",
            case="accusative",
            num_class="quantitative",
            gender="feminine",
        )["numeral"]
        == "сорок дві (двох)"
    )

    assert (
        int2numeral(43, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "сорок три (трьох)"
    )

    assert (
        int2numeral(
            43,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "сорок третій"
    )

    assert (
        int2numeral(44, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "сорок чотири (чотирьох)"
    )

    assert (
        int2numeral(
            44,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "сорок четверте"
    )

    assert (
        int2numeral(45, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "сорок п’ять (п’ятьох)"
    )

    assert (
        int2numeral(46, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "сорок шість (шістьох)"
    )

    assert (
        int2numeral(47, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "сорок сім (сімох)"
    )

    assert (
        int2numeral(47, lang="uk", case="instrumental", num_class="quantitative")[
            "numeral"
        ]
        == "сорока сімома (сьома)"
    )

    assert (
        int2numeral(48, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "сорок вісім (вісьмох)"
    )

    assert (
        int2numeral(49, lang="uk", case="accusative", num_class="quantitative")[
            "numeral"
        ]
        == "сорок дев’ять (дев’ятьох)"
    )

    assert (
        int2numeral(49, lang="uk", case="prepositional", num_class="quantitative")[
            "numeral"
        ]
        == "сорока дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(
            50, lang="uk", case="genetive", num_class="ordinal", number="plural"
        )["numeral"]
        == "п’ятдесятих"
    )

    assert (
        int2numeral(
            51,
            lang="uk",
            case="nominative",
            num_class="quantitative",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "п’ятдесят одне (одно)"
    )

    assert (
        int2numeral(
            51,
            lang="uk",
            case="instrumental",
            num_class="quantitative",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "п’ятдесятьма (п’ятдесятьома) однією (одною)"
    )

    assert (
        int2numeral(
            53,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "п’ятдесят третій"
    )

    assert (
        int2numeral(
            54,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "п’ятдесят четверте"
    )

    assert (
        int2numeral(57, lang="uk", case="instrumental", num_class="quantitative")[
            "numeral"
        ]
        == "п’ятдесятьма (п’ятдесятьома) сімома (сьома)"
    )

    assert (
        int2numeral(59, lang="uk", case="prepositional", num_class="quantitative")[
            "numeral"
        ]
        == "п’ятдесяти (п’ятдесятьох) дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(
            61,
            lang="uk",
            case="nominative",
            num_class="quantitative",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "шістдесят одне (одно)"
    )

    assert (
        int2numeral(
            61,
            lang="uk",
            case="instrumental",
            num_class="quantitative",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "шістдесятьма (шістдесятьома) однією (одною)"
    )

    assert (
        int2numeral(
            63,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "шістдесят третій"
    )

    assert (
        int2numeral(
            64,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "шістдесят четверте"
    )

    assert (
        int2numeral(67, lang="uk", case="instrumental", num_class="quantitative")[
            "numeral"
        ]
        == "шістдесятьма (шістдесятьома) сімома (сьома)"
    )

    assert (
        int2numeral(69, lang="uk", case="prepositional", num_class="quantitative")[
            "numeral"
        ]
        == "шістдесяти (шістдесятьох) дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(
            71,
            lang="uk",
            case="nominative",
            num_class="quantitative",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "сімдесят одне (одно)"
    )

    assert (
        int2numeral(
            71,
            lang="uk",
            case="instrumental",
            num_class="quantitative",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "сімдесятьма (сімдесятьома) однією (одною)"
    )

    assert (
        int2numeral(
            73,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "сімдесят третій"
    )

    assert (
        int2numeral(
            74,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "сімдесят четверте"
    )

    assert (
        int2numeral(77, lang="uk", case="instrumental", num_class="quantitative")[
            "numeral"
        ]
        == "сімдесятьма (сімдесятьома) сімома (сьома)"
    )

    assert (
        int2numeral(79, lang="uk", case="prepositional", num_class="quantitative")[
            "numeral"
        ]
        == "сімдесяти (сімдесятьох) дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(
            81,
            lang="uk",
            case="nominative",
            num_class="quantitative",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "вісімдесят одне (одно)"
    )

    assert (
        int2numeral(
            81,
            lang="uk",
            case="instrumental",
            num_class="quantitative",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "вісімдесятьма (вісімдесятьома) однією (одною)"
    )

    assert (
        int2numeral(
            83,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "вісімдесят третій"
    )

    assert (
        int2numeral(
            84,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "вісімдесят четверте"
    )

    assert (
        int2numeral(87, lang="uk", case="instrumental", num_class="quantitative")[
            "numeral"
        ]
        == "вісімдесятьма (вісімдесятьома) сімома (сьома)"
    )

    assert (
        int2numeral(89, lang="uk", case="prepositional", num_class="quantitative")[
            "numeral"
        ]
        == "вісімдесяти (вісімдесятьох) дев’яти (дев’ятьох)"
    )

    assert (
        int2numeral(
            91,
            lang="uk",
            case="nominative",
            num_class="quantitative",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "дев’яносто одне (одно)"
    )

    assert (
        int2numeral(
            91,
            lang="uk",
            case="instrumental",
            num_class="quantitative",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "дев’яноста однією (одною)"
    )

    assert (
        int2numeral(
            93,
            lang="uk",
            case="prepositional",
            num_class="ordinal",
            gender="feminine",
            number="singular",
        )["numeral"]
        == "дев’яносто третій"
    )

    assert (
        int2numeral(
            94,
            lang="uk",
            case="accusative",
            num_class="ordinal",
            gender="neuter",
            number="singular",
        )["numeral"]
        == "дев’яносто четверте"
    )

    assert (
        int2numeral(97, lang="uk", case="instrumental", num_class="quantitative")[
            "numeral"
        ]
        == "дев’яноста сімома (сьома)"
    )

    assert (
        int2numeral(99, lang="uk", case="prepositional", num_class="quantitative")[
            "numeral"
        ]
        == "дев’яноста дев’яти (дев’ятьох)"
    )
