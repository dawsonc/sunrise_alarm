"""Utility functions for working with times."""
from datetime import time

from .settings_utils import Settings


def before(current_time: time, target_time: time) -> bool:
    """
    Check if the current time is before the target time.

    Args:
        current_time (time): The current time.
        target_time (time): The target time to compare with.

    Returns:
        bool: True if the current time is before the target time, False otherwise.
    """
    return current_time < target_time


def interpolate_times(current_time: time, time1: time, time2: time) -> float:
    """
    Compute the fraction of the duration between time1 and time2 that has elapsed.

    If current_time is before time1 or after time2, saturate at 0 or 1, respectively.

    Args:
        current_time (time): The current time.
        time1 (time): The starting time.
        time2 (time): The ending time.

    Returns:
        float: The fraction of the duration elapsed between time1 and time2 at the
            current time. Values are saturated at 0 and 1 if the current time is
            outside this range.

    Raises:
        ValueError: If time1 is after time2.
    """
    if time1 > time2:
        raise ValueError("time1 cannot be after time2")

    total_seconds_between = (time2.hour * 3600 + time2.minute * 60 + time2.second) - (
        time1.hour * 3600 + time1.minute * 60 + time1.second
    )

    if current_time < time1:
        return 0.0
    elif current_time > time2:
        return 1.0
    else:
        elapsed_seconds = (
            current_time.hour * 3600 + current_time.minute * 60 + current_time.second
        ) - (time1.hour * 3600 + time1.minute * 60 + time1.second)
        return elapsed_seconds / total_seconds_between


def get_desired_intensity(current_time: time, settings: Settings) -> float:
    """
    Compute the desired intensity for the current time.

    Args:
        current_time (time): The current time.
        settings (Settings): The alarm settings.

    Returns:
        float: The desired intensity for the current time.
    """
    return settings.intensity * interpolate_times(
        current_time, settings.start_time, settings.max_brightness_time
    )
