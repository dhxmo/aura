import os
import shutil
import subprocess

import pyuac


def tesseract_install():
    # Define the URL and local filename for the Tesseract installer
    # url = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe"

    filename = os.path.join(os.getcwd(), 'aura', 'assets', 'Tesseract-OCR', 'tesseract-installer.exe')

    # Check if the script is running with admin privileges
    if not pyuac.isUserAdmin():
        # If not, re-launch the script with admin privileges
        pyuac.runAsAdmin()

    # Run the installer
    subprocess.run([filename], check=True)

    # Clone the tessdata repository
    # subprocess.run(['git', 'clone', 'https://github.com/tesseract-ocr/tessdata'], check=True)

    tessdata_filename = os.path.join(os.getcwd(), 'aura', 'assets', 'Tesseract-OCR', 'tessdata')

    # Copy the contents of the cloned repository to the Tesseract tessdata directory
    shutil.copytree(tessdata_filename, 'C:\\Program Files\\Tesseract-OCR\\tessdata')

    # removing installer
    os.remove(filename)
