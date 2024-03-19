'''
Author: Ajay Ravindran
Editor: Pranav Dalvi
'''

import os
from bs4 import BeautifulSoup
from glob import glob
from indicnlp.tokenize import sentence_tokenize
import csv
from tqdm import tqdm

def main(repo_name):
    # repo_name = "2000_JUNE"
    repo_lang = "sa" # "hi" for Hindi, "sa" for sanskrit
    repo_link = "https://github.com/UdaanContentForLogging/" + repo_name

    clone_link = repo_link[repo_link.index("github"):]+".git"
    # # os.system("git clone https://Ajay-Ravindran:@" + clone_link)
    os.system("git clone https://PranavDalvi:GPGKEY@" + clone_link)

    all_sents = []
    prev_page_para = ""
    for file_name in sorted(glob(f"/home/output_books/{repo_name}/Inds/*.txt")):
        with open(file_name, "r") as txt_file:
            lines = txt_file.readlines()

        lines_filtered = list(filter(lambda line: line.strip() != "", lines))

        if lines_filtered == []:
            if prev_page_para.strip() != "":
                sents = sentence_tokenize.sentence_split(prev_page_para.strip(), lang=repo_lang)
                for sent in sents:
                    all_sents.append([sent])
            prev_page_para = ""
            continue

        while lines[0].strip() == "":
            lines = lines[1:]
        while lines[len(lines) - 1].strip() == "":
            lines = lines[:-1]

        cur_para = prev_page_para
        for i in range(len(lines)):
            if lines[i].strip() != "":
                cur_para = cur_para + " " + lines[i].strip()
            else:
                if cur_para.strip() != "":
                    sents = sentence_tokenize.sentence_split(cur_para.strip(), lang=repo_lang)
                    for sent in sents:
                        all_sents.append([sent])
                cur_para = ""
        if cur_para.strip() != "":
            prev_page_para = cur_para.strip()
        else:
            prev_page_para = ""

    if prev_page_para != "":
        sents = sentence_tokenize.sentence_split(prev_page_para.strip(), lang=repo_lang)
        for sent in sents:
            all_sents.append([sent])

    # Save the combined text file
    combined_text_filename = f"{repo_name}.txt"
    with open(combined_text_filename, 'w', encoding='utf-8') as combined_text_file:
        combined_text_file.write('\n'.join([' '.join(sent) for sent in all_sents]))

    # Save the combined sentences to a CSV file
    csv_filename = f"{repo_name}.csv"
    fields = ['Sentences']
    with open(csv_filename, 'w', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(all_sents)

    print(f"Combined text saved to {combined_text_filename}")
    print(f"Sentences saved to {csv_filename}")


if __name__ == "__main__":
    repo_names = ["Repo list"]
    for repo_name in repo_names:
        main(repo_name)
