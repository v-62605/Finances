import concurrent.futures

import numpy as np
import pandas as pd


def calculate_tax(income: float) -> float:
    if income <= 18200:
        return 0
    elif income <= 45000:
        return (income - 18200) * 0.19
    elif income <= 120000:
        return (income - 45000) * 0.325 + 5092
    elif income <= 180000:
        return (income - 120000) * 0.37 + 29467
    else:
        return (income - 180000) * 0.45 + 51667


def get_number_of_weekdays(start_date: str, end_date: str) -> int:
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    weekdays = pd.date_range(start_date, end_date, freq="B")
    return len(weekdays)


def get_number_of_weekdays_minus_leave(
    start_date: str, end_date: str, leave_days: int
) -> int:
    return get_number_of_weekdays(start_date, end_date) - leave_days


def get_number_of_hours_in_year_minus_leave(year: int, leave_days: int = 0) -> int:
    return (
        get_number_of_weekdays_minus_leave(f"{year}-01-01", f"{year}-12-31", leave_days)
        * 8
    )


def get_number_of_weekdays_in_year_minus_leave(year: int, leave_days: int = 0) -> int:
    return get_number_of_weekdays(f"{year}-01-01", f"{year}-12-31") - leave_days


def get_number_of_weeks_in_year_minus_leave(year: int, leave_days: int = 0) -> int:
    return round(get_number_of_weekdays_in_year_minus_leave(year, leave_days) / 5, 0)


def get_number_of_biweeks_in_year_minus_leave(year: int, leave_days: int = 0) -> int:
    return round(get_number_of_weekdays_in_year_minus_leave(year, leave_days) / 10, 0)


def get_number_of_months_in_year_minus_leave(year: int, leave_days: int = 0) -> int:
    return round(get_number_of_weekdays_in_year_minus_leave(year, leave_days) / 22, 0)


# Convert daily income to yearly income
def get_yearly_income_using_daily_income(
    daily_income: float, leave_days: int, this_year: pd.Timestamp
) -> float:
    return daily_income * get_number_of_weekdays_in_year_minus_leave(
        this_year, leave_days
    )


# Divide floats in dictionary by x if they are floats except for yearly income, rate and hours
def divide_dict_by_x(dictionary: dict, x: float) -> dict:
    dictionary = {k: float(v) for k, v in dictionary.items()}
    return {
        k: v / x if isinstance(v, float) and k != "rate" and k != "hours" else v
        for k, v in dictionary.items()
    }


# Change keys in dictionary from yearly to monthly
def change_dict_keys_to_new_string(dictionary: dict, string: str) -> dict:
    return {k.replace("yearly", string): v for k, v in dictionary.items()}


def create_yearly_income_dict(
    daily_rate: float,
    daily_hours: float,
    leave_days: int,
    this_year: pd.Timestamp = pd.to_datetime("today").year,
) -> dict:
    income_dict = {}
    yearly_income = get_yearly_income_using_daily_income(
        daily_hours * daily_rate, leave_days, this_year
    )

    income_dict["yearly_income"] = yearly_income
    income_dict["yearly_tax"] = calculate_tax(yearly_income)
    income_dict["yearly_take_home"] = yearly_income - income_dict["yearly_tax"]
    income_dict["yearly_super"] = yearly_income * 0.105
    income_dict["yearly_take_home_plus_super"] = (
        income_dict["yearly_take_home"] + income_dict["yearly_super"]
    )
    income_dict["yearly_income_plus_super"] = (
        income_dict["yearly_income"] + income_dict["yearly_super"]
    )
    income_dict["rate"] = daily_rate
    income_dict["hours"] = daily_hours

    return income_dict


def x_to_name(x: str) -> str:
    if x == "hours":
        return "hourly"
    elif x == "weekdays":
        return "daily"
    elif x == "weeks":
        return "weekly"
    elif x == "months":
        return "monthly"
    elif x == "biweeks":
        return "biweekly"
    elif x == "year":
        return "yearly"
    return x


def create_x_income_dict(
    daily_rate: float,
    daily_hours: float,
    leave_days: int,
    x: str,
    this_year: pd.Timestamp = pd.to_datetime("today").year,
) -> dict:
    income_dict = create_yearly_income_dict(
        daily_rate, daily_hours, leave_days, this_year
    )

    if x == "year":
        return income_dict
    return change_dict_keys_to_new_string(
        divide_dict_by_x(
            income_dict,
            eval(f"get_number_of_{x}_in_year_minus_leave(this_year, leave_days)"),
        ),
        x_to_name(x),
    )


def create_all_x_income_dicts(
    daily_rate: float,
    daily_hours: float,
    leave_days: int,
    this_year: pd.Timestamp = pd.to_datetime("today").year,
) -> dict:
    return {
        x: create_x_income_dict(daily_rate, daily_hours, leave_days, x, this_year)
        for x in ["year", "months", "biweeks", "weeks", "weekdays", "hours"]
    }


def create_all_x_income_dicts_for_multiple_rates(
    daily_rates: list,
    daily_hours: float,
    leave_days: int,
    this_year: pd.Timestamp = pd.to_datetime("today").year,
) -> dict:
    return {
        f"{daily_rate}": create_all_x_income_dicts(
            daily_rate, daily_hours, leave_days, this_year
        )
        for daily_rate in daily_rates
    }


def dicts_have_matching_keys(d1: dict, d2: dict) -> bool:
    return d1.keys() == d2.keys()


def operate_dicts(d1: dict, d2: dict, operator: str) -> dict:
    if dicts_have_matching_keys(d1, d2) and operator in ["+", "-", "*", "/"]:
        return {k: eval(f"{d1[k]} {operator} {d2[k]}") for k in d1.keys()}
    else:
        return {k: d1[k] for k in d1.keys()}


def process_rate(rate, daily_hours, leave_days, this_year, period, base_rate_dict):
    rate_dict = create_all_x_income_dicts(rate, daily_hours, leave_days, this_year)[
        period
    ]
    return (rate, operate_dicts(rate_dict, base_rate_dict, "-"))


# Compare list of rates to a base rate
def compare_rates_to_base_rate(
    base_rate: float,
    period: str,
    rates: np.arange,
    daily_hours: float,
    leave_days: int,
    this_year: pd.Timestamp = pd.to_datetime("today").year,
) -> dict:
    base_rate_dict = create_all_x_income_dicts(
        base_rate, daily_hours, leave_days, this_year
    )[period]
    rates = sorted(np.insert(rates, 0, base_rate))
    compare_dict = {}

    with concurrent.futures.ProcessPoolExecutor(max_workers=None) as executor:
        futures = [
            executor.submit(
                process_rate,
                rate,
                daily_hours,
                leave_days,
                this_year,
                period,
                base_rate_dict,
            )
            for rate in rates
        ]
        compare_dict = {f.result()[0]: f.result()[1] for f in futures}

    return compare_dict


def get_excel_sheet_of_compare_rates_to_base_rate(
    base_rate: float,
    periods: list,
    rates: np.arange,
    daily_hours: float,
    leave_days: int,
    this_year: pd.Timestamp = pd.to_datetime("today").year,
) -> None:
    with pd.ExcelWriter("compare_rates.xlsx") as writer:
        for period in periods:
            pd.DataFrame.from_dict(
                compare_rates_to_base_rate(
                    base_rate, period, rates, daily_hours, leave_days, this_year
                ),
                orient="index",
            ).round(2).to_excel(writer, sheet_name=period)
