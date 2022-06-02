from datetime import datetime

"""

Format: year-month-day
Example: 2022-12-31

"""

DATE_FORMAT = '%Y-%m-%d'


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


def text_after_prefix(prefix, text: str):
    return text.partition(prefix)[2].strip()
