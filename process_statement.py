import logging
import sys

import pdftotext


class ProcessStatement:

    """This class contains all the processing functions for one PDF statement (specific to one particular bank)"""

    def __init__(self, pdfpath):
        logging.debug('Inside Process Statement')
        self.pdfpath = pdfpath
        self.pages = {}

    def read_pdf_file(self):
        try:
            with open(self.pdfpath, 'rb') as f:
                pdf = pdftotext.PDF(f)
        except FileNotFoundError as fe:
            print('File not found with path: ' + self.pdfpath)
            sys.exit(0)
        except Exception as e:
            print('Unexpected error occured!')
            print(e)
            sys.exit(0)
        for pagenum in range(len(pdf)):
            self.pages[pagenum + 1] = pdf[pagenum]

    def print_pdf_page(self, pagenum):
        print(self.pages[pagenum])

    def get_page_numbers(self):
        for pagenum in sorted(self.pages.keys()):
            print('Page {}/{}'.format(pagenum, len(self.pages.keys())))