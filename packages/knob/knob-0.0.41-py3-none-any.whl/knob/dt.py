# -*- coding:utf-8 -*-

__all__ = ['local_now', 'local_today', 'local_time', 'naive_time']

import six
from django.utils import timezone
from dt_utils import T


def local_now():
    return timezone.now().astimezone(timezone.get_current_timezone())


def local_today():
    return local_now().date()


def local_time(raw_time):
    if raw_time is None:
        return None

    time = T(raw_time)
    if timezone.is_aware(time):
        return timezone.localtime(time)
    else:
        return timezone.make_aware(time)


def naive_time(raw_time):
    if raw_time is None:
        return None

    time = T(raw_time)
    if timezone.is_aware(time):
        # make local first, lest the result is based on a wrong timezone
        return timezone.make_naive(timezone.localtime(time))
    else:
        return time
