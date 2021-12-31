import logging
import sys
import re
import pdftotext
# logging.getLogger('statement_logging')


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
            logging.error('File not found with path: ' + self.pdfpath)
            sys.exit(0)
        except Exception as e:
            logging.error('Unexpected error occured!')
            logging.error(e)
            sys.exit(0)
        for pagenum in range(len(pdf)):
            self.pages[pagenum + 1] = pdf[pagenum]

    def print_pdf_page(self, pagenum):
        logging.info(self.pages[pagenum])

    def pretty_print_page(self, pagenum):
        for line in self.pages[pagenum].split('\n'):
            logging.info(line)

    def get_page_numbers(self):
        return list(sorted(self.pages.keys()))

    def print_page_numbers(self):
        for pagenum in sorted(self.pages.keys()):
            logging.info('Page {}/{}'.format(pagenum, len(self.pages.keys())))

    def get_pdf_page(self, pagenum):
        return self.pages[pagenum]

    def write_page_to_txt_file(self, pagenum, out_file):
        with open(out_file, 'w') as of:
            of.write(self.get_pdf_page(pagenum))

    def process_pdf_page(self, page_num):
        num_line_with_transactions = 0
        for line in self.get_pdf_page(page_num).split('\n'):
            try:
                int(line[0])
            except ValueError as ve:
                continue
            except Exception as e:
                continue
            if re.search("[0-9][0-9]/[0-9][0-9]/[0-9][0-9]", line[:8]):
                num_line_with_transactions += 1
                transaction_date = line[:8]
                line_temp = line[8:]
                logging.debug(line_temp)
                transaction_regex = r"-?([0-9]+,?)+\.[0-9][0-9]"
                transaction_amount = re.search(transaction_regex, line_temp).group()
                transaction_description = re.sub(transaction_regex, "", line_temp).strip()
                logging.debug(f'{transaction_date} | {transaction_amount} | {transaction_description}')
        logging.info(f'Total {num_line_with_transactions} lines with transactions')



