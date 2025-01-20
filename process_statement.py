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

    def __init__(self, **kwargs):
        self.pages = {}
        self.pdfpath = kwargs.get('pdfpath', None)
        self.pdffileobject = kwargs.get('pdffileobject', None)
        self.pdf_raw_output = kwargs.get('raw', False)
        self.pdf_phy_output = kwargs.get('physical', False)
        self.bank_type = kwargs.get('bank_type', 'boa')
        self.categories = kwargs.get('categories', None)
        self.transactions = {'Date':[], 'Description': [], 'Amount': [], 'Category': []}
        self.transactions_df = None
        self.year_of_statements = kwargs.get('year_of_statements', '2022')

    def read_pdf_file(self):
        '''
        Step 1 - read the PDF file and assign to a pdf object
        '''
        try:
            if self.pdfpath is not None:
                with open(self.pdfpath, 'rb') as f:
                    pdf = pdftotext.PDF(f, raw=self.pdf_raw_output, physical=self.pdf_phy_output)
            elif self.pdffileobject is not None:
                #with open(self.pdffileobject, 'rb') as f:
                #pdf_file = self.pdffileobject.read()
                pdf = pdftotext.PDF(self.pdffileobject, raw=self.pdf_raw_output, physical=self.pdf_phy_output)
        except FileNotFoundError as fe:
            logging.error('File not found with path: ' + self.pdfpath)
            return None
        except Exception as e:
            logging.error('Unexpected error occured!')
            logging.error(e)
            return None
        for pagenum in range(len(pdf)):
            self.pages[pagenum + 1] = pdf[pagenum]
        if self.pdfpath is not None:
            print(f'Processing {self.pdfpath}')
        else:
            print(f'Processing uploaded file')

    def print_pdf_page(self, pagenum):
        print(self.pages[pagenum])

    def pretty_print_page(self, pagenum):
        for line in self.pages[pagenum].split('\n'):
            print(line)

    def get_page_numbers(self):
        '''
        Step 2 - get all the page numbers
        '''
        return list(sorted(self.pages.keys()))

    def print_page_numbers(self):
        for pagenum in sorted(self.pages.keys()):
            print('Page {}/{}'.format(pagenum, len(self.pages.keys())))

    def get_pdf_page(self, pagenum):
        return self.pages[pagenum]

    def write_page_to_txt_file(self, pagenum, out_file):
        with open(out_file, 'w') as of:
            of.write(self.get_pdf_page(pagenum))

    def process_pdf_page(self, page_num):
        '''
        Step 3 - process PDF page based on the bank
        '''
        current_page_lines = self.get_pdf_page(page_num).split('\n')
        if self.bank_type == 'boa':
            self.process_pdf_page_boa(current_page_lines, page_num)
        elif self.bank_type == 'chase':
            self.process_pdf_page_chase(current_page_lines, page_num)

    def process_pdf_page_chase(self, current_page_lines, pnum):
        print(f'Checking Chase page num {pnum}')
        num_line_with_transactions = 0
        deposit_or_withdrawal = ""
        for line in current_page_lines:
            line = line.strip()
            if "deposits" in line.lower():
                deposit_or_withdrawal = ""
            elif "withdrawals" in line.lower():
                deposit_or_withdrawal = "-"
            try:
                int(line[0])
            except ValueError as ve:
                continue
            except Exception as e:
                continue
            if re.search("[0-9][0-9]/[0-9][0-9]", line[:5]) and len(line) > 10:
                num_line_with_transactions += 1
                transaction_date = f"{line[:8].strip()}/{self.year_of_statements}"
                line_temp = line[8:]
                transaction_regex = r"\$?([0-9]+,?)+\.[0-9][0-9]"
                # try:
                transaction_amount = deposit_or_withdrawal + re.search(transaction_regex, line_temp).group().strip("$")
                # except AttributeError as ae:
                #     print(transaction_date)
                #     print(line_temp)
                #     print(line)
                #     print(line[:8])
                #     sys.exit(0)

                transaction_description = is_transaction_a_check(re.sub(transaction_regex, "", line_temp).strip())
                transaction_category = self.assign_category_to_transaction(transaction_description)
                self.add_transaction_to_data_dictionary(transaction_date,
                                                        transaction_description,
                                                        transaction_amount,
                                                        transaction_category)
        if num_line_with_transactions == 0:
            print(f'Page {pnum} with total {num_line_with_transactions} lines with transactions')
        else:
            print(f'Page {pnum} with total {num_line_with_transactions} lines with transactions')

    def process_pdf_page_boa(self, current_page_lines, pnum):
        print(f'Checking BOA page num {pnum}')
        num_line_with_transactions = 0
        for line in current_page_lines:
            line = line.strip()
            try:
                int(line[0])
            except ValueError as ve:
                continue
            except Exception as e:
                continue
            if re.search("[0-9][0-9]/[0-9][0-9]/[0-9][0-9]", line[:8]):
                print(f'PROCESSING PAGE {pnum}')
                num_line_with_transactions += 1
                transaction_date = line[:8]
                line_temp = line[8:]
                print(f'line_temp: {line_temp}')
                transaction_regex = r"-?([0-9]+,?)+\.[0-9][0-9]"
                transaction_amount = re.search(transaction_regex, line_temp).group()
                transaction_description = is_transaction_a_check(re.sub(transaction_regex, "", line_temp).strip())
                transaction_category = self.assign_category_to_transaction(transaction_description)
                self.add_transaction_to_data_dictionary(transaction_date,
                                                        transaction_description,
                                                        transaction_amount,
                                                        transaction_category)
        if num_line_with_transactions == 0:
            print(f'Page {pnum} with total {num_line_with_transactions} lines with transactions')
        else:
            print(f'Page {pnum} with total {num_line_with_transactions} lines with transactions')

    def assign_category_to_transaction(self, desc):
        desc_lower = desc.lower()
        if self.categories is not None:
            for category in self.categories:
                for category_phrase in self.categories[category]:
                    if category_phrase in desc_lower:
                        return category
            self.categories['other'].append(desc_lower.strip())
            return "other"
        else:
            return "transaction"

    def add_transaction_to_data_dictionary(self, date, desc, amount, catg):
        print(f'{date} | {amount} | {desc} | {catg}')
        self.transactions['Date'].append(date)
        self.transactions['Description'].append(desc)
        self.transactions['Amount'].append(amount)
        self.transactions['Category'].append(catg)

    def set_dataframe_from_data_dictionary(self):
        self.transactions_df = pd.DataFrame.from_dict(data=self.transactions)

    def save_transactions_df_to_csv(self, out_file, transactions_df=None):
        if transactions_df is None:
            transactions_df = self.transactions_df
        try:
            transactions_df.to_csv(out_file)
            print(f'Saved transactions to {out_file}')
        except Exception as e:
            logging.error(e)
