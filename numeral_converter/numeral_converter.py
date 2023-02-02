import logging
import math
import re
import warnings
from collections import namedtuple
from typing import Any, Dict, List, Optional

from .constants import DEFAULT_MORPH, MORPH_FORMS
from .lang_data_loader import NUMERAL_DATA, NUMERAL_TREE, check_numeral_data_load
from .utils import combinations

NumberItem = namedtuple("NumberItem", "value order scale")
NumeralWord = namedtuple("NumeralWord", "default alt")


logger = logging.getLogger(__name__)


def numeral2int(numeral: str, lang: str) -> Optional[int]:
    """
    Converts input numeral in language `lang` into integer value

    :param numeral: input numeral in language `lang`
    :param lang: language
    :return Optional [int]: integer value or None if nothing found

    :Example:

    >>> from numeral_converter import load_numeral_data, numeral2int

    >>> load_numeral_data("uk")
    >>> numeral2int("сорок два", lang="uk")
    42

    >>> # different morph forms
    >>> numeral2int("сорок другий", lang="uk")
    42

    >>> # spell checking
    >>> numeral2int("сороак двоіх", lang="uk")
    42

    # another languages
    >>> load_numeral_data("ru")
    >>> numeral2int("сорок второй", lang="uk")
    42

    >>> load_numeral_data("en")
    >>> numeral2int("forty two", lang="uk")
    42

    """
    number_items = numeral2number_items(numeral=numeral, lang=lang)
    value = number_items2int(number_items=number_items)
    return value


def int2numeral(value: int, lang: str, **kwargs):
    """
    Converts input integer number into a numeral in language `lang`
    into a morphological form given by the argument-parameters:
        "case": 'accusative', 'dative', 'genetive', 'instrumental', 'nominative' or
                'prepositional';
        "num_class": 'collective', 'ordinal' or 'quantitative';
        "gender": 'feminine', 'masculine' or 'neuter';
        "number": 'plural' or 'singular'.

    :param value: input integer value
    :param lang: language identifier
    :return str: string numeral in language `lang` in a morphological form
            given by the argument-parameters

    :Example:

    >>> from numeral_converter import load_numeral_data, int2numeral
    >>> load_numeral_data("uk")

    >>> int2numeral(42, case="nominative", num_class="quantitative")
    {
        'numeral': 'сорок два',
        'numeral_forms': ['сорок два', ]
    }

    >>> int2numeral(42, lang='uk', case="nominative", num_class="quantitative")
    {'numeral': 'сорок два', 'numeral_forms': ['сорок два']}

    >>> int2numeral(42, lang='uk', case="genetive", num_class="quantitative")
    {'numeral': 'сорока двох', 'numeral_forms': ['сорока двох']}

    >>> int2numeral(
    ...     42, lang='uk', case="dative", num_class="ordinal", gender='feminine')
    {'numeral': 'сорок другій', 'numeral_forms': ['сорок другій']}

    """
    __check_kwargs(kwargs)

    numeral_items = int2number_items(value)
    numeral = number_items2numeral(
        numeral_items,
        lang=lang,
        case=kwargs.get("case"),
        num_class=kwargs.get("num_class"),
        gender=kwargs.get("gender"),
        number=kwargs.get("number"),
    )

    return numeral


def numeral2number_items(numeral: str, lang: str):
    check_numeral_data_load(lang)
    numeral = __preprocess_numeral(numeral, lang)

    number_items: List[NumberItem] = list()

    for i, number_word in enumerate(numeral.split(" ")[::-1]):
        number_word_info = NUMERAL_TREE[lang].get(number_word)
        if not len(number_word_info):
            raise ValueError(f'can\'t convert "{number_word}" to integer')

        if i > 0:
            number_word_info = __delete_ordinal_from_numeral_word_info(number_word_info)
            if not len(number_word_info):
                raise ValueError(f'ordinal numeral word "{number_word}" inside numeral')

        number_items.insert(
            0,
            NumberItem(
                value=number_word_info[0]["value"]["value"],
                order=number_word_info[0]["value"]["order"],
                scale=number_word_info[0]["value"]["scale"],
            ),
        )

    return number_items


def number_items2int(number_items: List[NumberItem]) -> int:
    int_value = 0
    number_items = number_items[::-1]

    i = __scale_group_start = __scale_order = 0
    if number_items[0].scale is not None:
        i = __scale_group_start = 1
        __scale_order = number_items[0].order

    while i < len(number_items):

        __scale_order_found = None

        while (
            i < len(number_items)
            and (__scale_order > 0 or number_items[i].order < 3)
            and (number_items[i].scale is None or number_items[i].order < __scale_order)
        ):
            if number_items[i].scale and (
                __scale_order_found is None
                or __scale_order_found < number_items[i].order
            ):
                __scale_order_found = number_items[i].order

            i += 1

        if __scale_order_found:

            for k in range(__scale_group_start + 1, i):
                __order = (
                    0
                    if number_items[k].value % 10 ** number_items[k].order
                    else number_items[k].order
                )
                if number_items[k - 1].order == __order:
                    raise ValueError(
                        f"position {len(number_items) - k}: {number_items[k - 1].value}"
                        f" with order {number_items[k - 1].order} stands after "
                        f"{number_items[k].value} with equal order {__order}"
                    )

            int_value += (10**__scale_order) * number_items2int(
                number_items[__scale_group_start:i][::-1]
            )
        else:
            for k in range(__scale_group_start + 1, i):
                __order = (
                    0
                    if number_items[k].value % 10 ** number_items[k].order
                    else number_items[k].order
                )
                if number_items[k - 1].order >= __order:
                    raise ValueError(
                        f"position {len(number_items) - k}: {number_items[k - 1].value}"
                        f" with order {number_items[k - 1].order} stands after "
                        f"{number_items[k].value} with less/equal order {__order}"
                    )

            __n = sum([x.value for x in number_items[__scale_group_start:i]])
            __n = (10**__scale_order) * __n if __n else 10**__scale_order
            int_value += __n

            __scale_group_start = None

        if i >= len(number_items):
            return int_value

        if not number_items[i].scale:
            raise ValueError(
                f"position {len(number_items) - 1 - i}: expects 10^(3n) or 100; "
                f"found {number_items[i].value}"
            )

        __value_order = int(math.log10(int_value))
        if number_items[i].order <= __value_order:
            raise ValueError(
                f"position {len(number_items) - 1 - i}: order of "
                f"{number_items[i].value}:{number_items[i].order} "
                f"is less/equal of summary order in next group: {__value_order}"
            )

        __scale_order = number_items[i].order

        __scale_group_start = i + 1

        i += 1

    if __scale_group_start is not None:
        int_value += 10**__scale_order

    return int_value


def int2number_items(number: int) -> List[NumberItem]:
    number_items: List[NumberItem] = list()

    __order = 0
    __ones = None

    __number = number

    while __number:

        digit = __number % 10

        if __order % 3 == 2:

            value = 100 * digit
            if value:
                number_items.insert(0, NumberItem(value, __order % 3, None))

        elif __order % 3 == 0:

            if __order > 0:
                number_items.insert(0, NumberItem(10**__order, __order, True))

            __ones = digit

        else:

            if digit == 1 and __ones > 0:

                value = 10 * digit + __ones
                if value:
                    number_items.insert(0, NumberItem(value, __order % 3, None))
            else:

                value = __ones
                if value:
                    number_items.insert(0, NumberItem(value, 0, None))

                value = 10 * digit
                if value:
                    number_items.insert(0, NumberItem(value, __order % 3, None))

            __ones = None

        __order += 1
        __number = __number // 10

    if __ones:
        number_items.insert(0, NumberItem(__ones, 0, None))

    return number_items


def int2numeral_word(value: int, lang: str, **kwargs) -> NumeralWord:
    __check_kwargs(kwargs)
    check_numeral_data_load(lang)

    sub_data = NUMERAL_DATA[lang][NUMERAL_DATA[lang].value == value]

    if sub_data.shape[0] == 0:
        raise ValueError(f"no data for number {value}")

    for label, default in DEFAULT_MORPH.items():
        label_value = kwargs.get(label) or default
        if label_value and label not in NUMERAL_DATA[lang].columns:
            warnings.warn(
                f'no column "{label}" in data for language "{lang}"; ignored',
                UserWarning,
            )

        if label_value and label in sub_data.columns:
            if label_value in sub_data[label].values:
                sub_data = sub_data[sub_data[label] == label_value]
            elif kwargs.get(label):
                warnings.warn(
                    f"no data for {label} == {kwargs.get(label)}; ignored", UserWarning
                )
    if sub_data.shape[0] != 1:
        val_info = (
            f"number {value} ("
            + ", ".join(
                [
                    f'{label} = "{kwargs.get(label) or default}"'
                    for label, default in DEFAULT_MORPH.items()
                    if (kwargs.get(label) or default)
                ]
            )
            + ")"
        )

        if sub_data.shape[0] == 0:
            raise ValueError(f"No data for {val_info}")

        if sub_data.shape[0] > 1:
            raise ValueError(
                f"There are more then one values for {val_info}:\n" f"{sub_data.head()}"
            )

    numeral_words = [x.strip() for x in sub_data.iloc[0].string.split(" ") if x]

    return NumeralWord(numeral_words[0], numeral_words[1:])


def number_items2numeral(number_items: List[NumberItem], lang: str, **kwargs):
    case = kwargs.get("case") or DEFAULT_MORPH["case"]
    num_class = kwargs.get("num_class") or DEFAULT_MORPH["num_class"]
    number = kwargs.get("number") or DEFAULT_MORPH["number"]
    gender = kwargs.get("gender") or DEFAULT_MORPH["gender"]

    numbers = list()

    if num_class == "collective" and len(number_items) > 1:
        num_class = "quantitative"

    for i in range(len(number_items)):

        number_item = number_items[i]

        if i == len(number_items) - 1:

            __number = number
            __case = case
            if number_item.scale:
                __prev_value = number_items[i - 1].value if i > 0 else 1
                __number = "singular" if __prev_value == 1 else "plural"
                __case = (
                    "nominative"
                    if __prev_value == 1
                    else "nominative"
                    if __prev_value in (2, 3, 4)
                    else "genetive"
                )

            numbers.append(
                int2numeral_word(
                    number_item.value,
                    lang=lang,
                    case=__case,
                    num_class=num_class,
                    gender=gender,
                    number=__number,
                )
            )

            continue

        __case = case
        if num_class == "ordinal":
            __case = "nominative"

        if (
            (0 < number_item.value < 10)
            and (i + 1 < len(number_items))
            and number_items[i + 1].scale
        ):
            ___case = "nominative" if __case in ("nominative", "accusative") else __case
            __gender = "feminine" if number_items[i + 1].value == 1000 else "masculine"

            numbers.append(
                int2numeral_word(
                    number_item.value, lang=lang, case=___case, gender=__gender
                )
            )
            continue

        if number_item.scale:
            __prev_value = number_items[i - 1].value if i > 0 else 1
            __number = "singular" if __prev_value == 1 else "plural"

            ___case = __case
            if __case in ("nominative", "accusative"):
                ___case = "nominative" if __prev_value in (1, 2, 3, 4) else "genetive"

            numbers.append(
                int2numeral_word(
                    number_item.value, lang=lang, case=___case, number=__number
                )
            )
            continue

        ___case = (
            "nominative"
            if __case == "accusative" and i != len(number_items) - 2
            else __case
        )
        numbers.append(
            int2numeral_word(number_item.value, lang=lang, case=___case),
        )

    return __process_numbers(numbers, number_items, lang=lang)


def __check_kwargs(kwargs):
    for label, label_item in kwargs.items():
        if MORPH_FORMS.get(label) is None:
            raise ValueError(f"Invalid label; use one of {MORPH_FORMS.keys()}")
        if label_item and label_item not in MORPH_FORMS[label]:
            raise ValueError(
                f"Invalid label {label} value; use one of {MORPH_FORMS[label]}"
            )


def __process_numbers(
    numbers: List[NumeralWord], number_items, lang: str
) -> Dict[str, Any]:

    if lang == "en":
        numbers__ = numbers.copy()
        numbers = list()
        i = 0
        while i < len(number_items):
            if (
                i + 1 < len(number_items)
                and number_items[i].order == 1
                and number_items[i + 1].order == 0
            ):
                numbers.append(
                    NumeralWord(
                        numbers__[i].default + "-" + numbers__[i + 1].default, []
                    )
                )
                i += 2
            else:
                numbers.append(numbers__[i])
                i += 1

    numeral = " ".join(
        [
            f"{number.default}" + (f" ({', '.join(number.alt)})" if number.alt else "")
            for number in numbers
        ]
    )

    numeral_forms = [
        " ".join(
            [
                (
                    [
                        numbers[i].default,
                    ]
                    + numbers[i].alt
                )[j]
                for i, j in enumerate(__combinations)
            ]
        )
        for __combinations in combinations(
            *[range(1 + len(number.alt)) for number in numbers]
        )
    ]

    return {"numeral": numeral, "numeral_forms": numeral_forms}


def __preprocess_numeral(numeral: str, lang: str) -> str:

    if lang == "en":
        numeral = re.sub(r"-", " ", numeral)
        numeral = re.sub(r"\sand\s", " ", numeral)

    numeral = re.sub(r"\s+", " ", numeral).strip()

    numeral = numeral.lower()

    return numeral


def __delete_ordinal_from_numeral_word_info(
    number_word_info: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    return [
        item
        for item in number_word_info
        if (
            not isinstance(item["value"]["morph_forms"], list)
            and item["value"]["morph_forms"].get("num_class") != "ordinal"
        )
        or all(
            [
                (v.get("num_class") is None or v.get("num_class") != "ordinal")
                for v in item["value"]["morph_forms"]
            ]
        )
    ]
