import sys
import os
import SwapMdHtml as swap



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

        elif entry.name.endswith(".md"):
            print(f"{dTab}MARKDOWN: {entry.name}")
            file_swapper = swap.SwapMdHtml(entry, dir)
            print(file_swapper.to_html_str())


            files_data.append(file_swapper)

        else:
            print(f"{dTab}NEITHER D/M: {entry.name}")

    folder_data.append(files_data)
    return folder_data


def create_html(entry, dir):
    pass


def create_index(dir_dataset, root_folder):
    pass


def main(root_folder):
    all_the_data = scan_dir_recursive(root_folder)
    """print("\n" * 3)
    for row in all_the_data:
        print(f"NEXT: {row}")"""
    create_index(all_the_data, root_folder)

    """
    print("MADE IT THIS FAR... :)")
    assert 0#"""


# headers above md files come from dir names they're in...
# but I think each header is only there once






if __name__ == "__main__":
    main(sys.argv[1])
    