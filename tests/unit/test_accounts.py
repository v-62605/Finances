import pytest

from src.accounts import Account


@pytest.mark.parametrize(
    "first_name, last_name, id, rate, expected",
    [
        ("John", "Doe", 1, 10.0, {"id": 1, "first_name": "John", "last_name": "Doe", "rate": 10.0}),
        (
            "X",
            "Y",
            165468787,
            68.56,
            {"id": 165468787, "first_name": "X", "last_name": "Y", "rate": 68.56},
        ),
    ],
)
def test_account_init(
    first_name: str, last_name: str, id: int, rate: float, expected: dict
) -> None:
    account = Account(id, first_name, last_name, rate)
    assert account.get_info() == expected


@pytest.mark.parametrize(
    "first_name, last_name, rate, expected",
    [
        (
            "John",
            "Doe",
            10.0,
            {
                "first": {
                    "unpaid_hours": 20,
                    "paid_hours": 20,
                    "unpaid_income": 200,
                    "paid_income": 200,
                },
                "second": {
                    "unpaid_hours": 0,
                    "paid_hours": 50,
                    "unpaid_income": 0,
                    "paid_income": 800,
                },
            },
        ),
        (
            "X",
            "Y",
            60,
            {
                "first": {
                    "unpaid_hours": 20,
                    "paid_hours": 20,
                    "unpaid_income": 1200,
                    "paid_income": 1200,
                },
                "second": {
                    "unpaid_hours": 0,
                    "paid_hours": 50,
                    "unpaid_income": 0,
                    "paid_income": 3300,
                },
            },
        ),
    ],
)
def test_sequence_of_daily_accounting_events(
    first_name: str, last_name: str, rate: float, expected: dict
) -> None:
    account = Account(0, first_name, last_name, rate)
    account.add_hours(40)
    assert account.pay(20) == expected["first"]
    account.update_rate(rate + 10)
    account.add_hours(10)
    assert account.pay() == expected["second"]
