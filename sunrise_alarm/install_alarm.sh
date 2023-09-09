#!/bin/bash

# Make the settings directory if it doesn't exist
mkdir -p "$HOME/.sunrise_alarm"

# Get the directory where this script is located
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# TODO make fcserver run on boot

# Add a cron job to run reenable_alarm.sh every day at midnight (12:00 AM)
(crontab -l ; echo "0 0 * * * $script_dir/reenable_alarm.sh $HOME/.sunrise_alarm >> $HOME/.sunrise_alarm/logfile 2>&1") | crontab -

# Add a cron job to run alarm_exec.py every 10 seconds
(crontab -l ; echo "* * * * * $script_dir/alarm_exec.py $HOME/.sunrise_alarm  >> $HOME/.sunrise_alarm/logfile 2>&1") | crontab -
(crontab -l ; echo "* * * * * sleep 10; $script_dir/alarm_exec.py $HOME/.sunrise_alarm  >> $HOME/.sunrise_alarm/logfile 2>&1") | crontab -
(crontab -l ; echo "* * * * * sleep 20; $script_dir/alarm_exec.py $HOME/.sunrise_alarm  >> $HOME/.sunrise_alarm/logfile 2>&1") | crontab -
(crontab -l ; echo "* * * * * sleep 30; $script_dir/alarm_exec.py $HOME/.sunrise_alarm  >> $HOME/.sunrise_alarm/logfile 2>&1") | crontab -
(crontab -l ; echo "* * * * * sleep 40; $script_dir/alarm_exec.py $HOME/.sunrise_alarm  >> $HOME/.sunrise_alarm/logfile 2>&1") | crontab -
(crontab -l ; echo "* * * * * sleep 50; $script_dir/alarm_exec.py $HOME/.sunrise_alarm  >> $HOME/.sunrise_alarm/logfile 2>&1") | crontab -

echo "Cron jobs added successfully."
