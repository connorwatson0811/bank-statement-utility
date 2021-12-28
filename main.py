import process_statement

import pdftotext

import argparse
import logging


def parse_arguments(**kwargs):
    parser = argparse.ArgumentParser(description='This script tries to read in a PDF statement.')
    parser.add_argument('-pn', '--page', help='Read just one page', default=-1, type=int)
    parser.add_argument('-ra', '--raw', help='Store PDF pages in order it appears in content stream via pdftotext',
                        action='store_true', default=False)
    parser.add_argument('-ph', '--phy', help='Store PDF pages in order it appears regardless of format via pdftotext',
                        action='store_true', default=False)
    parser.add_argument('-vb', '--verbose', help='Turn on verbose debugging', action='store_true',
                        default=False)
    parser.add_argument('statement', help='Absolute\\Path\\To\\Statement.pdf')
    # parser.add_argument('config', help='Absolute\\Path\\To\\Params\\Json_File.json')
    args = parser.parse_args()
    log_fmt = '%(asctime)s LINE:%(lineno)d LEVEL:%(levelname)s %(message)s'
    args.verbose = kwargs.get('verbose_logs', False)
    if args.verbose:
        log_lvl = logging.DEBUG
    else:
        log_lvl = logging.INFO
    logging.basicConfig(level=log_lvl, format=log_fmt)
    '''
    if ret_args.log_file is not None:
		log_file = ret_args.log_file
		logging.basicConfig(level=log_lvl, filename=log_file, format=log_fmt)
	else:
		logging.basicConfig(level=log_lvl, format=log_fmt)
    '''
    return args


def main():
    cmd_args = parse_arguments(verbose_logs=True)
    p_num_check = int(cmd_args.page)
    statement_parser = process_statement.ProcessStatement(cmd_args.statement, raw=cmd_args.raw, physical=cmd_args.phy)
    statement_parser.read_pdf_file()
    page_numbers = statement_parser.get_page_numbers()
    if p_num_check > 0:
        logging.debug(f'Processing page #{p_num_check} only')
        output_file_name = f'C:\\Users\\watson\\Documents\\DataSets\\page_{p_num_check}.txt'
        logging.debug(f'Writing page #{p_num_check} only to {output_file_name}')
        statement_parser.write_page_to_txt_file(p_num_check, output_file_name)
    else:
        logging.debug(f'Will process all pages of the document')
        for page_num in page_numbers:
            output_file_name = f'C:\\Users\\watson\\Documents\\DataSets\\page_{page_num}.txt'
            logging.debug(f'Writing page #{page_num} to {output_file_name}')
            statement_parser.write_page_to_txt_file(page_num, output_file_name)


    #statement_parser.print_pdf_page(p_num)
    # statement_parser.pretty_print_page(3)
    #print(help(pdftotext))


if __name__ == '__main__':
    main()
