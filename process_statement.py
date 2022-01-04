import logging
import sys
import re
import pandas as pd
import pdftotext
# logging.getLogger('statement_logging')


def is_transaction_a_check(transaction_description: str):
    try:
        int(transaction_description)
        return f"Check Number {transaction_description}"
    except ValueError as ve:
        return transaction_description


class ProcessStatement:

    """This class contains all the processing functions for one PDF statement (specific to one particular bank)"""

    def __init__(self, pdfpath, **kwargs):
        self.pdfpath = pdfpath
        self.pages = {}
        self.pdf_raw_output = kwargs.get('raw', False)
        self.pdf_phy_output = kwargs.get('physical', False)
        self.bank_type = kwargs.get('bank_type', 'BoA')
        self.transactions = {'Date':[], 'Description': [], 'Amount': []}
        self.transactions_df = None

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
        logging.info(f'Processing {self.pdfpath}')

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
        current_page_lines = self.get_pdf_page(page_num).split('\n')
        if self.bank_type == 'BoA':
            self.process_pdf_page_boa(current_page_lines, page_num)

    def process_pdf_page_boa(self, current_page_lines, pnum):
        num_line_with_transactions = 0
        for line in current_page_lines:
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
                transaction_description = is_transaction_a_check(re.sub(transaction_regex, "", line_temp).strip())
                self.add_transaction_to_data_dictionary(transaction_date,
                                                        transaction_description,
                                                        transaction_amount)
        if num_line_with_transactions == 0:
            logging.debug(f'Page {pnum} with total {num_line_with_transactions} lines with transactions')
        else:
            logging.info(f'Page {pnum} with total {num_line_with_transactions} lines with transactions')

    def add_transaction_to_data_dictionary(self, date, desc, amount):
        logging.debug(f'{date} | {amount} | {desc}')
        self.transactions['Date'].append(date)
        self.transactions['Description'].append(desc)
        self.transactions['Amount'].append(amount)

    def set_dataframe_from_data_dictionary(self):
        self.transactions_df = pd.DataFrame.from_dict(data=self.transactions)

    def save_transactions_df_to_csv(self, out_file, transactions_df=None):
        if transactions_df is None:
            transactions_df = self.transactions_df
        try:
            transactions_df.to_csv(out_file)
            logging.info(f'Saved transactions to {out_file}')
        except Exception as e:
            logging.error(e)
