#!/bin/bash

# Make the settings directory if it doesn't exist
mkdir -p "$HOME/.sunrise_alarm"

# Get the directory where this script is located
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Make a settings directory if it doesn't exist

# Add a cron job to run reenable_alarm.sh every day at noon (12:00 PM)
(crontab -l ; echo "0 12 * * * $script_dir/reenable_alarm.sh $HOME/.sunrise_alarm") | crontab -

# Add a cron job to run alarm_exec.py every 10 seconds
(crontab -l ; echo "* * * * * for i in {1..6}; do $script_dir/alarm_exec.py $HOME/.sunrise_alarm & sleep 10; done") | crontab -

echo "Cron jobs added successfully."
