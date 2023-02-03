from .numeral_converter import (
    NUMERAL_TREE,
    NumberItem,
    check_numeral_data_load,
    number_items2int,
)


def convert_numerical_in_text(
    text: str, lang: str, max_mistakes_number_part=0.2
) -> str:
    """
    Converts numerical string in text into integer values

    :param text: input text
    :param lang: input text language
    :param max_mistakes_number_part: max mistakes number part:
           mistakes number / string lenght
    :return: update text

    :Example:

    >>> s = "У цій школі працює шість психологів, "
    ...     "і кожен із нас має навантаження понад сто учнів"
    >>> convert_numerical_in_text(s, lang='uk')
    "У цій школі працює 6 психологів, і кожен із нас має навантаження понад 100 учнів"

    >>> s = "У моєму портфелі лежало чотири книги."
    >>> convert_numerical_in_text(s, lang='uk')
    "У моєму портфелі лежало 4 книги."

    """
    check_numeral_data_load(lang)

    updated_text_tokens = list()

    __number_items = list()
    for token in text.split(" "):
        numerical = NUMERAL_TREE[lang].get(
            token, max_mistakes_number_part=max_mistakes_number_part
        )
        if numerical:
            __number_items.append(
                NumberItem(
                    numerical[0]["value"]["value"],
                    numerical[0]["value"]["order"],
                    numerical[0]["value"]["scale"],
                )
            )
        else:
            if __number_items:
                updated_text_tokens.append(str(number_items2int(__number_items)))
                __number_items = list()
            updated_text_tokens.append(token)

    return " ".join(updated_text_tokens)
