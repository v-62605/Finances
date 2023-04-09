import concurrent.futures
import datetime
import random
import time

import names


class Account:
    def __init__(self, id: int, first_name: str, last_name: str, rate: float):
        random.seed(time.time())
        self.id = random.randrange(1_000_000_000, 99999999999999999) if id <= 1_000_000_000 else id
        self.first_name = first_name
        self.last_name = last_name
        self.rate = rate if rate is not None else None
        self.unpaid_hours: float = 0
        self.unpaid_income: float = 0
        self.paid_hours: float = 0
        self.paid_income: float = 0
        self.average_pay_rate: float = 0
        self.pay_raise: list = [(self.rate, datetime.datetime.now().astimezone())]

    def __repr__(self) -> str:
        return f"Account({self.id}, {self.first_name}, {self.last_name}, {self.rate})"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Account):
            return NotImplemented

        return self.id == other.id

    def get_info(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "rate": self.rate,
            "unpaid_hours": self.unpaid_hours,
            "unpaid_income": self.unpaid_income,
            "paid_hours": self.paid_hours,
            "paid_income": self.paid_income,
            "pay_raise": self.pay_raise,
        }

    def update_rate(self, rate: float) -> dict:
        self.rate = rate

        self.pay_raise.append((self.rate, datetime.datetime.now().astimezone()))

        return {"rate": self.rate}

    def average_rate(self) -> dict:
        if self.rate is None:
            raise ValueError("Rate is not set")

        if self.paid_hours == 0:
            raise ValueError("No paid hours")

        self.average_pay_rate = self.paid_income / self.paid_hours

        return {"average_rate": self.average_pay_rate}

    def add_hours(self, hours: float) -> dict:
        if self.rate is None:
            raise ValueError("Rate is not set")

        self.unpaid_hours += hours
        self.unpaid_income = self.unpaid_hours * self.rate
        return {"unpaid_hours": self.unpaid_hours, "paid_hours": self.paid_hours}

    def get_income(self) -> dict:
        if self.rate is None:
            raise ValueError("Rate is not set")

        self.unpaid_income = self.unpaid_hours * self.rate
        return {"unpaid_income": self.unpaid_income, "paid_income": self.paid_income}

    def pay(self, hours: float = 0) -> dict:
        hours = hours if hours > 0 else self.unpaid_hours
        self.paid_hours += hours
        self.unpaid_hours = self.unpaid_hours - hours

        if self.rate is None:
            raise ValueError("Rate is not set")

        self.paid_income += hours * self.rate
        self.unpaid_income = self.unpaid_hours * self.rate

        return {
            "unpaid_hours": self.unpaid_hours,
            "paid_hours": self.paid_hours,
            "unpaid_income": self.unpaid_income,
            "paid_income": self.paid_income,
        }

    def save(self) -> None:
        pass


def generate_accounts(n: int) -> list:
    accounts = []
    for i in range(n):
        accounts.append(
            Account(
                i,
                names.get_first_name(),
                names.get_last_name(),
                round(random.normalvariate(30, 5), 2),
            )
        )

    return accounts


def generate_daily_events_for_an_account(account: Account) -> Account:
    """Generate daily events for an account"""

    # Add hours for the day
    account.add_hours(round(random.uniform(8, 10), 2))

    # Get a raise with probability 0.0035, (1-p)^261 = 0.4 -> p = 0.0035
    if random.random() < 0.0035:
        account.update_rate(round(account.rate * (1 + random.uniform(0, 0.05)), 2))

    # Pay when the account has more than 40 hours
    if account.unpaid_hours >= 40:
        account.pay()

    return account


def generate_n_days_events_for_an_account(account: Account, n: int) -> Account:
    """Generate n days events for an account"""

    for i in range(n):
        account = generate_daily_events_for_an_account(account)

    return account


def generate_n_days_events_for_accounts(accounts: list, n: int) -> list:
    """Generate n days events for accounts"""

    with concurrent.futures.ProcessPoolExecutor() as executor:
        accounts_events = executor.map(
            generate_n_days_events_for_an_account, accounts, [n] * len(accounts)
        )

    return list(accounts_events)
