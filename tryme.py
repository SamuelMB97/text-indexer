import sys
import os
import yaml
import markdown as md
from datetime import datetime



def get_yaml_block(f_md):
    with open(f_md, "r", encoding="utf-8") as f:
        yaml_block = []
        block_found = False
        for line in f.readlines():
            if line == "": #end of document
                return False
            elif line[:2] == "$[":
                block_found = True
            elif line[-4:] == "]$\n":
                block_found = False

            elif block_found:
                yaml_block.append(line)
        return "".join(yaml_block)
        

def scan_dir_recursive(dir, deapth=0):
    """takes a directory and recursively scans it, returning at each
    level a list with idx 0 = the current directory, and idx 1 = a
    list of what's inside (including data from .md files)"""
    if deapth > 10:
        print("too deeeeeep.")
        return -1
    
    dTab = "\t"*deapth
    folder_data = [dir]
    files_data = []
    for entry in os.scandir(dir):
        if entry.is_dir():
            print(f"{dTab}DIRECTORY: {entry}")
            folder_data.append(scan_dir_recursive(entry, deapth=deapth+1))

        elif entry.name[-3:] == ".md":
            print(f"{dTab}MARKDOWN: {entry.name}")
            files_data.append(f"MD: {entry.name}")#get_md_data(entry))
        else:
            print(f"{dTab}NEITHER D/M: {entry.name}")

    folder_data.append(files_data)
    return folder_data


def find_title(file):
    title = ""
    with open(file, "r", encoding='utf-8') as f:
        while not title:                
            line_words = f.readline().split()
            if line_words and line_words[0] in \
            ["#", "##", "###", "####", "#####"]:
                title = " ".join(line_words[1:]).strip()
    return title


def get_categories(file):
    entrypath = os.path.dirname(file.path)
    parent_dir_name = os.path.basename(entrypath)
    #print(f"parent_dir_name = {parent_dir_name}")
    return parent_dir_name


def get_word_count(file):
    with open(file, "r", encoding="utf-8") as f:
        count = 0
        for line in f.readlines():
            count += len(line.split())
    print(f"count: {count}")
    return count


def get_keywords(file):
    NOT_KEY_WORDS = [
        'a', 'about', 'and', 'as', 'at', 'but', 'by', 'down', 
        'for', 'from', 'if', 'in', 'into', 'like', 'near', 
        'nor', 'of', 'off', 'on', 'once', 'onto', 'or', 'over', 
        'past', 'so', 'than', 'that', 'the', 'to', 'upon', 
        'when', 'with', 'yet']
    keywords = []

    with open(file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line_words = line.split()
            if line_words and line_words[0] in \
            ["#", "##", "###", "####", "#####"]:
                for word in line_words[1:]:
                    keywords.append(word.lower())

    #print(f"\npre-cut keywords: {keywords}")
    for word in keywords:
        #print(f"word: '{word}' ", end="")
        if word.lower() in NOT_KEY_WORDS:
            #print(f"not allowed. ")
            keywords.remove(word)
        elif len(str(word)) < 3:
            #print(f"too short. ")
            keywords.remove(word)

    #print()
    keywords = list(dict.fromkeys(keywords)) #remove duplicates

    return keywords[:6]






def main(file):

    entries = os.scandir(file)
    for e in entries:
        keywords = get_keywords(e)
        print(f"KEYWORDS:>{keywords}<THAT'S THE KEYWORDS")

        """word_count = get_word_count(e)
        print(f"WORD COUNT:>{word_count}<THAT'S THE WORD COUNT")"""


        """categories = get_categories(e)
        print(f"CATEGORIES:>{categories}<THAT'S THE CATEGORIES")"""


    """title = find_title(file)
    print(f"TITLE:>{title}<THAT'S THE TITLE")"""


    """the_data = scan_dir_recursive(file)
    print("\nSCAN COMPLETE\n")
    for line in the_data:
        print(line)"""

    """block = get_yaml_block(file)
    #print(f"BLOCK:\n{block}\nTHAT'S THE BLOCK")
    if block:
        data = yaml.safe_load(block)
        print(f"DATA:\n{data}\nTHAT'S THE DATA")
    else:
        pass# data = get_it_from_the_file(file)
    """


if __name__ == "__main__":
    main(sys.argv[1])