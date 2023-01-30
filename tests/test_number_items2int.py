import re

import pytest

from numeral_converter.numeral_converter import NumberItem, number_items2int


def test_wrong_by_next_group_order_values():

    msg = (
        r"position 1: order of 1000000000:9 is less/equal "
        r"of summary order in next group: 9"
    )
    with pytest.raises(ValueError, match=msg):

        number_items2int(
            [
                NumberItem(value=3, order=0, scale=None),
                NumberItem(value=1000000000, order=9, scale=True),
                NumberItem(value=1000, order=3, scale=True),
                NumberItem(value=50, order=1, scale=None),
                NumberItem(value=5, order=0, scale=None),
                NumberItem(value=1000000, order=6, scale=True),
            ]
        )

    msg = (
        "position 1: order of 1000000000:9 is less/equal "
        "of summary order in next group: 9"
    )
    with pytest.raises(ValueError, match=msg):
        number_items2int(
            [
                NumberItem(value=3, order=0, scale=None),
                NumberItem(value=1000000000, order=9, scale=True),
                NumberItem(value=1000, order=3, scale=True),
                NumberItem(value=1000000, order=6, scale=True),
            ]
        )

    # "тисяча тисяч"
    msg = "position 0: order of 1000:3 is less/equal of summary order in next group: 3"
    with pytest.raises(ValueError, match=msg):
        number_items2int(
            number_items=[NumberItem(1000, 3, True), NumberItem(1000, 3, True)]
        )

    # тисяча двадцять сотень
    msg = "position 0: order of 1000:3 is less/equal of summary order in next group: 3"
    with pytest.raises(ValueError, match=msg):
        number_items2int(
            number_items=[
                NumberItem(value=1000, order=3, scale=True),
                NumberItem(value=20, order=1, scale=None),
                NumberItem(value=100, order=2, scale=True),
            ]
        )


def test_wrong_by_next_value_order_values():
    msg = "position 1: 2 with order 0 stands after 12 with less/equal order 0"
    with pytest.raises(ValueError, match=msg):
        number_items2int(
            number_items=[
                NumberItem(value=12, order=1, scale=None),
                NumberItem(value=2, order=0, scale=None),
            ]
        )


def test_wrong_by_scale_values():
    # "триста сто три"
    msg = re.escape("position 1: expects 10^(3n) or 100; found 100")
    with pytest.raises(ValueError, match=msg):
        number_items2int(
            number_items=[
                NumberItem(value=300, order=2, scale=None),
                NumberItem(value=100, order=2, scale=False),
                NumberItem(value=3, order=0, scale=None),
            ]
        )


def test_correct_nonsimple():
    # "тисяча мільонів"
    assert (
        number_items2int(
            number_items=[
                NumberItem(1000, 3, True),
                NumberItem(1000000, 6, True),
            ]
        )
        == 1000000000
    )

    # "триста сотень три"
    number_items2int(
        number_items=[
            NumberItem(value=300, order=2, scale=None),
            NumberItem(value=100, order=2, scale=True),
            NumberItem(value=3, order=0, scale=None),
        ]
    )


def test_correct():
    # "тисяча сто"
    assert (
        number_items2int(
            number_items=[
                NumberItem(value=1000, order=3, scale=True),
                NumberItem(value=100, order=2, scale=None),
            ]
        )
        == 1100
    )

    assert (
        number_items2int(
            number_items=[
                NumberItem(value=100, order=2, scale=None),
                NumberItem(value=11, order=1, scale=None),
                NumberItem(value=1000, order=3, scale=True),
                NumberItem(value=100, order=2, scale=None),
                NumberItem(value=11, order=1, scale=None),
            ]
        )
        == 111111
    )

    assert (
        number_items2int(
            number_items=[
                NumberItem(value=100, order=2, scale=None),
                NumberItem(value=40, order=1, scale=None),
                NumberItem(value=2, order=0, scale=None),
                NumberItem(value=1000, order=3, scale=True),
                NumberItem(value=30, order=1, scale=None),
                NumberItem(value=1, order=0, scale=None),
            ]
        )
        == 142031
    )

    assert (
        number_items2int(
            number_items=[
                NumberItem(200, 2, None),
                NumberItem(20, 1, None),
                NumberItem(2, 0, None),
            ]
        )
        == 222
    )
