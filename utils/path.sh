#!/usr/bin/env bash

# Get the PATH environment variable
path=$PATH

# Expand the '~' character to the user's home directory
home_dir=$HOME

# Create the .config folder if it does not exist
config_dir=$home_dir/.config
if [ ! -d "$config_dir" ]; then
    mkdir -p "$config_dir"
fi

# Write the PATH variable to the file in the .config folder
file_path=$config_dir/path.txt
echo "$path" > "$file_path"
