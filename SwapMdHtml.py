import yaml
import markdown as md #for writing an md file as an html file
from datetime import datetime
import os
from pathlib import Path

class SwapMdHtml():
    def __init__(self, md_entry:os.DirEntry, root_dir):
        self.root_dir = root_dir
        self.file_entry = md_entry
        self.parse_data(self.get_md_data(md_entry))

    def parse_data(self, data:dict):#add some ifs...?
        self.title = data['title']
        self.date = data['date']
        self.categories = data['categories']
        self.word_count = data['word_count']
        self.keywords = data['key-words']
        self.file_name = data['file_name']
        self.file_path = data['file_path']



    def get_md_data(self, file):
        """Takes a file and returns relevant data as dictionary"""
        data = {
            'title': "", 
            'date': "", 
            'categories': "", 
            'word_count': "", 
            'key-words': "", 
            'file_name': "", 
            'file_path': ""}
        
        block = self.get_yaml_block(file)
        if block:
            yaml_data = yaml.safe_load(block)
            data.update(yaml_data)


        if not data['title']:
            data['title'] = self.find_title(file)

        if not data['date']:
            stat = os.stat(file).st_mtime
            data['date'] = datetime.fromtimestamp(stat).date()

        if not data['categories']:
            data['categories'] = [self.get_categories(file)]

        if not data['word_count']:
            data['word_count'] = self.get_word_count(file)

        if not data['key-words']:
            data['key-words'] = self.get_keywords(file)

        if not data['file_name']:
            data['file_name'] = self.file_entry.name

        if not data['file_path']:
            data['file_path'] = self.file_entry.path
        
        return data

    
    def find_title(self, file):
        title = ""
        with open(file, "r", encoding='utf-8') as f:
            while not title:
                line = f.readline()
                if line == "":
                    return file.name# There's no header
                
                line_words = line.split()
                
                if line_words and line_words[0] in \
                ["#", "##", "###", "####", "#####"]:
                    title = " ".join(line_words[1:]).strip()
        return title


    def get_categories(self, file):
        entrypath = os.path.dirname(file.path)
        parent_dir_name = os.path.basename(entrypath)
        return parent_dir_name


    def get_word_count(self, file):
        with open(file, "r", encoding="utf-8") as f:
            count = 0
            for line in f.readlines():
                count += len(line.split())
        return count


    def get_keywords(self, file):
        NOT_KEY_WORDS = [
            'a', 'about', 'and', 'as', 'at', 'but', 'by', 'down', 
            'for', 'from', 'if', 'in', 'into', 'like', 'near', 
            'nor', 'of', 'off', 'on', 'once', 'onto', 'or', 'over', 
            'past', 'so', 'than', 'that', 'the', 'to', 'upon', 
            'when', 'with', 'yet', 'what', 'can', 'have', 'has']
        keywords = []

        with open(file, "r", encoding="utf-8") as f:
            for line in f.readlines():
                line_words = line.split()
                if line_words and line_words[0] in \
                ["#", "##", "###", "####", "#####"]:
                    for word in line_words[1:]:
                        keywords.append(word.lower())

        for word in keywords:
            if word.lower() in NOT_KEY_WORDS:
                keywords.remove(word)
            elif len(str(word)) < 3:
                keywords.remove(word)

        keywords = list(dict.fromkeys(keywords)) #remove duplicates

        return keywords[:6]


    def get_yaml_block(self, file):
        with open(file, "r", encoding="utf-8") as f:
            yaml_block = []
            block_found = False
            for line in f.readlines():
                if line == "": #end of document
                    return False
                elif "]$" in line.split():
                    block_found = False

                if block_found:
                    yaml_block.append(line)
                elif "*$[ article*" in line.strip():# only accepts article blocks
                    block_found = True
                    

            return "".join(yaml_block)


    def to_html_str(self, root_folder):
        self.html_path = self.make_html_file()
        self.rel_html_path = self.html_path.relative_to(root_folder).as_posix()

        new_str = f"""
            <div style="font-weight: bold; font-size: 120%; padding-bottom: 5px;">
                <a href="{self.rel_html_path}">{self.html_path.name}</a>
            </div>
            <br>
            Date: {self.date}
            <br>
            Categories: {self.categories}
            <br>
            {self.word_count} words
            <br>
            Keywords: {self.keywords}
            <br>
            {self.file_name}
            <br>
            <br>
            """
        return new_str


    def trim_blocks(self, file):
        """takes a .md file and returns the text contents without yaml
        blocks"""
        lines = file.readlines()


        in_block = False
        bad_line_idxs = []
        for i in range(len(lines)):
            if in_block:
                if "]$" in lines[i].split():
                    in_block = False
                bad_line_idxs.append(i)
            else:
                if "$[" in lines[i].split():
                    in_block = True
                    bad_line_idxs.append(i)
            
        for i in reversed(bad_line_idxs):
            lines.pop(i)


        return "".join(lines)
        

    def make_html_file(self):
        """Takes an os.DirEntry as a .md file, and
        writes a .html file copy in the same folder"""

        md_path = Path(self.file_entry.path)
        html_path = md_path.with_suffix(".html")


        with open(self.file_entry, "r", encoding='utf-8') as f:
            text = self.trim_blocks(f)

        with open(html_path, "w", encoding='utf-8') as f:
            f.write(md.markdown(text))

        return html_path
    