import sys
import os
import yaml
import markdown as md #for writing an md file as an html file
import Presentable_md as pmd

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


def get_md_data(f_md):# TODO delete outdated function
    """Takes a file and returns relevant data as dictionary"""
    block = get_yaml_block(f_md)
    if block:
        data = yaml.safe_load(block)
    else:
        data = load_data_from_file(f_md)
    return data


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
            themd = pmd.Presentable_md(entry)
            
            #print(themd.to_html())

            files_data.append(pmd.Presentable_md(entry))
        else:
            print(f"{dTab}NEITHER D/M: {entry.name}")

    folder_data.append(files_data)
    return folder_data


def main(argv):

    all_the_data = scan_dir_recursive(argv[1])

    """print("MADE IT THIS FAR... :)")
    assert 0"""
    """
    data = get_file_data(argv[1])
    print(f"DATA:\n{data}\nTHAT'S THE DATA")
    """

    """d=data
    html = html_str_for_md(d['title'], d['date'], d['categories'], "999", d['key-words'], "NameOfFile.md", argv, )
    print(f"HTML:\n{html}\nTHAT'S THE HTML")
    """


# headers above md files come from dir names they're in...
# but I think each header is only there once






if __name__ == "__main__":
    main(sys.argv)