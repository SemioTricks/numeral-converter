import logging
import math
import re
import warnings
from collections import namedtuple
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from fuzzy_multi_dict import FuzzyMultiDict

from .constants import DEFAULT_MORPH, MORPH_FORMS
from .utils import combinations

NumberItem = namedtuple("NumberItem", "value order scale")
NumeralWord = namedtuple("NumeralWord", "default alt")

DATA_PATH = Path("/Users/tatiana/PycharmProjects/numeral-converter/data")

NUMERAL_TREE: Dict[str, Any] = dict()
NUMERAL_DATA: Dict[str, pd.DataFrame] = dict()


logger = logging.getLogger(__name__)


def numeral2int(numeral: str, lang: str) -> Optional[int]:
    """
    Converts input numeral in language `lang` into integer value

    :param numeral: input numeral in language `lang`
    :param lang: language
    :return Optional [int]: integer value or None if nothing found

    :Example:

    >>> from numeral_converter import load, numeral2int
    >>> load("uk")
    >>> numeral2int("дві тисячі двадцять третій", lang="uk")
    2023

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

    >>> from numeral_converter import load, int2numeral
    >>> load("uk")
    >>> int2numeral(2023, case="nominative", num_class="quantitative")
    {
        'numeral': 'дві тисячі двадцять три',
        'numeral_forms': ['дві тисячі двадцять три', ]
    }

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


def get_available_languages() -> List[str]:
    """
    Check available languages

    :return List[str]: list of available languages identifier

    :Example:

    >>> from numeral_converter import get_available_languages
    >>> get_available_languages()
    ['uk', 'ru', 'en']

    """
    return [x.stem for x in DATA_PATH.glob("*.csv")]


def load(lang: str):
    """
    Loads language `lang` data

    :param str lang: language identifier

    :Example:

    >>> from numeral_converter import load
    >>> load('uk')

    """

    def __update_value(x, y):
        if x is None:
            return y

        if not isinstance(x, dict) or not isinstance(y, dict):
            raise TypeError(
                f"Invalid value type; expect dict; got {type(x)} and {type(y)}"
            )

        for k, v in y.items():
            if x.get(k) is None:
                x[k] = v
            elif isinstance(x[k], list):
                x[k].append(v)
            elif x[k] != v:
                x[k] = [x[k], v]

        return x

    if NUMERAL_TREE.get(lang) is None and NUMERAL_DATA.get(lang) is None:
        __available_languages = get_available_languages()
        if lang not in __available_languages:
            raise ValueError(
                f"no data for language {lang}; "
                f"use one of the available languages: {__available_languages}"
            )
        filename = DATA_PATH / f"{lang}.csv"

        df = pd.read_csv(filename, sep=",")
        df["order"] = df.order.apply(lambda x: int(x) if not pd.isnull(x) else -1)
        df["value"] = df.apply(
            lambda row: int(row.value) if not pd.isnull(row.value) else 10**row.order,
            axis=1,
        )
        for c in df.columns:
            df[c] = df[c].apply(lambda x: None if pd.isnull(x) else x)

        NUMERAL_DATA[lang] = df
        NUMERAL_TREE[lang] = FuzzyMultiDict(update_value_func=__update_value)

        for i, row in df.iterrows():
            for string in row["string"].split(" "):
                if not string:
                    continue

                data = {
                    "morph_forms": {
                        label: row[label]
                        for label in DEFAULT_MORPH.keys()
                        if row.get(label)
                    },
                    "value": row["value"],
                    "order": row["order"],
                    "scale": row["scale"],
                }

                NUMERAL_TREE[lang][string] = data


def numeral2number_items(numeral: str, lang: str):
    if NUMERAL_TREE.get(lang) is None:
        logger.info(
            f'data for language "{lang}" is not loaded;'
            f'starts searching for data for language "{lang}"'
        )
        load(lang)

    number_items: List[NumberItem] = list()

    __process_first = False
    numeral = re.sub("-", " ", numeral)
    for number_word in numeral.split(" ")[::-1]:

        if not number_word:
            continue

        number_word_info = NUMERAL_TREE[lang].get(number_word)
        if __process_first:
            number_word_info__ = [
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
            if len(number_word_info) and not len(number_word_info__):
                raise ValueError(
                    "the number in the middle of the numeral cannot be ordinal"
                )
            else:
                number_word_info = number_word_info__
        else:
            __process_first = True

        if not len(number_word_info):
            raise ValueError(f'can\'t convert "{number_word}" to integer')

        number_word_data = number_word_info[0]["value"]

        number_items.insert(
            0,
            NumberItem(
                value=number_word_data["value"],
                order=number_word_data["order"],
                scale=number_word_data["scale"],
            ),
        )

    return number_items


def number_items2int(number_items: List[NumberItem]) -> int:

    number_items = number_items[::-1]

    __value = 0

    if number_items[0].scale is None:
        i = __scale_group_start = 0
        __scale_order = 0
    else:
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

            __value += (10**__scale_order) * number_items2int(
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
            __value += __n

            __scale_group_start = None

        if i >= len(number_items):
            return __value

        if not number_items[i].scale:
            raise ValueError(
                f"position {len(number_items) - 1 - i}: expects 10^(3n) or 100; "
                f"found {number_items[i].value}"
            )

        __value_order = int(math.log10(__value))
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
        __value += 10**__scale_order

    return __value


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

    if NUMERAL_DATA.get(lang) is None:
        logger.info(
            f'data for language "{lang}" is not loaded;'
            f'starts searching for data for language "{lang}"'
        )
        load(lang)

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
