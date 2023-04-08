import pytest

from src.accounts import Account


@pytest.mark.parametrize(
    "first_name, last_name, id, rate, expected",
    [
        ("John", "Doe", 1, 10.0, {"id": 1, "first_name": "John", "last_name": "Doe", "rate": 10.0}),
        (
            "X",
            "Y_@()!1",
            165468787,
            68.56,
            {"id": 165468787, "first_name": "X", "last_name": "Y_@()!1", "rate": 68.56},
        ),
    ],
)
def test_account_init(
    first_name: str, last_name: str, id: int, rate: float, expected: dict
) -> None:
    account = Account(id, first_name, last_name, rate)
    assert account.get_info() == expected
