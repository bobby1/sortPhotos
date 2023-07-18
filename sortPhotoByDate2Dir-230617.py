#! /usr/bin/python
# =============================================================================
# Created on Sat Jun 17 10:57:37 2023
#
# @author: b1
# Program to delete duplicate jpg filesProgram to sort jpg into directories by shoot date
#
# The modification in this version is in the sort_photos_by_date function. Instead of creating separate year, month, and day directories, it directly creates a single directory with the "yyyy-MM-dd" format using shoot_date.strftime("%Y-%m-%d").
# 
# Remember to replace "path/to/source/directory" and "path/to/destination/directory" with the actual paths to your source and destination directories, respectively.
# import os
# =============================================================================
import os
import shutil
from datetime import datetime
from PIL import Image


def get_photo_date(photo_path):
    """Extracts the shoot date from the photo metadata."""
    try:
        with Image.open(photo_path) as img:
            info = img._getexif()
            if info is not None and 36867 in info:
                shoot_date_str = info[36867]
                shoot_date = datetime.strptime(shoot_date_str, "%Y:%m:%d %H:%M:%S")
                return shoot_date
    except (OSError, KeyError, ValueError):
        pass

    # Return None if the shoot date couldn't be extracted
    return None


def sort_photos_by_date(source_dir, destination_dir):
    """Sorts photos by shoot date and moves them to different directories based on the date."""
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for filename in os.listdir(source_dir):
        photo_path = os.path.join(source_dir, filename)
        if os.path.isfile(photo_path) and filename.lower().endswith('.jpg'):
            shoot_date = get_photo_date(photo_path)
            if shoot_date is not None:
                date_str = shoot_date.strftime("%Y-%m-%d")
                date_dir = os.path.join(destination_dir, date_str)
                os.makedirs(date_dir, exist_ok=True)

                destination_path = os.path.join(date_dir, filename)
                #shutil.move(photo_path, destination_path)
                shutil.copy(photo_path, destination_path)
                print(f"Copied {filename} to {destination_path}")
            else:
                print(f"Couldn't extract shoot date for {filename}")

# Example usage:
# source_directory = "path/to/source/directory"
# destination_directory = "path/to/destination/directory"

source_directory = "C:/Users/b1/Pictures/2023Graduations/Graduation 2022 Nic and Sam"
destination_directory = "C:/Users/b1/Pictures/hold"

sort_photos_by_date(source_directory, destination_directory)
