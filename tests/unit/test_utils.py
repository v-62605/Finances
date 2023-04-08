import numpy as np
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


@pytest.mark.parametrize(
    "base_rate, period, rates, daily_hours, leave_days, expected",
    [
        (
            30,
            "weekdays",
            np.arange(31, 34),
            8,
            5,
            {
                30: {
                    "daily_income": 0.0,
                    "daily_tax": 0.0,
                    "daily_take_home": 0.0,
                    "daily_super": 0.0,
                    "daily_take_home_plus_super": 0.0,
                    "daily_income_plus_super": 0.0,
                    "rate": 0.0,
                    "hours": 0.0,
                },
                31: {
                    "daily_income": 8.0,
                    "daily_tax": 2.6000000000000014,
                    "daily_take_home": 5.400000000000006,
                    "daily_super": 0.8399999999999999,
                    "daily_take_home_plus_super": 6.240000000000009,
                    "daily_income_plus_super": 8.840000000000032,
                    "rate": 1.0,
                    "hours": 0.0,
                },
                32: {
                    "daily_income": 16.0,
                    "daily_tax": 5.200000000000003,
                    "daily_take_home": 10.800000000000011,
                    "daily_super": 1.6799999999999997,
                    "daily_take_home_plus_super": 12.480000000000018,
                    "daily_income_plus_super": 17.680000000000007,
                    "rate": 2.0,
                    "hours": 0.0,
                },
                33: {
                    "daily_income": 24.0,
                    "daily_tax": 7.799999999999997,
                    "daily_take_home": 16.19999999999999,
                    "daily_super": 2.5199999999999996,
                    "daily_take_home_plus_super": 18.72,
                    "daily_income_plus_super": 26.52000000000004,
                    "rate": 3.0,
                    "hours": 0.0,
                },
            },
        ),
        (
            100,
            "weeks",
            np.arange(100, 111, 5),
            8,
            20,
            {
                100: {
                    "weekly_income": 0.0,
                    "weekly_tax": 0.0,
                    "weekly_take_home": 0.0,
                    "weekly_super": 0.0,
                    "weekly_take_home_plus_super": 0.0,
                    "weekly_income_plus_super": 0.0,
                    "rate": 0.0,
                    "hours": 0.0,
                },
                105: {
                    "weekly_income": 200.83333333333348,
                    "weekly_tax": 90.375,
                    "weekly_take_home": 110.45833333333303,
                    "weekly_super": 21.087500000000034,
                    "weekly_take_home_plus_super": 131.54583333333358,
                    "weekly_income_plus_super": 221.92083333333358,
                    "rate": 5.0,
                    "hours": 0.0,
                },
                110: {
                    "weekly_income": 401.6666666666665,
                    "weekly_tax": 180.75,
                    "weekly_take_home": 220.91666666666652,
                    "weekly_super": 42.174999999999955,
                    "weekly_take_home_plus_super": 263.09166666666624,
                    "weekly_income_plus_super": 443.84166666666624,
                    "rate": 10.0,
                    "hours": 0.0,
                },
            },
        ),
        (
            75,
            "biweeks",
            np.arange(80, 91, 5),
            8,
            20,
            {
                75: {
                    "biweekly_income": 0.0,
                    "biweekly_tax": 0.0,
                    "biweekly_take_home": 0.0,
                    "biweekly_super": 0.0,
                    "biweekly_take_home_plus_super": 0.0,
                    "biweekly_income_plus_super": 0.0,
                    "rate": 0.0,
                    "hours": 0.0,
                },
                80: {
                    "biweekly_income": 401.66666666666697,
                    "biweekly_tax": 148.6166666666668,
                    "biweekly_take_home": 253.05000000000018,
                    "biweekly_super": 42.174999999999955,
                    "biweekly_take_home_plus_super": 295.22500000000036,
                    "biweekly_income_plus_super": 443.84166666666715,
                    "rate": 5.0,
                    "hours": 0.0,
                },
                85: {
                    "biweekly_income": 803.333333333333,
                    "biweekly_tax": 297.2333333333331,
                    "biweekly_take_home": 506.10000000000036,
                    "biweekly_super": 84.34999999999991,
                    "biweekly_take_home_plus_super": 590.4499999999998,
                    "biweekly_income_plus_super": 887.6833333333334,
                    "rate": 10.0,
                    "hours": 0.0,
                },
                90: {
                    "biweekly_income": 1205.0,
                    "biweekly_tax": 445.85000000000014,
                    "biweekly_take_home": 759.1500000000005,
                    "biweekly_super": 126.52499999999998,
                    "biweekly_take_home_plus_super": 885.6750000000011,
                    "biweekly_income_plus_super": 1331.5250000000005,
                    "rate": 15.0,
                    "hours": 0.0,
                },
            },
        ),
        (
            43.56,
            "months",
            np.arange(31, 32),
            8,
            18,
            {
                31: {
                    "monthly_income": -2219.694545454545,
                    "monthly_tax": -721.4007272727271,
                    "monthly_take_home": -1498.293818181819,
                    "monthly_super": -233.06792727272727,
                    "monthly_take_home_plus_super": -1731.3617454545456,
                    "monthly_income_plus_super": -2452.7624727272732,
                    "rate": -12.560000000000002,
                    "hours": 0.0,
                },
                43: {
                    "monthly_income": -98.96727272727276,
                    "monthly_tax": -32.164363636363305,
                    "monthly_take_home": -66.80290909090854,
                    "monthly_super": -10.391563636363571,
                    "monthly_take_home_plus_super": -77.19447272727211,
                    "monthly_income_plus_super": -109.35883636363724,
                    "rate": -0.5600000000000023,
                    "hours": 0.0,
                },
            },
        ),
        (
            27.89,
            "year",
            np.arange(25, 31, 2),
            8,
            0,
            {
                25: {
                    "yearly_income": -6034.32,
                    "yearly_tax": -1961.1540000000005,
                    "yearly_take_home": -4073.1659999999974,
                    "yearly_super": -633.6035999999995,
                    "yearly_take_home_plus_super": -4706.7696,
                    "yearly_income_plus_super": -6667.923600000002,
                    "rate": -2.8900000000000006,
                    "hours": 0,
                },
                27: {
                    "yearly_income": -1858.3199999999997,
                    "yearly_tax": -603.9539999999997,
                    "yearly_take_home": -1254.3659999999945,
                    "yearly_super": -195.1235999999999,
                    "yearly_take_home_plus_super": -1449.4896000000008,
                    "yearly_income_plus_super": -2053.443600000006,
                    "rate": -0.8900000000000006,
                    "hours": 0,
                },
                29: {
                    "yearly_income": 2317.6800000000003,
                    "yearly_tax": 753.246000000001,
                    "yearly_take_home": 1564.434000000001,
                    "yearly_super": 243.35640000000058,
                    "yearly_take_home_plus_super": 1807.790399999998,
                    "yearly_income_plus_super": 2561.0364000000045,
                    "rate": 1.1099999999999994,
                    "hours": 0,
                },
            },
        ),
    ],
)
def test_compare_rates_to_base_rate(
    base_rate: float,
    period: str,
    rates: np.arange,
    daily_hours: float,
    leave_days: int,
    expected: dict,
) -> None:
    assert (
        utils.compare_rates_to_base_rate(base_rate, period, rates, daily_hours, leave_days, 2021)
        == expected
    )
