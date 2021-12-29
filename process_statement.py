import logging
import sys

import pdftotext


class ProcessStatement:

    """This class contains all the processing functions for one PDF statement (specific to one particular bank)"""

    def __init__(self, pdfpath, **kwargs):
        self.pdfpath = pdfpath
        self.pages = {}
        self.pdf_raw_output = kwargs.get('raw', False)
        self.pdf_phy_output = kwargs.get('physical', False)

    def read_pdf_file(self):
        try:
            with open(self.pdfpath, 'rb') as f:
                pdf = pdftotext.PDF(f, raw=self.pdf_raw_output, physical=self.pdf_phy_output)
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

    def pretty_print_page(self, pagenum):
        for line in self.pages[pagenum].split('\n'):
            print(line)

    def get_page_numbers(self):
        return list(sorted(self.pages.keys()))

    def print_page_numbers(self):
        for pagenum in sorted(self.pages.keys()):
            print('Page {}/{}'.format(pagenum, len(self.pages.keys())))

    def get_pdf_page(self, pagenum):
        return(self.pages[pagenum])

    def write_page_to_txt_file(self, pagenum, out_file):
        with open(out_file, 'w') as of:
            of.write(self.get_pdf_page(pagenum))
