import pytest

import src.utils as utils


# From src/finance/utils.py create test for calculate_tax
@pytest.mark.parametrize(
    "income, expected",
    [
        (0, 0),
        (10000, 0),
        (20000, 342.0),
        (30000, 2242.0),
        (40000, 4142.0),
        (50000, 6717.0),
        (60000, 9967.0),
        (70000, 13217.0),
        (80000, 16467.0),
        (90000, 19717.0),
        (100000, 22967.0),
        (110000, 26217.0),
        (120000, 29467.0),
        (130000, 33167.0),
    ],
)
def test_calculate_tax(income: float, expected: float) -> None:
    assert utils.calculate_tax(income) == expected
