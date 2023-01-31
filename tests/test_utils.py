from numeral_converter.utils import combinations


def test_one_item_array():
    assert list(
        combinations(
            [1, 2],
        )
    ) == [[1], [2]]


def test_one_item_arrays():
    assert list(
        combinations(
            [
                1,
            ],
            [
                1,
            ],
        )
    ) == [[1, 1]]


def test_combinations():
    assert list(
        combinations(
            [
                1,
            ],
            [
                1,
                2,
            ],
            [1, 2, 3],
        )
    ) == [[1, 1, 1], [1, 1, 2], [1, 1, 3], [1, 2, 1], [1, 2, 2], [1, 2, 3]]


def test_combinations_ranges():
    assert list(
        combinations(
            range(1),
            range(2),
            range(3),
        )
    ) == [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 1, 0], [0, 1, 1], [0, 1, 2]]


def test_combinations_empty_ranges():
    assert list(combinations(range(1), range(1), range(1),)) == [
        [0, 0, 0],
    ]


def test_combinations_ranges_list():
    r = [
        range(1),
        range(1),
        range(1),
    ]
    assert list(combinations(*r)) == [
        [0, 0, 0],
    ]
