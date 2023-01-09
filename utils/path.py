import os


def write_to_file(file, contents):
    with open(file, 'w') as f:
        f.write(contents)


# Get the PATH environment variable
path = os.environ['PATH']

# Expand the '~' character to the user's home directory
home_dir = os.path.expanduser('~')

# Create the .config folder if it does not exist
config_dir = os.path.join(home_dir, '.config')
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

# Write the PATH variable to the file in the .config folder
file_path = os.path.join(config_dir, 'path.txt')
write_to_file(file_path, path)
