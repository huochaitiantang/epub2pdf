import bs4
import os

DEFAULT_FONT = "default"
FONT_TAGS = [
    "p",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
]
BLOCK_TAGS = [
    "p",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
]


class ContentParser(object):
    def __init__(self, base_dir):
        self.stack_fonts = [DEFAULT_FONT]
        self.stack_hrefs = [None]
        self.contents = []
        self.base_dir = base_dir

    def parse(self, x):
        if isinstance(x, bs4.element.Tag):
            func_name = "parse_tag_{}".format(x.name)
            if hasattr(self, func_name):
                getattr(self, func_name)(x)
            else:
                self.parse_tag_common(x)
        elif isinstance(x, bs4.element.NavigableString):
            self.parse_string(x)
        else:
            raise Exception("Unexcepted tag type: {}!".format(x))

    def parse_string(self, x):
        if self.stack_fonts[-1] == DEFAULT_FONT and str(x).rstrip() == "":
            return
        if str(x) == "\n" and len(self.contents) > 0:
            last_content = self.contents[-1]
            if last_content['type'] == "text" and last_content['font'] == self.stack_fonts[-1]:
                last_content['value'] += "\n"
                return
        self.contents.append({
            "type": "text",
            "value": str(x),
            "font": self.stack_fonts[-1],
            "href": self.stack_hrefs[-1],
        })

    def parse_tag_common(self, x):
        if x.name in FONT_TAGS:
            self.stack_fonts.append(x.name)
        if x.contents:
            for y in x.contents:
                self.parse(y)
            if x.name in BLOCK_TAGS:
                self.parse_string("\n")
        if x.name in FONT_TAGS:
            self.stack_fonts.pop(-1)

    def parse_tag_a(self, x):
        self.stack_hrefs.append(x['href'])
        if x.contents:
            for y in x.contents:
                self.parse(y)
        self.stack_hrefs.pop(-1)

    def parse_tag_img(self, x):
        self.contents.append({
            "type": "img",
            "value": os.path.join(self.base_dir, x['src']),
        })

    def write_txt(self, fout):
        for c in self.contents:
            if c['type'] == "img":
                fout.write("IMG[{}]\n".format(c['value']))
            elif c['type'] == "text":
                href_s = "({})".format(c['href']) if c['href'] else ""
                s = "[{}]{}{}".format(c['font'], href_s, c['value'])
                s = s.encode('gbk', 'ignore').decode('gbk')
                # print(s)
                fout.write(s)
            else:
                raise Exception("Unexcepted content type: {}!".format(c['type']))

    def write_pdf(self, pdf_writer):
        for c in self.contents:
            pdf_writer.write(c)