import sys
import os
import SwapMdHtml as swap


def scan_dir_recursive(dir, deapth=0):
    """takes a directory and recursively scans it, returning at each
    level a list with idx 0 = the current directory, and idx 1 = a
    list of what's inside (including data from .md files)"""
    
    dTab = "\t"*deapth
    dir_name = os.path.basename(dir)
    
    folder_data = [dir_name]
    files_data = []
    for entry in os.scandir(dir):
        if entry.is_dir():
            #print(f"{dTab}DIRECTORY: {entry}")
            folder_data.append(scan_dir_recursive(entry, deapth=deapth+1))

        elif entry.name.endswith(".md"):
            #print(f"{dTab}MARKDOWN: {entry.name}")
            file_swapper = swap.SwapMdHtml(entry, dir)
            files_data.append(file_swapper)

        else:
            #print(f"{dTab}NEITHER D/M: {entry.name}")
            pass

    folder_data.insert(1, files_data)
    return folder_data


def body_html_recursive(dataset, root):
    """takes a dataset from scan_dir_recursive, and recursively
    extracts data and builds the contents of the <body> section
    of an html index"""

    inside = ""
    
    for e in dataset:
        tp = type(e)
        if tp == str:
            inside = inside + header(e)
        if tp == swap.SwapMdHtml:
            inside = inside + e.to_html_str(root)
        elif tp == list:
            inner = body_html_recursive(e, root)
            if inner:
                inside = inside + inner
    return inside

def header(folder_name):
    """Takes a folder name and returns it as an html header"""
    return f"<h2>{folder_name}</h2>"

def create_index(dir_dataset, root_folder):
    """takes a dataset from scan_dir_recursive and the root folder, 
    and builds the html for a directory index in the root."""

    return f"""
    <html>
        <head>
            <meta charset="utf-8">
        </head>
        <body>
            {body_html_recursive(dir_dataset, root_folder)}
        </body>
    </html>
    """
    


def main(root_folder):
    """takes a root folder as a path, creates .html versions of
    internal .md files, and makes a .html index in the root."""

    all_the_data = scan_dir_recursive(root_folder)

    html = create_index(all_the_data, root_folder)

    index_path = os.path.join(root_folder, "index.html")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)






if __name__ == "__main__":
    main(sys.argv[1])
    