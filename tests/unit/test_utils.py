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
            start_date="2020-01-01",
            end_date="2020-12-31",
            leave_days=leave_days,
        )
        == expected
    )


@pytest.mark.parametrize(
    "daily_rate, daily_hours, leave_days, expected",
    [
        (
            100,
            8,
            0,
            {
                "yearly_income": 208800,
                "yearly_tax": 64627.0,
                "yearly_take_home": 144173.0,
                "yearly_super": 21924.0,
                "yearly_take_home_plus_super": 166097.0,
                "yearly_income_plus_super": 230724.0,
                "rate": 100,
                "hours": 8,
            },
        ),
        (
            42,
            8,
            0,
            {
                "yearly_income": 87696,
                "yearly_tax": 18968.2,
                "yearly_take_home": 68727.8,
                "yearly_super": 9208.08,
                "yearly_take_home_plus_super": 77935.88,
                "yearly_income_plus_super": 96904.08,
                "rate": 42,
                "hours": 8,
            },
        ),
        (
            75.69,
            11.43,
            20,
            {
                "yearly_income": 208497.94469999996,
                "yearly_tax": 64491.075114999985,
                "yearly_take_home": 144006.86958499998,
                "yearly_super": 21892.284193499996,
                "yearly_take_home_plus_super": 165899.15377849998,
                "yearly_income_plus_super": 230390.22889349997,
                "rate": 75.69,
                "hours": 11.43,
            },
        ),
    ],
)
def test_create_yearly_income_dict(
    daily_rate: float, daily_hours: float, leave_days: int, expected: dict
) -> None:
    assert utils.create_yearly_income_dict(daily_rate, daily_hours, leave_days, 2021) == expected


@pytest.mark.parametrize(
    "daily_rates, daily_hours, leave_days, expected",
    [
        (
            [27, 30, 35],
            8,
            6,
            {
                "27": {
                    "year": {
                        "yearly_income": 55080,
                        "yearly_tax": 8368.0,
                        "yearly_take_home": 46712.0,
                        "yearly_super": 5783.4,
                        "yearly_take_home_plus_super": 52495.4,
                        "yearly_income_plus_super": 60863.4,
                        "rate": 27,
                        "hours": 8,
                    },
                    "months": {
                        "monthly_income": 4590.0,
                        "monthly_tax": 697.3333333333334,
                        "monthly_take_home": 3892.6666666666665,
                        "monthly_super": 481.95,
                        "monthly_take_home_plus_super": 4374.616666666667,
                        "monthly_income_plus_super": 5071.95,
                        "rate": 27.0,
                        "hours": 8.0,
                    },
                    "biweeks": {
                        "biweekly_income": 2118.4615384615386,
                        "biweekly_tax": 321.84615384615387,
                        "biweekly_take_home": 1796.6153846153845,
                        "biweekly_super": 222.43846153846152,
                        "biweekly_take_home_plus_super": 2019.0538461538463,
                        "biweekly_income_plus_super": 2340.9,
                        "rate": 27.0,
                        "hours": 8.0,
                    },
                    "weeks": {
                        "weekly_income": 1080.0,
                        "weekly_tax": 164.07843137254903,
                        "weekly_take_home": 915.9215686274509,
                        "weekly_super": 113.39999999999999,
                        "weekly_take_home_plus_super": 1029.321568627451,
                        "weekly_income_plus_super": 1193.4,
                        "rate": 27.0,
                        "hours": 8.0,
                    },
                    "weekdays": {
                        "daily_income": 216.0,
                        "daily_tax": 32.8156862745098,
                        "daily_take_home": 183.1843137254902,
                        "daily_super": 22.68,
                        "daily_take_home_plus_super": 205.8643137254902,
                        "daily_income_plus_super": 238.68,
                        "rate": 27.0,
                        "hours": 8.0,
                    },
                    "hours": {
                        "hourly_income": 27.0,
                        "hourly_tax": 4.101960784313725,
                        "hourly_take_home": 22.898039215686275,
                        "hourly_super": 2.835,
                        "hourly_take_home_plus_super": 25.733039215686276,
                        "hourly_income_plus_super": 29.835,
                        "rate": 27.0,
                        "hours": 8.0,
                    },
                },
                "30": {
                    "year": {
                        "yearly_income": 61200,
                        "yearly_tax": 10357.0,
                        "yearly_take_home": 50843.0,
                        "yearly_super": 6426.0,
                        "yearly_take_home_plus_super": 57269.0,
                        "yearly_income_plus_super": 67626.0,
                        "rate": 30,
                        "hours": 8,
                    },
                    "months": {
                        "monthly_income": 5100.0,
                        "monthly_tax": 863.0833333333334,
                        "monthly_take_home": 4236.916666666667,
                        "monthly_super": 535.5,
                        "monthly_take_home_plus_super": 4772.416666666667,
                        "monthly_income_plus_super": 5635.5,
                        "rate": 30.0,
                        "hours": 8.0,
                    },
                    "biweeks": {
                        "biweekly_income": 2353.846153846154,
                        "biweekly_tax": 398.34615384615387,
                        "biweekly_take_home": 1955.5,
                        "biweekly_super": 247.15384615384616,
                        "biweekly_take_home_plus_super": 2202.653846153846,
                        "biweekly_income_plus_super": 2601.0,
                        "rate": 30.0,
                        "hours": 8.0,
                    },
                    "weeks": {
                        "weekly_income": 1200.0,
                        "weekly_tax": 203.07843137254903,
                        "weekly_take_home": 996.9215686274509,
                        "weekly_super": 126.0,
                        "weekly_take_home_plus_super": 1122.921568627451,
                        "weekly_income_plus_super": 1326.0,
                        "rate": 30.0,
                        "hours": 8.0,
                    },
                    "weekdays": {
                        "daily_income": 240.0,
                        "daily_tax": 40.615686274509805,
                        "daily_take_home": 199.3843137254902,
                        "daily_super": 25.2,
                        "daily_take_home_plus_super": 224.5843137254902,
                        "daily_income_plus_super": 265.2,
                        "rate": 30.0,
                        "hours": 8.0,
                    },
                    "hours": {
                        "hourly_income": 30.0,
                        "hourly_tax": 5.076960784313726,
                        "hourly_take_home": 24.923039215686273,
                        "hourly_super": 3.15,
                        "hourly_take_home_plus_super": 28.073039215686276,
                        "hourly_income_plus_super": 33.15,
                        "rate": 30.0,
                        "hours": 8.0,
                    },
                },
                "35": {
                    "year": {
                        "yearly_income": 71400,
                        "yearly_tax": 13672.0,
                        "yearly_take_home": 57728.0,
                        "yearly_super": 7497.0,
                        "yearly_take_home_plus_super": 65225.0,
                        "yearly_income_plus_super": 78897.0,
                        "rate": 35,
                        "hours": 8,
                    },
                    "months": {
                        "monthly_income": 5950.0,
                        "monthly_tax": 1139.3333333333333,
                        "monthly_take_home": 4810.666666666667,
                        "monthly_super": 624.75,
                        "monthly_take_home_plus_super": 5435.416666666667,
                        "monthly_income_plus_super": 6574.75,
                        "rate": 35.0,
                        "hours": 8.0,
                    },
                    "biweeks": {
                        "biweekly_income": 2746.153846153846,
                        "biweekly_tax": 525.8461538461538,
                        "biweekly_take_home": 2220.3076923076924,
                        "biweekly_super": 288.34615384615387,
                        "biweekly_take_home_plus_super": 2508.653846153846,
                        "biweekly_income_plus_super": 3034.5,
                        "rate": 35.0,
                        "hours": 8.0,
                    },
                    "weeks": {
                        "weekly_income": 1400.0,
                        "weekly_tax": 268.078431372549,
                        "weekly_take_home": 1131.921568627451,
                        "weekly_super": 147.0,
                        "weekly_take_home_plus_super": 1278.921568627451,
                        "weekly_income_plus_super": 1547.0,
                        "rate": 35.0,
                        "hours": 8.0,
                    },
                    "weekdays": {
                        "daily_income": 280.0,
                        "daily_tax": 53.615686274509805,
                        "daily_take_home": 226.3843137254902,
                        "daily_super": 29.4,
                        "daily_take_home_plus_super": 255.7843137254902,
                        "daily_income_plus_super": 309.4,
                        "rate": 35.0,
                        "hours": 8.0,
                    },
                    "hours": {
                        "hourly_income": 35.0,
                        "hourly_tax": 6.701960784313726,
                        "hourly_take_home": 28.298039215686273,
                        "hourly_super": 3.675,
                        "hourly_take_home_plus_super": 31.973039215686274,
                        "hourly_income_plus_super": 38.675,
                        "rate": 35.0,
                        "hours": 8.0,
                    },
                },
            },
        ),
    ],
)
def test_create_all_x_income_dicts_for_multiple_rate(
    daily_rates: list, daily_hours: float, leave_days: int, expected: dict
) -> None:
    assert (
        utils.create_all_x_income_dicts_for_multiple_rates(
            daily_rates, daily_hours, leave_days, 2021
        )
        == expected
    )
