from numeral_converter import convert_numerical_in_text


def test_convert_numerical_in_text():
    s = (
        "Прості числівники мають один корінь. Складні числівники мають два корені. "
        "Складені числівники містять в собі два і більше простих чи складних "
        "числівників. Кількісні числівники не мають граматичних ознак роду та числа "
        "і змінюються лише за відмінками"
    )

    expect = (
        "Прості числівники мають 1 корінь. Складні числівники мають 2 корені. "
        "Складені числівники містять в собі 2 і більше простих чи складних "
        "числівників. Кількісні числівники не мають граматичних ознак роду та числа "
        "і змінюються лише за відмінками"
    )
    assert convert_numerical_in_text(s, lang="uk") == expect

    s = (
        "Числительные делятся на четыре лексико-грамматических разряда: "
        "количественные (два, пятьдесят, двести, триста пятьдесят один) и "
        "собирательные (оба, двое, пятеро) — отвечают на вопрос сколько?, "
        "порядковые — отвечают на вопрос который? (первый, второй, сотый), "
        "дробные."
    )
    expect = (
        "Числительные делятся на 4 лексико-грамматических разряда: "
        "количественные (2, 50, 200, 351) и собирательные (2, 2, 5) — "
        "отвечают на вопрос сколько?, порядковые — отвечают на вопрос который? "
        "(1, 2, 100), дробные."
    )
    assert convert_numerical_in_text(s, lang="ru") == expect
    s = (
        "After twenty, numbers such as twenty-five, fifty, seventy-five, "
        "and one hundred follow. So long as one knows the core number, or the number "
        "situated in the tens or hundreds position that determines the general "
        "amount, understanding these more complicated numbers won't be difficult. "
        'For example thirty-three is simply "thirty" plus three; sixty-seven '
        'is "sixty" plus seven; and sixty-nine is simply "sixty" plus nine.'
    )
    expect = (
        "After 20, numbers such as 25, 50, 75, and 100 follow. So long as 1 "
        "knows the core number, or the number situated in the 10 or 100 "
        "position that determines the general amount, understanding these more "
        "complicated numbers won't be difficult. For example 33 is simply "
        '"30" plus 3; 67 is "60" plus 7; and 69 is simply "60" plus 9.'
    )

    assert convert_numerical_in_text(s, lang="en") == expect
