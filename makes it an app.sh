#!/bin/bash

# Check if PyInstaller is installed
if pip3 show pyinstaller &>/dev/null; then
    echo PyInstaller is installed
else
    echo PyInstaller is not installed
    exit 1
fi

# Run the PyInstaller command
pyinstaller --name 'FixingX360Dates' \
            --icon 'FixingX360Dates.png' \
            --onefile \
            FixingX360Dates.py