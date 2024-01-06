import os
import subprocess


def find_directory(name, search_path):
    # Get a list of all items in the directory
    items = os.listdir(search_path)

    # Filter the list to include only directories
    directories = [item for item in items if os.path.isdir(os.path.join(search_path, item))]

    # Check if the directory is in the list
    if name in directories:
        return os.path.join(search_path, name)


# List of drives to search
drives = ['~', 'C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\', 'H:\\', 'I:\\', 'J:\\', 'K:\\', 'L:\\', 'M:\\', 'N:\\',
          'O:\\', 'P:\\', 'Q:\\', 'R:\\', 'S:\\', 'T:\\', 'U:\\', 'V:\\', 'W:\\', 'X:\\', 'Y:\\', 'Z:\\']

def find_dir_in_explorer(directory, drive=None):
   if drive is None:
       for drive in drives:
           drive_path = os.path.expanduser(drive) if drive == '~' else drive
           if os.path.exists(drive_path):
               result = find_directory(directory, drive_path)
               if result is not None:
                  return result
   else:
       if os.path.exists(drive):
           result = find_directory(directory, drive)
           if result is not None:
               return result


# dir -> format C:\\
def find_file_powershell(name, directory):
  # Define the PowerShell command
  command = f'(Get-ChildItem -Path {directory} -Include {name} -Recurse -ErrorAction SilentlyContinue -File).FullName'

  # Execute the command and capture the output
  result = subprocess.run(['powershell', '-Command', command], stdout=subprocess.PIPE, text=True)

  # Split the output into lines
  lines = result.stdout.splitlines()

  # Return the list of files
  return lines
