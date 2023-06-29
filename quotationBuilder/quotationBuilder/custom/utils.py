from math import isnan
import datetime
from django.contrib import admin


def float_nan_check(value):
    if isinstance(value, float):
        if isnan(value):
            return None
        else:
            return (value)
    else:
        return None


def format_datetime_str(value: datetime.datetime) -> str:
    if isinstance(value, datetime.datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return value


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


def round_float_none(value, ndigits):
    if isinstance(value, float):
        if isnan(value):
            return None
        else:
            return round(value, ndigits=ndigits)

    return None
