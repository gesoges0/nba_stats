from datetime import datetime


def get_current_datetime() -> datetime:
    """
    :return: current datetime
    """
    return datetime.now()


def convert_datetime_to_yyyymmdd(dt: datetime) -> str:
    """
    :param dt:
    :return: YYYYMMDD
    """
    return dt.strftime('%Y%m%d')


def get_current_datetime_with_yyyymmdd_format() -> str:
    """
    :return: YYYYMMDD
    """
    current_datetimie = get_current_datetime()
    return convert_datetime_to_yyyymmdd(current_datetimie)
