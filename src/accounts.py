from typing import Union


class Account:
    def __init__(self, id: int, first_name: str, last_name: str, rate: Union[float, None] = None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.rate = rate
        self.unpaid_hours: float = 0
        self.unpaid_income: float = 0
        self.paid_hours: float = 0
        self.paid_income: float = 0
        self.average_pay_rate: float = 0

    def __repr__(self) -> str:
        return f"Account({self.id}, {self.first_name}, {self.last_name})"

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
        }

    def update_rate(self, rate: float) -> dict:
        self.rate = rate

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
        return {"unpaid_hours": self.unpaid_hours, "paid_hours": self.paid_hours}

    def get_income(self) -> dict:
        if self.rate is None:
            raise ValueError("Rate is not set")

        self.unpaid_income = self.unpaid_hours * self.rate
        return {"unpaid_income": self.unpaid_income, "paid_income": self.paid_income}

    def pay(self) -> dict:
        self.paid_hours += self.unpaid_hours
        self.paid_income += self.get_income()["unpaid_income"]
        self.unpaid_hours = 0
        self.unpaid_income = 0
        return {
            "unpaid_hours": self.unpaid_hours,
            "paid_hours": self.paid_hours,
            "unpaid_income": self.unpaid_income,
            "paid_income": self.paid_income,
        }
