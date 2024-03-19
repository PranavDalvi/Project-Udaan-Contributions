'''
Integrating pandas + git clone for word count of OCR Repos
To Run python git-test.py -f CSV files which contains git repo links
Author: Pranav Dalvi
'''

import pandas as pd
import git
import os
from bs4 import BeautifulSoup
import re
import argparse

def extract_repo_name(link):
    # extract the repository name
    match = re.search(r'/([^/]+)$', link)
    if match:
        return match.group(1)
    else:
        return None

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

            for tag in span_tags + p_tags:
                unique_text_set.add(tag.get_text())

    for text in unique_text_set:
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        total_word_count += word_count

    return total_word_count

def main():
    parser = argparse.ArgumentParser(description='Calculate total word count for HTML files in a directory.')
    parser.add_argument('-f', '--csv_file_path', type=str, required=True, help='Path to the CSV file containing GitHub links.')

    args = parser.parse_args()

    df = pd.read_csv(args.csv_file_path)

    # Iterate over the GitHub links in column 'GitHub Link'
    for index, row in df.iterrows():
        github_link = row['Github Link'].strip()

        # Execute the code for each link
        src_url = github_link
        clone_link = src_url[src_url.index("github"):]
        gh_token = ""
        repo_url = f"https://{gh_token}@{clone_link}"
        repo_name = extract_repo_name(src_url)

        gh_clone_folder = "gh_clone"
        os.makedirs(gh_clone_folder, exist_ok=True)

        repo_path = os.path.join(gh_clone_folder, repo_name)

        repo = git.Repo.clone_from(repo_url, repo_path)
        print(f"Repository cloned to: {repo.working_dir}")

        input_folder_path = os.path.join(gh_clone_folder, repo_name, "CorrectorOutput")
        total_word_count = calculate_total_word_count(input_folder_path)

        df.at[index, 'Word Count'] = total_word_count

        # os.remove(repo_path)

    df.to_csv(args.csv_file_path, index=False)

if __name__ == "__main__":
    main()
