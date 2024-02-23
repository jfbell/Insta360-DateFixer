#!/usr/bin/env python3

"""
Created on Feb 23 2024

This script processes files and directories created by Insta360 Studio in a given directory and decodes 
the date and time from the file and directory names.It then writes the date and time to the 
file and directory metadata.

The script is executed from the command line and takes a single argument, the directory to process.

The script processes all files and directories in the given directory and its subdirectories.
For each file, it decodes the date and time from the filename, writes the date and time to the file's metadata, and calculates and prints the time shift in hours and minutes.
For each directory, it decodes the date and time from the directory name and writes the date and time to the directory's metadata.

"""

import os
import time
from datetime import datetime
import re
import click 


# Assuming decodeDateTime is a function that decodes date and time from a filename
def decodeDateTime(fileName):
    regex = r"(.+?)_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})"
    match = re.search(regex, fileName)
    if match:
        _, year, month, day, hour, minute, second = match.groups()
        return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    else:
        raise ValueError('Invalid file name format')
        

def process_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(".mp4") or file_path.endswith(".jpg") or file_path.endswith(".mov"):
                try:
                    print(f'Processing file: {file_path}')
                    # Decode the date and time from the filename
                    fileDateTime = decodeDateTime(file)
                    # Print the file's current created date
                    stats = os.stat(file_path)
                    print(f"File: {file} created at: {time.ctime(stats.st_ctime)}")
                    # Write the date and time to the file's metadata
                    os.utime(file_path, (fileDateTime.timestamp(), fileDateTime.timestamp()))

                    # calculate and print time shift in hours and minutes for the file
                    time_shift = fileDateTime - datetime.fromtimestamp(stats.st_ctime)
                    print(f"Time shift: {time_shift.days} days, {time_shift.seconds//3600} hours, {(time_shift.seconds//60)%60} minutes")
                except Exception as e:
                    print(f'Error processing file: {e}')
                    continue
        
        for dir in dirs:
            try:
                dir_path = os.path.join(root, dir)
                print(f'Processing directory: {dir_path}')
                # Decode the date and time from the directory name
                dirDateTime = decodeDateTime(dir)
                # Write the date and time to the directory's metadata
                os.utime(dir_path, (dirDateTime.timestamp(), dirDateTime.timestamp()))
            except Exception as e:
                print(f'Error processing directory: {e}')
                continue

# def main(directory):
#     process_files(directory)
#     print('Date and time decoded and written to metadata')

import tkinter as tk
from tkinter import filedialog

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    directory = filedialog.askdirectory()  # Open a dialog to choose a directory
    if directory:
        process_files(directory)
        tk.messagebox.showinfo("Success", "Date and time decoded and written to metadata")
    else:
        tk.messagebox.showerror("Error", "No directory selected")

if __name__ == "__main__":
    main()


# pyinstaller --name 'FixingX360Dates' \
#             --icon 'FixingX360Dates.ico' \
#             --onefile \
#             FixingX360Dates.py