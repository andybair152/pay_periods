"""
Script to list pay periods in the month-day format "m_mmdd_mmdd" for
easy cutting and pasting.

Install runtime dependencies:

    $ python3 -m pip install tabulate --upgrade

Usage:

    $ python3 pay_periods.py list -s 2026-01-01

    2026-01-02 15:54:28,761 - pay_periods.PayPeriods.list().57 -  INFO - Listing pay periods: days_per_pay_period=14; number_of_pay_periods=26; start_datetime=2026-01-01

    pay_period
    e_0101_0114
    e_0115_0128
    e_0129_0211
    e_0212_0225
    ...

Formatted with black and isort:

    black -q -
    isort --force-single-line-imports -
"""


from argparse import ArgumentParser
from argparse import ArgumentTypeError
from datetime import datetime
from datetime import timedelta
from logging import getLogger
from logging.config import dictConfig
from re import search

from tabulate import tabulate

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LOG_FORMAT = "%(asctime)s - %(module)s.%(name)s.%(funcName)s().%(lineno)d -  %(levelname)s - %(message)s"


# pylint: disable=W1203


class PayPeriods:
    """
    Class to produce pay period dates.
    """

    def __init__(self):
        """
        Create object.
        """

        self.logger = getLogger(f"{self.__class__.__name__}")

    def list(
        self,
        days_per_pay_period,
        number_of_pay_periods,
        start_datetime,
    ):
        """
        Public method to generate the start and end date for pay
        periods where pay period each date is the month-day format
        "m_mmdd_mmdd" (e.g., m_0101_0114) for easy cutting and pasting.

        Args:
            days_per_pay_period: Number of days per pay perid
            number_of_pay_periods: Number of pay periods
            start_datetime: Beginning datetime string in the format
                YYYY-mm-dd

        Returns:
            List of dictionaries containing the start and end dates
            for each pay period

        """
        self.logger.info(
            f"Listing pay periods: days_per_pay_period={days_per_pay_period}; number_of_pay_periods={number_of_pay_periods}; start_datetime={start_datetime}"
        )

        response = []

        work_datetimes = []
        work_datetime = None

        for pay_period in range(number_of_pay_periods):
            if work_datetime:
                work_datetime = work_datetime + timedelta(days=days_per_pay_period)

            else:
                work_datetime = datetime.fromisoformat(start_datetime)

            work_datetimes.append(work_datetime)

        for work_datetime in work_datetimes:
            beg = work_datetime.strftime("%m%d")
            end = (work_datetime + timedelta(days=(days_per_pay_period - 1))).strftime(
                "%m%d"
            )

            item = f"e_{beg}_{end}"

            response.append({"pay_period": item})

        return response


def datetime_string(value):
    """
    Validates that the value is the datetime format YYYY-mm-dd
    """

    datetime_regex = r"^2[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$"
    match_datetime = search(datetime_regex, value)

    if not match_datetime:
        raise ArgumentTypeError(
            f"Invalid datetime string: datetime_regex={datetime_regex}; datetime_string={value}"
        )

    return value


if __name__ == "__main__":
    DEFAULT_DAYS_PER_PAY_PERIOD = 14
    DEFAULT_NUMBER_OF_PAY_PERIODS = 26

    ##################################################################
    # Parse command line arguments
    ##################################################################

    parser = ArgumentParser(add_help=True)

    parser.add_argument(
        "-L",
        "--log_level",
        default="DEBUG",
        choices=LOG_LEVELS,
        help="Log level",
    )

    sub_parsers = parser.add_subparsers(help="Sub-command help", dest="command")

    ##################################################################
    # list
    ##################################################################

    parser_list = sub_parsers.add_parser("list", help="List pay periods")
    parser_list.add_argument(
        "-d",
        "--days-per-pay-period",
        default=DEFAULT_DAYS_PER_PAY_PERIOD,
        type=int,
        help="Number of days in each pay period (default={DEFAULT_DAYS_PER_PAY_PERIOD})",
    )
    parser_list.add_argument(
        "-n",
        "--number-of-pay-periods",
        default=DEFAULT_NUMBER_OF_PAY_PERIODS,
        type=int,
        help="Number of pay periods (default={DEFAULT_NUMBER_OF_PAY_PERIODS})",
    )
    parser_list.add_argument(
        "-s",
        "--start-datetime",
        required=True,
        type=datetime_string,
        help="Start date in format YYYY-mm-dd",
    )

    ##################################################################
    # Parse arguments
    ##################################################################

    args = parser.parse_args()

    ##################################################################
    # Configure logger and initialize variables
    ##################################################################

    log_args = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"default": {"class": "logging.Formatter", "format": LOG_FORMAT}},
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": args.log_level,
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console"]},
    }

    dictConfig(log_args)
    logger = getLogger()

    ##################################################################
    # Do the work
    ##################################################################

    if args.command == "list":
        call_args = {
            "days_per_pay_period": args.days_per_pay_period,
            "number_of_pay_periods": args.number_of_pay_periods,
            "start_datetime": args.start_datetime,
        }
        pay_periods = PayPeriods()
        response = pay_periods.list(**call_args)
        print(tabulate(response, headers="keys", tablefmt="plain"))

    else:
        parser.print_help()
        exit(1)
