import warnings
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from fuzzy_multi_dict import FuzzyMultiDict

from .constants import DEFAULT_MORPH

DATA_PATH = Path("/Users/tatiana/PycharmProjects/numeral-converter/data")

NUMERAL_TREE: Dict[str, Any] = dict()
NUMERAL_DATA: Dict[str, pd.DataFrame] = dict()


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


def load_numeral_data(lang: str):
    """
    Loads language `lang` data

    :param str lang: language identifier

    :Example:

    >>> from numeral_converter import load_numeral_data
    >>> load_numeral_data('uk')

    """
    if __is_loaded(lang):
        warnings.warn(f"data for language {lang} already load", UserWarning)
        return

    if not __is_available(lang):
        raise ValueError(
            f"no data for language {lang}; "
            f"use one of the available languages: {get_available_languages()}"
        )

    filename = DATA_PATH / f"{lang}.csv"

    NUMERAL_DATA[lang] = __read_language_data(filename)
    NUMERAL_TREE[lang] = __build_numeral_tree(NUMERAL_DATA[lang])


def check_numeral_data_load(lang):
    if not __is_loaded(lang):
        warnings.warn(
            f'data for language "{lang}" is not loaded;'
            f'starts searching for data for language "{lang}"',
            UserWarning,
        )
        load_numeral_data(lang)


def __read_language_data(filename: Path) -> pd.DataFrame:
    df = pd.read_csv(filename, sep=",")
    df["order"] = df.order.apply(lambda x: int(x) if not pd.isnull(x) else -1)
    df["value"] = df.apply(
        lambda row: int(row.value) if not pd.isnull(row.value) else 10**row.order,
        axis=1,
    )
    for c in df.columns:
        df[c] = df[c].apply(lambda x: None if pd.isnull(x) else x)

    return df


def __build_numeral_tree(df: pd.DataFrame) -> FuzzyMultiDict:
    numeral_tree = FuzzyMultiDict(update_value_func=__update_numeral_word_value)

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

            numeral_tree[string] = data

    return numeral_tree


def __is_loaded(lang: str):
    return not (NUMERAL_TREE.get(lang) is None or NUMERAL_DATA.get(lang) is None)


def __is_available(lang: str) -> bool:
    __available_languages = get_available_languages()
    return lang in __available_languages


def __update_numeral_word_value(x, y):
    if x is None:
        return y

    if not isinstance(x, dict) or not isinstance(y, dict):
        raise TypeError(f"Invalid value type; expect dict; got {type(x)} and {type(y)}")

    for k, v in y.items():
        if x.get(k) is None:
            x[k] = v
        elif isinstance(x[k], list):
            x[k].append(v)
        elif x[k] != v:
            x[k] = [x[k], v]

    return x
