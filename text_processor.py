#!/bin/python
#
# text_processor.py - cleans the converted news article files (.txt files), compiles the text in each of the files into two
# files: a training and a testing set, and standardizes the training and testing sets
#
# Mark Lekina Rorat, Jun, July, Sept, Oct 2021

import os
import re


# helper function for the clean_files function (see below)
def clean_file(input_file, output_file):
    regex = r'(([A-Z]+ +)|[A-Z][A-Z]+)|(People Daily)|(([0-9]+/[0-9]+/[0-9]+).+)|(http.+)|(Page .+)|(MANU ' \
            r'?SCRIBES|Manu ?scribes)|(URADI|Uradi)|(TAMBU ?LIKA|TAMU ?LIKA|Tamb ?ulika|Tamu ?lika)|(Fomu ?Ni(' \
            r'Safi)?\??|FOMU ?NI(SAFI)?\??)|(MANUEL NTOYAI|Manuel Ntoyai)|(NAFSI ?HURU|Nafsi ?Huru)|(([A-Z]+ +)|[' \
            r'A-Z][A-Z]+)|(\n)'

    # open input file for reading
    i_file = open(input_file, "r")
    text = i_file.read()

    # process text
    text = text.encode("ascii", "ignore").decode()
    text = re.sub(regex, " ", text)
    text = re.split(r'[.?!] *', text)
    text = '\n'.join(text).strip()
    text = re.sub('(\n)+', '\n', text)
    text = re.sub('( )+', ' ', text)
    text = re.sub(r'[^\w\s\n]', '', text).lower()
    # close file
    i_file.close()

    # open output file, write and close file
    o_file = open(output_file, "w")
    o_file.write(text)
    o_file.close()


# takes in raw text files from a directory and returns clean text files in a destination directory
def clean_files(source_dir, dest_dir):
    filenames = os.listdir(source_dir)
    for filename in filenames:
        input_path = os.path.join(source_dir, filename)
        output_path = os.path.join(dest_dir, filename)
        clean_file(input_path, output_path)


# cleans and standardizes the training and testing sets
def clean_sentences(raw_file):
    # open file for reading
    file = open(raw_file, 'r')
    lines = file.readlines()
    file.close()

    # open file for writing
    file = open(raw_file, 'w')
    sentences = []
    for line in lines:
        if len(line) > 1 and not line.isspace():
            sentences.append(line)
    file.writelines(sentences)
    file.close()


# takes in a directory of files as input and compiles all text files in the directory into a single file
def compile_single_text(source_dir, output_file):
    o_file = open(output_file, 'w')
    filenames = os.listdir(source_dir)
    for filename in filenames:
        file = os.path.join(source_dir, filename)
        i_file = open(file, 'r')
        text = i_file.read()
        o_file.write(text)
        o_file.write("\n\n")
        i_file.close()
    o_file.close()


# takes in a directory of files as input and compiles all text files in the directory into two text files,
# one containing a training set and the other a testing set
def compile_train_and_test_text(source_dir, train_filename, test_filename, threshold=.95):
    train_file = open(train_filename, 'w')
    test_file = open(test_filename, 'w')
    filenames = os.listdir(source_dir)

    for filename in filenames:
        file = os.path.join(source_dir, filename)
        i_file = open(file, 'r')
        text = i_file.read()
        sentences = text.split('\n')

        train_text = '\n'.join(sentences[:int(threshold * len(sentences))])
        test_text = '\n'.join(sentences[int(threshold * len(sentences)):])
        train_text = re.sub('(\n)+', '\n', train_text)
        test_text = re.sub('(\n)+', '\n', test_text)

        train_file.write(train_text)
        train_file.write("\n\n")
        test_file.write(test_text)
        test_file.write("\n\n")
        i_file.close()

    train_file.close()
    test_file.close()


def main():
    clean_files("raw_data/source_texts", "raw_data/processed_texts")
    compile_train_and_test_text("raw_data/processed_texts", "processed_data/train.txt", "processed_data/test.txt")
    clean_sentences("processed_data/test.txt")
    clean_sentences("processed_data/train.txt")


if __name__ == "__main__":
    main()
