import os
import sys
import zipfile
import traceback
import shutil
from book import Book


def find_opf(tmp_dir):
    for root, _, files in os.walk(tmp_dir):
        for f in files:
            if f.endswith(".opf"):
                return os.path.join(root, f)
    return None


def process_epub(epub_path):
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
        fout = open("{}.txt".format(base_name), 'w')
        b.write_txt(fout)
        fout.close()

    except Exception as e:
        traceback.print_exc(limit=100)

    finally:
        pass
        #if os.path.isdir(tmp_dir):
        #    shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    process_epub(sys.argv[1])