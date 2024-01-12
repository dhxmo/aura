import os
import subprocess

from aura.core.utils import read_aloud
from aura.intents.computer_search import computer_search

# List of drives to search
drives = ['~', 'C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\', 'H:\\', 'I:\\', 'J:\\', 'K:\\', 'L:\\', 'M:\\', 'N:\\',
          'O:\\', 'P:\\', 'Q:\\', 'R:\\', 'S:\\', 'T:\\', 'U:\\', 'V:\\', 'W:\\', 'X:\\', 'Y:\\', 'Z:\\']


def find_directory(name, search_path):
    # Get a list of all items in the directory
    items = os.listdir(search_path)

    # Filter the list to include only directories
    directories = [item for item in items if os.path.isdir(os.path.join(search_path, item))]

    # Check if the directory is in the list
    if name in directories:
        return os.path.join(search_path, name)


def find_dir_in_explorer(directory, drive=None):
    if drive is None:
        for drive in drives:
            drive_path = os.path.expanduser(drive) if drive == '~' else drive
            if os.path.exists(drive_path):
                result = find_directory(directory, drive_path)
                if result is not None:
                    computer_search(result)
    else:
        if os.path.exists(drive):
            result = find_directory(directory, drive)
            if result is not None:
                computer_search(result)


# dir -> format C:\\
def find_file_powershell(name, directory):
    if directory:
        if os.path.exists(os.path.join(directory, name)):
            subprocess.Popen(r'explorer /select,"{}"'.format(os.path.join(directory, name)))
            return

        # Define the PowerShell command
        command = (f'(Get-ChildItem -Path {directory} -Include {name} -Recurse -ErrorAction SilentlyContinue '
                   f'-File).FullName')

        # Execute the command and capture the output
        result = subprocess.run(['powershell', '-Command', command], stdout=subprocess.PIPE, text=True)

        # Split the output into lines
        lines = result.stdout.splitlines()

        if len(lines) > 1:
            # Extract the final subdirectory from each path
            directories = [os.path.basename(line) for line in lines]

            # Remove duplicates
            directories_list = list(set(directories))

            # Speak the directories if the length of lines is greater than 1
            directories_str = " "
            for directory in directories_list:
                directories_str += directory + ", "

            res = (f"File {name} was found in a few sub directories in {directory}. "
                   f"Which one would you like to open from {directories}?")

            read_aloud(res)
        elif len(lines) == 1:
            subprocess.Popen(r'explorer /select,"{}"'.format(lines[0]))
            # os.startfile(lines[0])
        else:
            read_aloud("No files were found")
