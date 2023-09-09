#!/bin/bash

# Check if the number of arguments is not equal to 1
if [ $# -ne 1 ]; then
    echo "reenable_alarm usage: $0 <directory_path>"
    exit 1
fi

# Get the directory path from the command line argument
directory_path="$1"

# Check if the directory exists
if [ ! -d "$directory_path" ]; then
    echo "Error: Directory '$directory_path' does not exist."
    exit 1
fi

# Define the path to the disable_alarm file
disable_file="$directory_path/disable_alarm"

# Check if the disable_alarm file exists
if [ -f "$disable_file" ]; then
    # Remove the disable_alarm file
    rm "$disable_file"
    echo "Alarm re-enabled in '$directory_path'."
else
    echo "No disable_alarm file found in '$directory_path'. Nothing to re-enable."
fi
