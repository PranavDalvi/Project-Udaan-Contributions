from pdf2docx import Converter
import sys
import os

def main(pdf_path):
    filename = os.path.basename(pdf_path)
    print(filename)
    cv = Converter(pdf_path)
    cv.convert(f"./{filename}.docx", start=0, end=None)
    cv.close()

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    main(pdf_path)
