import pytest

import src.utils as utils


# From src/finance/utils.py create test for calculate_tax
@pytest.mark.parametrize(
    "income, expected",
    [
        (0, 0),
        (10000, 0),
        (20000, 342.0),
    ],
)
def test_calculate_tax(income: float, expected: float) -> None:
    assert utils.calculate_tax(income) == expected
