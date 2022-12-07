
import os
import bs4
from bs4 import BeautifulSoup
from parse_content import ContentParser


class Chapter(object):

    def __init__(self, html_file):
        # print(" + Init Chapter from html {}".format(html_file))
        self.chapter_name = os.path.basename(html_file)
        html = open(html_file, 'rb').read()
        bs = BeautifulSoup(html, features='html.parser')
        html_dir = os.path.basename(html_file)

        self.content = ContentParser(os.path.dirname(html_file))
        self.content.parse(bs.body)
        # print(" + Found {} contents.".format(len(self.content.contents)))

    def write_txt(self, fout):
        # first, set label with html file name
        fout.write("---------------[Label: {}]--------------\n".format(self.chapter_name))
        self.content.write_txt(fout)

    def write_pdf(self, pdf_writer):
        pdf_writer.write_new_page()
        pdf_writer.write_label(self.chapter_name)
        self.content.write_pdf(pdf_writer)

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
            if href and href.endswith('html') or href.endswith("htm"):
                chapter_files.append(os.path.join(opf_dir, href))
        print(" + Found {} chapter html files.".format(len(chapter_files)))

        # Init Chapter one by one
        self.chapters = []
        for chapter_file in chapter_files:
            self.chapters.append(Chapter(chapter_file))

        # outline guides
        self.guides = []
        for guide in bs.package.guide.findAll('reference'):
            href = guide['href']
            title = guide['title']
            self.guides.append([title, href])
        print(" + Found {} guide references.".format(len(self.guides)))

    def write_txt(self, fout):
        for chapter in self.chapters:
            chapter.write_txt(fout)

    def write_pdf(self, pdf_writer):
        pdf_writer.set_guides(self.guides)
        for chapter in self.chapters:
            chapter.write_pdf(pdf_writer)

if __name__ == "__main__":
    c = Chapter("chapter2.html")
    fout = open("tmp.txt", 'w')
    c.write_txt(fout)
    fout.close()