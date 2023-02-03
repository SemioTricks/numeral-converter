from numeral_converter import convert_numerical_in_text


def test_convert_numerical_in_text():
    s = (
        "У цій школі працює шість психологів, і кожен із нас має навантаження "
        "понад сто учнів"
    )
    expect = (
        "У цій школі працює 6 психологів, і кожен із нас має навантаження "
        "понад 100 учнів"
    )
    assert convert_numerical_in_text(s, lang="uk") == expect

    s = "У моєму портфелі лежало чотири книги."
    expect = "У моєму портфелі лежало 4 книги."
    assert convert_numerical_in_text(s, lang="uk") == expect

    s = (
        "Їй дуже хочеться модний жакет, який коштує сто п’ятнадцять доларів, "
        "і Клайду важко встояти перед її бажанням."
    )
    expect = (
        "Їй дуже хочеться модний жакет, який коштує 115 доларів, "
        "і Клайду важко встояти перед її бажанням."
    )
    assert convert_numerical_in_text(s, lang="uk") == expect

    s = "У моєму класі двадцять п’ять учнів."
    expect = "У моєму класі 25 учнів."
    assert convert_numerical_in_text(s, lang="uk") == expect

    s = "Вчора на зустрічі випускників учні нашої гімназії посадили чотири дерева."
    expect = "Вчора на зустрічі випускників учні нашої гімназії посадили 4 дерева."
    assert convert_numerical_in_text(s, lang="uk") == expect

    s = (
        "Сорок учнів отримали сертифікат про закінчення курсів першої "
        "невідкладної допомоги."
    )
    expect = (
        "40 учнів отримали сертифікат про закінчення курсів 1 невідкладної допомоги."
    )
    assert convert_numerical_in_text(s, lang="uk") == expect

    s = (
        "На покритих піною морських водоростях лежало одинадцять "
        "білих лебединих пір’їн."
    )
    expect = "На покритих піною морських водоростях лежало 11 білих лебединих пір’їн."
    assert convert_numerical_in_text(s, lang="uk") == expect

    s = "За добу було зібрано тридцять чотири тонни зерна."
    expect = "За добу було зібрано 34 тонни зерна."
    assert convert_numerical_in_text(s, lang="uk") == expect
