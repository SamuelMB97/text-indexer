import yaml
from datetime import datetime
import os


class Presentable_md():
    def __init__(self, md_file):
        self.parse_data(self.get_md_data(md_file))


    def parse_data(self, data:dict):#add some ifs...?
        self.title = data['title']
        self.date = data['date']
        self.categories = data['categories']
        self.word_count = data['word_count']
        self.keywords = data['keywords']
        self.file_name = data['file_name']
        self.file_path = data['file_path']


    def get_md_data(self, file):
        """Takes a file and returns relevant data as dictionary"""
        block = self.get_yaml_block(file)
        data = dict()
        if block:
            data = yaml.safe_load(block)

        if not data['title']:
            data['title'] = self.find_title(file)
            print(data['title'])

        if not data['date']:
            stat = os.stat(file).st_mtime
            data['date'] = datetime.fromtimestamp(stat).date()
            print(data['date'])

        if not data['categories']:
            data['categories'] = [self.get_categories()]

        if not data['word_count']:
            data['word_count'] = self.get_word_count(file)

        if not data['keywords']:
            data['keywords'] = self.get_keywords(file)

        if not data['file_name']:
            pass# TODO
        if not data['file_path']:
            pass# TODO
        return data

    
    def find_title(self, file):
        title = ""
        with open(file, "r", encoding='utf-8') as f:
            while not title:                
                line_words = f.readline().split()
                if line_words and line_words in \
                ["#", "##", "###", "####", "#####"]:
                    title = " ".join(line_words[1:]).strip()
        return title


    def get_categories(self, file):
        entrypath = os.path.dirname(file.path)
        parent_dir_name = os.path.basename(entrypath)
        #print(f"parent_dir_name = {parent_dir_name}")
        return parent_dir_name


    def get_word_count(self, file):
        with open(file, "r", encoding="utf-8") as f:
            count = 0
            for line in f.readlines():
                count += len(line.split())
        print(f"count: {count}")
        return count


    def get_keywords(self, file):
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


    def get_yaml_block(self, file):
        with open(file, "r", encoding="utf-8") as f:
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

    def load_data_from_file(self, file):
        return -1
        self.set_title(file)
        self.title = data.title
        self.date = data.date
        self.categories = data.categories
        self.word_count = data.word_count
        self.keywords = data.keywords
        self.file_name = data.file_name
        self.file_path = data.file_path


    def to_html(self):
        new_str = f"""
            <div style="font-weight: bold; font-size: 120%; padding-bottom: 5px;">
                " FFFFFF "
                <a href="{self.file_path}">{self.file_name}</a>
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
            """
        return new_str