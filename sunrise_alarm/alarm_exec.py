#!/usr/bin/python3
import argparse
from datetime import datetime

from alarm_exec_utils.time_utils import before, get_desired_intensity
from alarm_exec_utils.settings_utils import load_settings, check_disabled
from alarm_exec_utils.led_interface import LEDInterface, FadecandyInterface


def main(leds: LEDInterface, settings_dir: str):
    """
    Run the alarm.

    Args:
        leds: An LEDInterface object.
        settings_dir: The directory containing the alarm settings file.
    """
    # Connect to the LED interface
    leds.connect()

    settings = load_settings(settings_dir)
    if check_disabled(settings_dir):
        # If alarm is disabled, turn off LEDs and exit
        print("[alarm_exec] Alarm is disabled.")
        leds.set((0, 0, 0), 0)
    else:
        current_time = datetime.now().time()

        if before(current_time, settings.start_time):
            # If it's before the turn-on time, turn off LEDs
            print(f"[alarm_exec] Current time {current_time} before the turn-on time {settings.start_time}.")
            leds.set((0, 0, 0), 0)
        elif before(current_time, settings.max_brightness_time):
            # If it's between turn-on and max-brightness times, set LEDs to appropriate brightness
            desired_intensity = get_desired_intensity(current_time, settings)
            print(f"[alarm_exec] Current time {current_time}; fading LEDs to {desired_intensity}")
            leds.set(settings.color, desired_intensity)
        else:
            # If it's after the max-brightness time, set LEDs to full brightness
            print(f"[alarm_exec] Current time {current_time}; setting LEDs to full {settings.intensity}")
            leds.set(settings.color, settings.intensity)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the sunrise alarm.")
    parser.add_argument(
        "settings_dir",
        type=str,
        help="Path to the directory containing the alarm settings.",
    )
    args = parser.parse_args()

    leds = FadecandyInterface()

    main(leds, args.settings_dir)
