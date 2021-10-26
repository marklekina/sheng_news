#!/bin/python
#
# file_convertor.py - handles the conversion of news article files (.pdf files) to text files
#
#
# Mark Lekina Rorat, Jun, July, Sept, Oct 2021


import os
import subprocess


# removes whitespace from file titles for easier processing by the subprocess module
def rename_files(source_dir):
    filenames = os.listdir(source_dir)
    for filename in filenames:
        new_filename = "".join(filename.split())
        source_name = os.path.join(source_dir, filename)
        dest_name = os.path.join(source_dir, new_filename)
        os.rename(source_name, dest_name)


# takes pdf files from a source directory as input, converts them to txt files and stores them in the destination
# directory. PDF (.pdf) to text (.txt) conversion is handled by the (external) pdf2txt module
def convertPDFtoTXT(source_dir, dest_dir):
    filenames = os.listdir(source_dir)
    for filename in filenames:
        source_filename = os.path.join(source_dir, filename)
        dest_filename = os.path.join(dest_dir, filename[:-3] + "txt")
        cmd = ["pdf2txt.py", "-o", dest_filename, source_filename]
        subprocess.run(cmd)


def main():
    rename_files("raw_data/raw_files")
    convertPDFtoTXT("raw_data/raw_files", "raw_data/converted_files")


if __name__ == "__main__":
    main()
