import process_statement

import pdftotext

import argparse
import logging


def parse_arguments(**kwargs):
    parser = argparse.ArgumentParser(description='This script tries to read in a PDF statement.')
    # parser.add_argument('path', help='Absolute\\Path\\To\\Statement.pdf')
    parser.add_argument('-vb', '--verbose', help='Turn on verbose debugging', action='store_true',
                        default=False)
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
    logging.debug('Hello world!')
    statement_parser = process_statement.ProcessStatement()



if __name__ == '__main__':
    main()
