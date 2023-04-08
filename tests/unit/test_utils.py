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


@pytest.mark.parametrize(
    "start_date, end_date, expected",
    [
        ("2020-01-01", "2020-01-31", 23),
        ("2020-01-01", "2020-02-29", 43),
        ("2020-01-01", "2020-03-31", 65),
        ("2045-01-01", "2045-04-30", 85),
        ("2045-01-01", "2045-05-31", 108),
        ("2045-01-01", "2100-06-30", 14478),
    ],
)
def test_get_number_of_weekdays(start_date: str, end_date: str, expected: int) -> None:
    assert utils.get_number_of_weekdays(start_date, end_date) == expected


@pytest.mark.parametrize(
    "leave_days,expected",
    [
        (0, 262),
        (10, 252),
        (7, 255),
        (57, 205),
    ],
)
def test_get_number_of_weekdays_minus_leave(leave_days: int, expected: int) -> None:
    assert (
        utils.get_number_of_weekdays_minus_leave(
            start_date="2020-01-01", end_date="2020-12-31", leave_days=leave_days
        )
        == expected
    )
