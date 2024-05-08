"""Holidays tracking."""

import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar


def n_us_business_day_offset(days: int, dates: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """Return offsetted dates by business day."""
    max_date = dates.max()
    holidays = _get_us_federal_holidays(max_date)
    offsetter = pd.tseries.offsets.CustomBusinessDay(n=days, holidays=holidays)
    return dates + offsetter


def _get_us_federal_holidays(
    end_date: pd.Timestamp, start_date: pd.Timestamp = pd.Timestamp(2022, 1, 1)
) -> pd.DatetimeIndex:
    """Return US Federal holidays in date interval."""
    calendar = USFederalHolidayCalendar()
    return calendar.holidays(start=start_date, end=end_date)
