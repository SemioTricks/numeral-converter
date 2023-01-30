import logging
import math
import warnings
from collections import OrderedDict, namedtuple
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from fuzzy_multi_dict import FuzzyMultiDict

NumberItem = namedtuple("NumberItem", "value order scale")

DATA_PATH = Path("/Users/tatiana/PycharmProjects/numeral-converter/data")
NUMERAL_TREE: Dict[str, Any] = dict()
NUMERAL_DATA: pd.DataFrame = dict()
DEFAULT_MORPH: Dict[str, Any] = OrderedDict(
    [
        ("case", "nominative"),
        ("num_class", "quantitative"),
        ("number", None),
        ("gender", "masculine"),
    ]
)

logger = logging.getLogger(__name__)


def numeral2int(numeral: str, lang: str = "uk") -> Optional[int]:
    """
    Converts input numeral in language `lang` into integer value

    :param numeral: input numeral in language `lang`
    :param lang: language; default 'uk'
    :return Optional [int]: integer value or None if nothing found
    """
    number_items = numeral2number_items(numeral=numeral, lang=lang)

    value = number_items2int(number_items=number_items)

    return value


def int2numeral(value: int, lang: str = "uk", **kwargs):
    """
    Converts input integer number into a numeral in language `lang`
    into a morphological form given by the argument-parameters:
        "case": 'accusative', 'dative', 'genetive', 'instrumental', 'nominative' or
                'prepositional';
        "num_class": 'collective', 'ordinal' or 'quantitative';
        "gender": 'feminine', 'masculine' or 'neuter';
        "number": 'plural' or 'singular'.

    :param value: input integer value
    :param lang: language identifier; default is 'uk'
    :return str: string numeral in language `lang` in a morphological form
            given by the argument-parameters

    """

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


def load(lang: str = "uk"):
    """
    Loads language `lang` data

    :param str lang: language identifier; default is 'uk'

    """
    global NUMERAL_TREE, NUMERAL_DATA, DEFAULT_MORPH, DATA_PATH

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
        __available_languages = [x.stem for x in DATA_PATH.glob("*.csv")]
        if lang not in __available_languages:
            raise ValueError(
                f"no data for language {lang}; "
                f"use one of the available languages: {__available_languages}"
            )
        filename = DATA_PATH / f"{lang}.csv"

        df = pd.read_csv(filename, sep=",")
        df["order"] = df.order.apply(lambda x: int(x) if not pd.isnull(x) else -1)
        df["value"] = df.apply(lambda row: int(row.value), axis=1)
        for c in df.columns:
            df[c] = df[c].apply(lambda x: None if pd.isnull(x) else x)

        NUMERAL_DATA[lang] = df
        NUMERAL_TREE[lang] = FuzzyMultiDict(update_value_func=__update_value)

        for i, row in df.iterrows():

            for string in row["string"].split(" "):
                if not string:
                    continue

                data = {
                    "morph_forms": [
                        {label: row[label] for label in DEFAULT_MORPH.keys()},
                    ],
                    "value": row["value"],
                    "order": row["order"],
                    "scale": row["scale"],
                }

                NUMERAL_TREE[lang][string] = data


def numeral2number_items(numeral: str, lang: str):
    global NUMERAL_TREE

    if NUMERAL_TREE.get(lang) is None:
        logger.info(
            f'data for language "{lang}" is not loaded;'
            f'starts searching for data for language "{lang}"'
        )
        load(lang)

    number_items: List[NumberItem] = list()

    for number_word in numeral.split(" ")[::-1]:

        if not number_word:
            continue

        number_word_info = NUMERAL_TREE[lang].get(number_word)

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


def int2numeral_word(value: int, lang: str = "uk", **kwargs) -> Dict[str, Any]:
    global NUMERAL_DATA, DEFAULT_MORPH

    if NUMERAL_DATA.get(lang) is None:
        logger.info(
            f'data for language "{lang}" is not loaded;'
            f'starts searching for data for language "{lang}"'
        )
        load(lang)

    sub_data = NUMERAL_DATA[lang][NUMERAL_DATA[lang].value == value]

    for label, default in DEFAULT_MORPH.items():
        value = kwargs.get(label) or default

        if label not in NUMERAL_DATA[lang].columns:
            raise ValueError(f'no column "{label}" in data for language "{lang}"')

        if value:
            if value in sub_data[label].values:
                sub_data = sub_data[sub_data[label] == value]
            elif kwargs.get(label):
                warnings.warn(
                    f"no data for {label} == {kwargs.get(label)}; ignored", UserWarning
                )

    if sub_data.shape[0] != 1:
        val_info = f"number {value}" + ", ".join(
            [
                f', {label} = "{kwargs.get(label) or default}"'
                for label, default in DEFAULT_MORPH.items()
                if (kwargs.get(label) or default)
            ]
        )

        if sub_data.shape[0] == 0:
            raise ValueError(f"No data for {val_info}")

        if sub_data.shape[0] > 1:
            values = ", ".join([f"{x}" for x in sub_data.value.values])
            raise ValueError(f"There are more then one values {val_info}: {values}")

    numeral_words = [x.strip() for x in sub_data.iloc[0].string.split(" ") if x]

    return {
        "numeral_word": numeral_words[0],
        "alts": numeral_words[1:],
    }


def __process_numbers(numbers: List[Dict[str, Any]]) -> str:
    s = " ".join(
        [
            f"{number['numeral_word']}"
            + (f" ({', '.join(number['alts'])})" if number["alts"] else "")
            for number in numbers
        ]
    )
    return s


def number_items2numeral(number_items: List[NumberItem], lang: str = "uk", **kwargs):
    global NUMERAL_DATA, DEFAULT_MORPH

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
            if number_item.scale:
                __prev_value = number_items[i - 1].value if i > 0 else 1
                __number = "singular" if __prev_value == 1 else "plural"

            numbers.append(
                int2numeral_word(
                    number_item.value,
                    lang=lang,
                    case=case,
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
                int2numeral_word(number_item.value, case=___case, gender=__gender)
            )
            continue

        if number_item.scale:
            __prev_value = number_items[i - 1].value if i > 0 else 1
            __number = "singular" if __prev_value == 1 else "plural"

            ___case = __case
            if __case in ("nominative", "accusative"):
                ___case = "nominative" if __prev_value in (1, 2, 3, 4) else "genetive"

            numbers.append(
                int2numeral_word(number_item.value, case=___case, number=__number)
            )
            continue

        ___case = (
            "nominative"
            if __case == "accusative" and i != len(number_items) - 2
            else __case
        )
        numbers.append(int2numeral_word(number_item.value, case=___case))

    return __process_numbers(numbers)
