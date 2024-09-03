import pymupdf as fitz
import sys
import os
import glob

# pdf_path: the folder of all the PDF files
# saved_path: the path of the saved page images
def convert_pdf_to_image(pdf_path, pdf_file, saved_path):

    if not os.path.exists(saved_path):
        os.mkdir(saved_path)
    else:
        files = glob.glob('saved_path/*')
        for f in files:
            os.remove(f)

    try:
        fitz.TOOLS.mupdf_warnings()  # empty the problem message container
        doc = fitz.open(pdf_path + "/" + pdf_file)
        warnings = fitz.TOOLS.mupdf_warnings()
        if warnings:
            print(warnings)
            raise RuntimeError()

        for page in doc:  # iterate through the pages
            pix = page.get_pixmap()  # render page to an image
            pix.save(saved_path + "/" + f"{pdf_file[:-4]}-{page.number}.png")  # store image as a PNG
        return

    except:
        print("error when opening the pdf file {}".format(pdf_file))
        return None
    