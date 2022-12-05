
import os
import bs4
from bs4 import BeautifulSoup

class Paragraph(object):
    def __init__(self) -> None:
        self.texts = []

class Chapter(object):

    def __init__(self, html_file):
        print(" + Init Chapter from html {}".format(html_file))
        html = open(html_file, 'rb').read()
        bs = BeautifulSoup(html, features='html.parser')
        html_dir = os.path.basename(html_file)

        self.contents = []
        for item in bs.body.div:
            if isinstance(item, bs4.element.Tag):

                if item.name == 'img':
                    img_path = os.path.join(html_dir, item['src'])
                    self.contents.append(['img', img_path])

                elif item.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    assert len(item.contents) == 1
                    self.contents.append([item.name, item.contents[0]])

                elif item.name == 'p':
                    ps = []
                    for sub in item.contents:
                        if isinstance(sub, bs4.element.Tag):
                            if sub.name == "a":
                                assert len(sub.contents) == 1
                                ps.append(["a", sub.contents[0], sub['href']])
                        elif isinstance(sub, bs4.element.NavigableString):
                            ps.append(["text", sub])
                        else:
                            raise Exception("Unexcepted child tag for <p>: {}!".format(sub))
                    self.contents.append(["p", ps])

                else:
                    raise Exception("Unexcepted tag for chapter: {}!".format(item))

        print(" + Found {} contents.".format(len(self.contents)))

    def write_pdf(self):
        # first, set label with html file name
        pass


class Book(object):

    def __init__(self, opf_file):
        print(" + Init Book from opf {}".format(opf_file))

        xml = open(opf_file, 'rb').read()
        bs = BeautifulSoup(xml, features='xml')

        chapter_files = []
        opf_dir = os.path.dirname(opf_file)

        # find all chapter html files
        for item in bs.package.manifest.findAll('item'): 
            href = item['href']
            if href and href.endswith('html'):
                chapter_files.append(os.path.join(opf_dir, href))
        print(" + Found {} chapter html files.".format(len(chapter_files)))

        # Init Chapter one by one
        self.chapters = []
        for chapter_file in chapter_files:
            self.chapters.append(Chapter(chapter_file))

    def write_pdf(self):
        pass

if __name__ == "__main__":
    Chapter("chapter2.html")