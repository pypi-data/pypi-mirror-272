# Copyright (c) 2024 구FS, all rights reserved. Subject to the MIT licence in `licence.md`.
import datetime as dt
import math
import time


def sleep_mod(sleep_modulus: int) -> None:
    """
    Blockingly sleeps until the current unix time modulus sleep_modulus equals 0.

    Arguments:
    - sleep_modulus: the modulus to use to determin when to stop sleeping
    """

    now_dt: dt.datetime     # now
    return_dt: dt.datetime  # when to return

    now_dt=dt.datetime.now(dt.timezone.utc)
    return_dt=now_dt-dt.timedelta(seconds=now_dt.timestamp()%sleep_modulus)+dt.timedelta(seconds=sleep_modulus)


    sleep_until(return_dt)  # sleep until calculated return time

    return


def sleep_until(return_dt: dt.datetime) -> None:
    """
    Blockingly sleeps until the specified datetime and then returns. Expects timezone-aware datetime object.

    Arguments:
    - return_dt: the datetime when to return
    """

    now_dt: dt.datetime             # now
    time_until_return: dt.timedelta # how long still until return
    time_to_sleep: float            # how many seconds is next sleep? depends on time_until_return magnitude


    while (now_dt:=dt.datetime.now(dt.timezone.utc))<return_dt:                             # as long as return datetime not reached yet: sleep
        time_until_return=return_dt-now_dt                                                  # update time until return
        try:
            time_to_sleep=10**(math.floor(math.log10(time_until_return.total_seconds()))-1) # time to sleep is 1 magnitude smaller than time until return
        except ValueError:                                                                  # in case time until return is exactly 0: log10 crashes, give time to sleep 0
            time_to_sleep=0
        if time_to_sleep<1e-3:
            time_to_sleep=1e-3                                                              # sleep at least 1ms, otherwise needlessly computing for anyways inaccurate result

        time.sleep(time_to_sleep)

    return