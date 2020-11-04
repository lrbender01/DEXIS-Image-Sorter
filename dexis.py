# Sort dexis images within a directory by patient names within image binaries
# Luke Bender (lrbender01@gmail.com) 8-7-20

import re
import os
import shutil
import sys
import time
from pathlib import Path

# Binary regular expression to match names
pattern = re.compile(b"\0[-A-Za-z\.\s'\(\)0-9\xF1]+\^[-A-Za-z\s'\(\)\xF1]+[-A-Za-z\.\s\^'\(\)0-9\xF1]*\0")


def update_progress(percent):
    # Set length for progress bar
    length = 200

    # Current bar length
    bar_length = int(round(length * percent))

    # Formatted bar string to be printed
    bar = '\r[{0}] {1}%'.format('#' * bar_length + '-' * (length - bar_length), round(percent * 100, 2))

    # Write bar and flush
    sys.stdout.write(bar)
    sys.stdout.flush()


def get_name(path):
    # Open bytes in file and read into file_bytes
    try:
        byte_file = open(path, 'rb')
        file_bytes = byte_file.read()
        byte_file.close()
    except:
        print('Unable to open:\t' + path)
        exit(1)

    # Find all matches for pattern regular expression
    matches = re.findall(pattern, file_bytes)

    # Try to find name matches
    try:
        # Pick out the last match, strip 0-bytes, and decode with UTF-8
        name = matches[-1][1:-1].decode('utf-8')

        # Replace all ^ characters with spaces
        return name.replace('^', ' ')
    # If there are no matches, return for error checking
    except:
        print('\r' + path + '\tIRREGULAR NAME')
        sys.stdout.flush()
        return '__IRREGULAR_NAME__'


def main():
    # Get search and target folders
    search_folder = input('Search folder: ')
    target_folder = input('Target folder: ')

    # Start timer
    start_time = time.time()

    # Check that folders are valid
    if not os.path.exists(search_folder):
        print('Invalid search folder.')
        exit(1)

    if not os.path.exists(target_folder):
        print('Invalid target folder.')
        exit(1)

    # Get all paths to dexis images and record the number found
    image_list = Path(search_folder).glob('**/*.dex')

    # Count number of images and track number done for progress bar
    count_list = Path(search_folder).glob('**/*.dex')
    num_images = len(list(count_list))
    count = 0

    # Print number of images found
    print(str(num_images) + " X-rays found.")

    # Iterate through all images
    for image in image_list:
        # Directory where the image belongs
        path = os.path.join(target_folder, get_name(str(image)))

        # Check if the directory exists and put the image there
        if os.path.exists(path):
            shutil.copy2(str(image), path)
        else:
            os.mkdir(path)
            shutil.copy2(str(image), path)

        # Increment number processed and update progress bar
        count = count + 1
        update_progress(float(count / num_images))

        # Error / progress checking
        # print(str(count) + ':\t' + str(image) + '\t->\t' + str(path) + '\t' + get_name(str(image)))

    total_time = time.time() - start_time

    print('\nDONE in ' + str(round(total_time, 3)) + ' seconds.')


if __name__ == '__main__':
    main()