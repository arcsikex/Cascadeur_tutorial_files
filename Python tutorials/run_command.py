# This is an assist file that can't run on its own it should be
# called from VSCode Code Runner extension with the .py file's full name as argument

import os
import sys
import subprocess


CASCADEUR_EXE_PATH = r"C:\Program Files\Cascadeur\cascadeur.exe"

if len(sys.argv) > 1:
    source_file_path = str(sys.argv[1])

    print(source_file_path)
    directory, filename = os.path.split(source_file_path)
    # Extract the last folder from the directory path
    last_folder = os.path.basename(directory)
    # Remove the file extension from the filename
    script_name, _ = os.path.splitext(filename)

    # Combine the last folder and script name using '.' as a separator
    command = f"{last_folder}.{script_name}"
    print("Running command:")
    print(CASCADEUR_EXE_PATH + " --run-script " + command)

    subprocess.Popen([CASCADEUR_EXE_PATH, "--run-script", command])
else:
    print("No arguments were given!")
