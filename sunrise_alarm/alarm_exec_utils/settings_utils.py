import os
from datetime import time
from typing import NamedTuple


# Define a named tuple to store settings
class Settings(NamedTuple):
    start_time: time
    max_brightness_time: time
    intensity: float
    color: tuple[int, int, int]


# Function to load settings from the "alarm_settings.txt" file
def load_settings(base_path: str) -> Settings:
    try:
        with open(os.path.join(base_path, "alarm_settings.txt"), "r") as settings_file:
            lines = settings_file.readlines()

        # Parse lines from the settings file, excluding comments
        start_time_str = lines[0].split("#", 1)[0].strip()
        max_brightness_time_str = lines[1].split("#", 1)[0].strip()
        intensity_str = lines[2].split("#", 1)[0].strip()
        color_str = lines[3].split("#", 1)[0].strip()

        # Convert values to the appropriate types
        start_time = time.fromisoformat(start_time_str)
        max_brightness_time = time.fromisoformat(max_brightness_time_str)
        intensity = min(max(float(intensity_str), 0.0), 1.0)  # Clip intensity to [0, 1]
        color = tuple(int(x) for x in color_str.split())
        color = tuple(min(max(x, 0), 255) for x in color)  # Clip color to [0, 255]

        return Settings(start_time, max_brightness_time, intensity, color)

    except FileNotFoundError:
        # Handle missing settings file
        raise FileNotFoundError("The 'alarm_settings.txt' file does not exist.")


# Function to check if the "disable_alarm" file is present
def check_disabled(base_path: str) -> bool:
    return os.path.isfile(os.path.join(base_path, "disable_alarm"))
