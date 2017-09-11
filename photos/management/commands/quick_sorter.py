#!/usr/bin/env python

import sys
import exifread
from os.path import join
import fnmatch
import time
import os
import uuid
import getopt
import filecmp
import shutil

class QuickSorter:

    directory_listing = dict()
    debug = False

    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory

    def get_listing(self):
        files = []
        for root, dirnames, filenames in os.walk(self.input_directory):
            print("search:", root)
            for ext in ('*.gif', '*.png', '*.jpg', '*.jpeg','*.JPEG','*.JPG', '*.PNG', '*.MOV', '*.mov', '*.mts', '*.MTS','*.mp4','*.MP4', '*.mxf', '*.MXF', '*.wmv', '*.WMV', '*.3g2', '*.3G2', '*.avi', '*.AVI', '*.bmp', '*.BMP', '*.mpg', '*.MPG', '*.tif', '*.TIF', '*.3pg', '*.3PG'):
                for filename in fnmatch.filter(filenames, ext):
                    files.append(os.path.join(root, filename))
        print("listing:", len(files))
        self.directory_listing = files
    
    # Print iterations progress
    def printProgressBar (self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '*'):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
        # Print New Line on Complete
        if iteration == total: 
            print()

    def read_files_information(self):
        intTotal = len(self.directory_listing)
        intCount = 0
        for file_image in self.directory_listing:
            self.printProgressBar(intCount,intTotal)
            intCount =+ 1
            try:
                file_current = open(file_image, 'rb')
                try:
                    tags_image = exifread.process_file(file_current, details=False)
                    if 'EXIF DateTimeOriginal' in tags_image:
                        date_time_stamp = time.strptime(str(tags_image['EXIF DateTimeOriginal']) + 'UTC', '%Y:%m:%d %H:%M:%S%Z')
                        # print(file_image, date_time_stamp)
                        self.sort(file_image, date_time_stamp)
                    else:
                        date_time_stamp = time.strptime(time.ctime(os.path.getmtime(file_image)))
                        # print(file_image, tags_image.keys(), date_time_stamp)
                        self.sort(file_image, date_time_stamp)
                except Exception as e_time:
                    print("error:", "exifread", file_image, e_time)
                finally:
                    file_current.close()
            except Exception as e:
                print("error:", "read_file_information", file_image, e)
                pass
            

    def sort(self, current_file_path, date_time_stamp):
        # print(date_time_stamp.tm_year, date_time_stamp.tm_mon, date_time_stamp.tm_mday)
        current_file_path_details = os.path.split(current_file_path)
        new_file_path = os.path.join(self.output_directory,
            str(date_time_stamp.tm_year),
            str(date_time_stamp.tm_mon),
            str(date_time_stamp.tm_mday))
        new_file_name = os.path.join(new_file_path, current_file_path_details[1])
        if not os.path.exists(new_file_path) and not self.debug:
            os.makedirs(new_file_path)
        if not os.path.exists(new_file_name):
            if not self.debug:
                shutil.move(current_file_path, new_file_name)
            print("moved:" , current_file_path, new_file_name)
        # elif not current_file_path == new_file_name and filecmp.cmp(current_file_path, new_file_name):
        #    print("duplicate:", "identical", "removing", current_file_path)
        #   if not self.debug:
        #       os.remove(current_file_path)
        else:
            duplicate_file_path = os.path.join(new_file_path, 'duplicate')
            if not os.path.exists(duplicate_file_path) and not self.debug:
                os.makedirs(duplicate_file_path)
            temp_base, temp_extension = os.path.splitext(os.path.basename(current_file_path))
            unique = uuid.uuid4()
            duplicate_file_name = os.path.join(duplicate_file_path, ("%s_%s%s" % (temp_base, str(unique), temp_extension)) )
            if not self.debug:
                shutil.move(current_file_path, duplicate_file_name)
            print("duplicate:", current_file_path, new_file_name, duplicate_file_name)
            
        # Clean Up
        if os.path.exists(os.path.join(current_file_path_details[0],'Thumbs.db')):
            os.remove(os.path.join(current_file_path_details[0],'Thumbs.db'))
            print("remove:", "thumbs.db")
        if not os.listdir(current_file_path_details[0]):
            os.rmdir(current_file_path_details[0])
            print("remove:", "empty-directory", current_file_path_details[0])


if __name__ == "__main__":
    try:
        options, args = getopt.getopt(sys.argv[1:],"i:o:")
    except getopt.GetoptError as e:
        print (str(e))
        print("Usage: %s -i input -o output" % sys.argv[0])
        sys.exit(2)

    input_directory = ""
    output_directory = "sorted"
    for operator, argument in options:
        if operator == '-i':
            input_directory = argument
            print("input:", input_directory)
        elif operator == '-o':
            output_directory = argument
            print("output:", output_directory)

    sort = QuickSorter(input_directory=input_directory,output_directory=output_directory)
    print("getting-files:")
    sort.get_listing()
    print("reading-moving:")
    sort.read_files_information()
    print("done:")

