# pay_periods

Script to generate the start and end date for pay periods where pay
period each date is the month-day format `m_mmdd_mmdd` (e.g.,
`m_0101_0114`) for easy cutting and pasting.

## Usage

Install runtime dependencies:

``` bash
$ python3 -m pip install tabulate --upgrade
```

Run the script:

``` bash
$ python3 pay_periods.py list -s 2026-01-01

2026-01-02 15:54:28,761 - pay_periods.PayPeriods.list().57 -  INFO - Listing pay periods: days_per_pay_period=14; number_of_pay_periods=26; start_datetime=2026-01-01

pay_period
e_0101_0114
e_0115_0128
e_0129_0211
e_0212_0225
...
```
