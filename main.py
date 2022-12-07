import os
import sys
import zipfile
import traceback
import shutil
from book import Book
from pdf_writer import PDFWriter


def find_opf(tmp_dir):
    for root, _, files in os.walk(tmp_dir):
        for f in files:
            if f.endswith(".opf"):
                return os.path.join(root, f)
    return None


def process_epub(epub_path, export_txt, export_pdf, font_name):
    print("Process epub file: {}...".format(epub_path))
    base_name = os.path.splitext(os.path.basename(epub_path))[0]
    tmp_dir = "tmp_" + base_name
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    try:
        # extract files as zip file
        extracts = zipfile.ZipFile(epub_path)
        extracts.extractall(tmp_dir)
        extracts.close()

        # find opf file
        opf_file = find_opf(tmp_dir)
        if not opf_file:
            raise Exception("Can not find opf file for {}!".format(epub_path))

        b = Book(opf_file)
        if len(b.chapters) <= 0:
            raise Exception("Can not find chapters for {}!".format(epub_path))

        if export_txt:
            txt_path = os.path.join(os.path.dirname(epub_path), "{}.txt".format(base_name))
            fout = open(txt_path, 'w')
            b.write_txt(fout)
            fout.close()
            print("Writen to {}.".format(txt_path))

        if export_pdf:
            pdf_path = os.path.join(os.path.dirname(epub_path), "{}.pdf".format(base_name))
            pdf_writer = PDFWriter(font_name=font_name)
            b.write_pdf(pdf_writer)
            pdf_writer.export_pdf(pdf_path)
            print("Writen to {}.".format(pdf_path))

    except Exception as e:
        traceback.print_exc(limit=100)

    finally:
        if os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir)


def process(path, export_txt, export_pdf, font_name):
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".epub"):
                    process_epub(os.path.join(root, f), export_txt, export_pdf, font_name)
    elif os.path.isfile(path):
        process_epub(path, export_txt, export_pdf, font_name)
    else:
        raise Exception("File or directory {} not existed!".format(path))


if __name__ == "__main__":
    process(
        sys.argv[1],
        export_txt=False,
        export_pdf=True,
        font_name='SimSun'
    )