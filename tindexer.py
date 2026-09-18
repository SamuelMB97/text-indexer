import sys
import os
import SwapMdHtml as swap

# TODO pretty much everything is working except the links to
# the new html files :P

def scan_dir_recursive(dir, deapth=0):
    """takes a directory and recursively scans it, returning at each
    level a list with idx 0 = the current directory, and idx 1 = a
    list of what's inside (including data from .md files)"""
    if deapth > 10:
        print("too deeeeeep.")
        return -1
    
    dTab = "\t"*deapth
    dir_name = os.path.basename(dir)
    
    folder_data = [dir_name]
    files_data = []
    for entry in os.scandir(dir):
        if entry.is_dir():
            print(f"{dTab}DIRECTORY: {entry}")
            folder_data.append(scan_dir_recursive(entry, deapth=deapth+1))

        elif entry.name.endswith(".md"):
            print(f"{dTab}MARKDOWN: {entry.name}")
            file_swapper = swap.SwapMdHtml(entry, dir)
            #print(file_swapper.to_html_str())
            files_data.append(file_swapper)

        else:
            print(f"{dTab}NEITHER D/M: {entry.name}")

    folder_data.insert(1, files_data)
    return folder_data


def create_html(entry, dir):
    pass


def body_html_recursive(dataset, root, deapth=0):
    inside = ""
    dTab = "\t" * deapth
    
    for e in dataset:
        tp = type(e)
        print(f"{dTab}{tp}")
        if tp == str:
            inside = inside + header(e)
        if tp == swap.SwapMdHtml:
            inside = inside + e.to_html_str(root)
        elif tp == list:
            inner = body_html_recursive(e, root, deapth=deapth+1)
            if inner:
                inside = inside + inner
    return inside

def header(folder_name):
    return f"<h2>{folder_name}</h2>"

def create_index(dir_dataset, root_folder):
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
    all_the_data = scan_dir_recursive(root_folder)
    print(all_the_data)
    """print("\n" * 3)
    for row in all_the_data:
        print(f"NEXT: {row}")"""

    print(f"\n\nCREATING HTML:")
    html = create_index(all_the_data, root_folder)
    print(f"\n\n FINAL HTML:\n{html}")

    index_path = os.path.join(root_folder, "index.html")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    """
    print("MADE IT THIS FAR... :)")
    assert 0#"""


# headers above md files come from dir names they're in...
# but I think each header is only there once






if __name__ == "__main__":
    main(sys.argv[1])
    