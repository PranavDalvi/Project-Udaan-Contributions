'''
Integrating git clone for word count of OCR Repos
To Run python git-test.py -g git-repo-url
Author: Pranav Dalvi
'''
import git
import os
import argparse
from bs4 import BeautifulSoup
import re

def extract_repo_name(link):
    # Use a regular expression to extract the repository name
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

            # Combine text from both types of tags, ensuring uniqueness
            for tag in span_tags + p_tags:
                unique_text_set.add(tag.get_text())

    # Calculate word count for unique text
    for text in unique_text_set:
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        total_word_count += word_count

    return total_word_count

def main():
    parser = argparse.ArgumentParser(description='Calculate total word count for HTML files in a directory.')
    parser.add_argument('-g', '--github_repo_link', type=str, required=True, help='Path to the directory containing HTML files.')


    args = parser.parse_args()

    src_url = args.github_repo_link
    clone_link = src_url[src_url.index("github"):]
    gh_token = ""
    repo_url = f"https://{gh_token}@{clone_link}"
    repo_name = extract_repo_name(src_url)

    # make a folder named gh_clone if it doesn't exist
    gh_clone_folder = "gh_clone"
    os.makedirs(gh_clone_folder, exist_ok=True)

    repo_path = os.path.join(gh_clone_folder, repo_name)
    repo = git.Repo.clone_from(repo_url, repo_path)

    print(f"Repository cloned to: {repo.working_dir}")

    Input_folder_path = os.path.join(gh_clone_folder,repo_name, "CorrectorOutput")
    total_word_count = calculate_total_word_count(Input_folder_path)

    # Print or use the total word count
    print(f'Total word count for all HTML files in the directory: {total_word_count}')

    # Write the total word count to a text file
    output_file_path = os.path.join(gh_clone_folder,repo_name, "word-count.txt")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"Total word count: {total_word_count}")

    print(f'Total word count written to {output_file_path}.')

if __name__ == "__main__":
    main()
