# Sunrise alarm clock design notes

## User stories

- I want to be woken gently by a light that gently fades from dark to bright.
- I want to set the time at which the light turns on, and how fast the light turns on.
- I want to set the color of the light in RGB.
- I want to use a web interface to manage the alarm settings.
- I want to use a web interface to turn the alarm off.

## Design

There will be several components:

- **alarm_settings.txt**: a text file containing the current settings for the alarm.
- **disable_alarm**: a file that, if present, prevents the alarm from running.
- **reenable_alarm**: deletes the disable_alarm file, if present, every afternoon (cron job).
- **alarm_exec**: a service that controls the brightness of the LEDs over time.
- **alarm_manager**: a service that exposes a RESTful API for managing alarm settings.
- **alarm_frontend**: a webpage that allows the user to manage alarm settings.

### Settings files

`alarm_settings.txt` will have the following structure. Comments are allowed; all text after the first `#` on each line will be ignored.

```
HH:MM     # alarm start time
HH:MM     # alarm maximum brightness time
XX        # fraction of maximum LED power at max brightness; float [0, 1] (values >1 will be clipped to 1)
RR GG BB  # color of alarm; int [0, 255]
```

The contents of the `disable_alarm` file will be ignored; only the presence or absence of this file is checked.

### `cron` jobs

The `reenable_alarm` and `alarm_exec` services will be run as `cron` jobs.

`reenable_alarm` will be run once per day, at noon.

`alarm_exec` will be run every 10 seconds. It will:

- Connect to the LEDs.
- Check if the alarm is disabled. If so, turn LEDs off and exit.
- Read settings from the settings file.
- Check the current time.
    - If it is before the turn-on time, turn LEDs off.
    - If it is between the turn-on and max-brightness times, turn the LEDs to the appropriate brightness.
    - If it is after the max-brightness time, turn the LEDs to full brightness.

This will require the following subcomponents:

- LED interface
    - `connect()`: connect to the LEDs (e.g. if required by neopixels/fadecandy).
    - `set(rgb, intensity)`: set the desired RGB color and intensity.
- Settings interface
    - `load_settings() -> SettingsStruct`: load the settings from a file and return a struct
    - `check_disabled() -> bool`: check if the `disable_alarm` file is present
- Other functions
    - `get_desired_intensity(current_time, settings_struct)`: get the desired intensity (0 to 1) of the LEDs at the given time, accounting for the specified maximum intensity in the settings.
    - `before(current_time, target_time) -> bool` check if the current time is before the target time
    - `interpolate_times(current_time, time1, time2) -> float` compute the fraction of the duration between time1 and time2 that has elapsed at the current time. If the current time is before time1 or after time2, saturate at 0 and 1, respectively. Throw an error if time1 is after time2.
