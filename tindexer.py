import sys
import os
import PyYAML as pyy
import Markdown as md


def main(argv):
    pass

# headers above md files come from dir names they're in... but I think each header is only there once
def html_str_for_md(title, date, categories, word_count, keywords, file_name, file_path): #not sure FFFFFF is correct
    new_str = f"""
        <div style="font-weight: bold; font-size: 120%; padding-bottom: 5px;">
            " FFFFFF "
            <a href="{file_path}">{file_name}</a>
        <br>
        Date: {date}
        <br>
        Categories: {categories}
        <br>
        {word_count} words
        <br>
        Keywords: {keywords}
        <br>
        {file_name}
        <br>
        """
    return new_str





if __name__ == "__main__":
    main(sys.argv)