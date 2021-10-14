import logging
import sys

import pdftotext


class AutomatedTools:
    """This class contains several functions to allow project level access to basic functions"""

    def __init__(self):
        pass

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