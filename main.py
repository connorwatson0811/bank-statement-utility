import pdftotext
import process_statement
import argparse
import json
import logging
import os
import sys
import pathlib
logger = logging.getLogger('main_logger')


def parse_arguments(): # **kwargs
    global logger
    parser = argparse.ArgumentParser(description='This script tries to read in a PDF statement.')
    # parser.add_argument('-pn', '--page', help='Read just one page', default=-1, type=int)
    # parser.add_argument('-ra', '--raw', help='Store PDF pages in order it appears in content stream via pdftotext',
    #                     action='store_true', default=False)
    # parser.add_argument('-ph', '--phy', help='Store PDF pages in order it appears regardless of format via pdftotext',
    #                     action='store_true', default=False)
    # parser.add_argument('-vb', '--verbose', help='Turn on verbose debugging', action='store_true',
    #                     default=False)
    # parser.add_argument('statement', help='Absolute\\Path\\To\\Statement.pdf')
    parser.add_argument('config', help='Absolute\\Path\\To\\Params\\Json_File.json', default=None)
    parser.add_argument('-vb', '--verbose', help='Turn on verbose debugging', action='store_true',
                        default=False)
    args = parser.parse_args()

    try:
        config = json.load(open(args.config))
    except Exception as e:
        print(str(e))
        sys.exit(1)
    log_fmt = '%(asctime)s LINE:%(lineno)d %(module)s LEVEL:%(levelname)s %(message)s'
    verbose_logs = config['verbose_logging']
    if verbose_logs:
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
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_lvl)
    stream_handler.setFormatter(logging.Formatter(log_fmt))
    logger.addHandler(stream_handler)
    return args

"""
another funciton with error checking
    # try:
    #
    # except json.decoder.JSONDecodeError as je:
    #     logging.error(je)
    #     sys.exit(1)
    # except Exception as e:
    #     logging.error('Something else happened')
    #     logging.error(e)
    #     sys.exit(1)

    # if config['statements_path'] is not None and config['statements_path'] != '':
    #     assert os.path.exists(config['statements_path']), "Please configure a valid directory to bank statements"
    #     assert os.path.isdir(config['statements_path']), "Please configure a directory to bank statements"
    #     assert len(os.listdir(config['statements_path'])) != 0, \
    #         "Please configure a non-empty directory to bank statements"
    # if not os.path.exists(config['output_directory']):
    #     os.mkdir(config['output_directory'])
"""


def main():
    in_args = parse_arguments()
    config = json.load(open(in_args.config))
    p_num_check = int(config['page_numbers_to_read'])
    out_dir = config['output_directory']
    logger.debug(f'Output directory is: {out_dir}')
    if not os.path.exists(config['output_directory']):
        os.mkdir(config['output_directory'])
    for filepath in pathlib.Path(config['statements_path']).glob('**/*'):
        statement_path = filepath.absolute()
        fname = os.path.basename(statement_path).split(".")[0]
        if os.path.isdir(os.path.abspath(statement_path)):
            continue
        statement_parser = process_statement.ProcessStatement(statement_path,
                                                              raw=config['raw_pdf_content'],
                                                              physical=config['physical_pdf_content'])
        logger.debug(statement_path)
        statement_parser.read_pdf_file()
        page_numbers = statement_parser.get_page_numbers()
        if p_num_check > 0:
            logger.debug(f'Processing page #{p_num_check} only')
            output_file_name = os.path.abspath(os.path.join(out_dir, f'{fname}_page_{p_num_check}.txt'))
            logger.debug(f'Writing page #{p_num_check} only to {output_file_name}')
            statement_parser.write_page_to_txt_file(p_num_check, output_file_name)
            statement_parser.process_pdf_page(p_num_check)
        else:
            logger.debug(f'Will process all pages of the document')
            for page_num in page_numbers:
                output_file_name = os.path.abspath(os.path.join(out_dir, f'{fname}_page_{page_num}.txt'))
                logger.debug(f'Writing page #{page_num} to {output_file_name}')
                statement_parser.write_page_to_txt_file(page_num, output_file_name)


if __name__ == '__main__':
    main()
