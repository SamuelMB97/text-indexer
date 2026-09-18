import yaml
import markdown as md #for writing an md file as an html file
from datetime import datetime
import os

# TODO set links as relative instead of absolute
class SwapMdHtml():
    def __init__(self, md_entry:os.DirEntry, parent_dir):
        #print(f">>INITIALIZING Presentable_md with entry: {md_entry.name}")
        self.parent = parent_dir
        self.file_entry = md_entry
        self.html = self.make_html_file(
            self.file_entry, self.parent
            )
        self.html_name = self.html[0]
        self.html_path = self.html[1]
        self.parse_data(self.get_md_data(md_entry))

    def parse_data(self, data:dict):#add some ifs...?
        #print(f">>PARSING .md data from {type(data)}")
        self.title = data['title']
        self.date = data['date']
        self.categories = data['categories']
        self.word_count = data['word_count']
        self.keywords = data['key-words']
        self.file_name = data['file_name']
        self.file_path = data['file_path']



    def get_md_data(self, file):
        """Takes a file and returns relevant data as dictionary"""
        #print(f">>GETTING .md data from {file.name}")
        data = {
            'title': "", 
            'date': "", 
            'categories': "", 
            'word_count': "", 
            'key-words': "", 
            'file_name': "", 
            'file_path': ""}
        
        #print(f"data set empty: {data}")
        block = self.get_yaml_block(file)
        #print(f"YAML BLOCK:\n{block}\nTHAT'S THE BLOCK, type: {type(block)}, length: {len(block)}, truthy: {bool(block)}")
        if block:
            yaml_data = yaml.safe_load(block)
            #print(f"yaml_data: {yaml_data}")
            data.update(yaml_data)
        #print(f"data set after yaml: {data}")


        if not data['title']:
            data['title'] = self.find_title(file)
            #print(f"Title in data: {data['title']}")

        if not data['date']:
            stat = os.stat(file).st_mtime
            data['date'] = datetime.fromtimestamp(stat).date()
            #print(f"date in data: {data['date']}")

        if not data['categories']:
            data['categories'] = [self.get_categories(file)]
            #print(f"categories in data: {data['categories']}")

        if not data['word_count']:
            data['word_count'] = self.get_word_count(file)
            #print(f"word count in data: {data['word_count']}")

        if not data['key-words']:
            data['key-words'] = self.get_keywords(file)
            #print(f"keywords in data: {data['key-words']}")

        if not data['file_name']:
            data['file_name'] = self.file_entry.name
            #print(f"file_name from entry: {data['file_name']}")

        if not data['file_path']: #TODO file path should go to the html file
            data['file_path'] = self.file_entry.path
            #print(f"file_path from entry: {data['file_path']}")
        
        #print(f"data set after scrape: {data}")
        return data

    
    def find_title(self, file):
        #print(f"file type: {type(file)}, file name: {file.name}")
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
        #print(f"parent_dir_name = {parent_dir_name}")
        return parent_dir_name


    def get_word_count(self, file):
        with open(file, "r", encoding="utf-8") as f:
            count = 0
            for line in f.readlines():
                count += len(line.split())
        #print(f"count: {count}")
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
        #print(f">>GETTING YAML BLOCK from {file}")
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
                #elif "$[" in line.split():# accepts the first block it finds
                elif "*$[ article*" in line.strip():# only accepts article blocks
                    block_found = True
                    

            return "".join(yaml_block)


    def to_html_str(self):
        new_str = f"""
            <div style="font-weight: bold; font-size: 120%; padding-bottom: 5px;">
                <a href="{self.html_path}">{self.html_name}</a>
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
        

    def make_html_file(self, entry, folder):
        """Takes an os.DirEntry as a .md file and it's parent folder and
        writes a .html file copy in the same folder"""
        #print(folder)
        #print(entry.name)
        out_file_name = entry.name[:-2] + "html"
        #print(out_file_name)
        out_file_path = os.path.join(folder, out_file_name)
        #print(f"path: {out_file_path}")

        with open(entry, "r", encoding='utf-8') as f:
            text = self.trim_blocks(f)

        """ # TODO this part must be un-commented to make the html files
        with open(out_file_path, "w", encoding='utf-8') as f:
            f.write(md.markdown(text))#"""

        return (out_file_name, out_file_path)
    