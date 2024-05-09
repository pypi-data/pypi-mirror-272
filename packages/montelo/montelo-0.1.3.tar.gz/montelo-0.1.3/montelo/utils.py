from datetime import datetime, UTC
from typing import Callable

from cuid2 import cuid_wrapper

cuid_generator: Callable[[], str] = cuid_wrapper()


def format_utc_date(d: datetime):
    return d.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


def get_current_utc_time():
    # Get the current time in UTC
    now_utc = datetime.now(UTC)
    # Return the formatted string
    return format_utc_date(now_utc)
