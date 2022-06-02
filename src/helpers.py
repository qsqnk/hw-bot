from datetime import datetime
from datetime import timedelta

"""

Format: '%d/%m/%y %H:%M'
         day/month/year hours:minutes
Example: 01/02/21 23:43

"""

DATE_FORMAT = '%d/%m/%y %H:%M'


def utc_current_time():
    return datetime.utcnow()


def to_utc(dt, delta=3):
    return dt + timedelta(hours=-delta)


def datetime_check_format(date):
    try:
        datetime.strptime(date, DATE_FORMAT)
        return True
    except:
        return False


def datetime_from_str(date):
    return datetime.strptime(date, DATE_FORMAT)


def datetime_to_str(date):
    return date.strftime(DATE_FORMAT)


def difference_in_days(dt1, dt2):
    def to_days(d):
        return d.year * 365 + d.month * 30 + d.day

    return to_days(dt1) - to_days(dt2)

def text_after_prefix(prefix, text: str):
    return text.partition(prefix)[2].strip()