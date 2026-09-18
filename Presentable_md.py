import yaml


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
        if not data['date']:
            pass# TODO
        if not data['categories']:
            pass# TODO
        if not data['word_count']:
            pass# TODO
        if not data['keywords']:
            pass# TODO
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