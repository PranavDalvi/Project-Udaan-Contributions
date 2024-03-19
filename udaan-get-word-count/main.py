
'''
To run: python main.py 
Options: 

-d OCRed_Book_Folder (corrector output)
-x csv files
-l latex files using detex CLI package

Author: Pranav Dalvi
'''

import os
import argparse
from bs4 import BeautifulSoup
import re
import csv
import subprocess
import argparse


# For OCR Word Count (.html from correctorOutput)

def calculate_total_word_count(input_folder_path):
    total_word_count = 0
    unique_text_set = set()

    for filename in os.listdir(input_folder_path):
        if filename.endswith(".html"):
            file_path = os.path.join(input_folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all <span> and <p> tags on the page
            span_tags = soup.find_all('span')
            p_tags = soup.find_all('p')

            # Combine text from both types of tags, ensuring uniqueness
            for tag in span_tags + p_tags:
                unique_text_set.add(tag.get_text())

    # Calculate word count for unique text
    for text in unique_text_set:
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        total_word_count += word_count

    return total_word_count

def remove_latex_format(file_path):
    try:
        detex_output = subprocess.check_output(['detex', file_path], universal_newlines=True)
        return detex_output
    except subprocess.CalledProcessError:
        print(f'Error running detex for file: {file_path}')
        return ''

def get_word_count_from_latex_file(file_path):
    detex_output = remove_latex_format(file_path)
    words = detex_output.split()
    word_count = len(words)
    return word_count

def get_total_word_count_from_directory(directory_path):
    total_word_count = 0
    file_word_counts = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".tex"):
            file_path = os.path.join(directory_path, filename)
            file_word_count = get_word_count_from_latex_file(file_path)
            total_word_count += file_word_count
            file_word_counts.append((filename, file_word_count))

    # Write word counts to a text file
    output_file_path = os.path.join(directory_path, 'wordcount.txt')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f'Total word count across all LaTeX files: {total_word_count}\n\n')
        for filename, count in file_word_counts:
            output_file.write(f'Total word count in {filename}: {count}\n')
            
    print(f'Total word count in {filename}: {count}\n')
    print(f'Word counts written to {output_file_path}')

# For CSV Word Count
def get_word_count_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Read all rows and columns, and concatenate the values
        all_text = ' '.join([' '.join(row) for row in csv_reader])

        # Split the text into words
        words = all_text.split()

        # Count the words
        word_count = len(words)

    return word_count

def get_word_counts_from_csv_directory(directory_path):
    # Get a sorted list of CSV files in the directory
    csv_files = sorted([filename for filename in os.listdir(directory_path) if filename.endswith(".csv")])

    # Initialize a dictionary to store word counts for each CSV file
    file_word_counts = {}

    # Loop through all sorted files in the directory
    for filename in csv_files:
        file_path = os.path.join(directory_path, filename)

        # Get word count for the current CSV file
        file_word_count = get_word_count_from_csv(file_path)

        # Store word count for the current file
        file_word_counts[filename] = file_word_count

        # Print word count for each file
        print(f'Total word count in {filename}: {file_word_count}')

    # Write word counts to a text file
    output_file_path = os.path.join(directory_path, 'wordcount.txt')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for filename, count in file_word_counts.items():
            output_file.write(f'\nTotal word count in {filename}: {count}\n')

    print(f'Word counts written to {output_file_path}')

def main():
    parser = argparse.ArgumentParser(description='Calculate total word count for HTML files in a directory.')
    parser.add_argument('-d', '--ocr_directory_path',default=None, type=str, help='Path to the directory containing HTML files.')
    parser.add_argument('-x', '--csv_directory_path',default=None, type=str, help='Path to the csv file.')

    args = parser.parse_args()
    
    if (args.ocr_directory_path != None and args.csv_directory_path == None):
        input_folder_path = os.path.join(args.ocr_directory_path, "CorrectorOutput")
        total_word_count = calculate_total_word_count(input_folder_path)

        print(f'\nTotal word count for all HTML files in the directory: {total_word_count}\n')

        # Write the total word count to a text file
        output_file_path = os.path.join(args.ocr_directory_path, "word-count.txt")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(f"Total word count: {total_word_count}")

        print(f'Total word count written to {args.ocr_directory_path}word-count.txt')

    elif(args.ocr_directory_path == None and args.csv_directory_path != None):
        get_word_counts_from_csv_directory(args.csv_directory_path)
    else:
        print("usage: main.py [-h] -d ocr_directory_path -x csv_directory_path")
    

if __name__ == "__main__":
    main()
