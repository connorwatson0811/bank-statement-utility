import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode # , JSCode
import pandas as pd
import pdftotext
import src.process_statement as process_statement
import argparse
import json
import logging
import os
import sys
import pathlib
from datetime import datetime

st.set_page_config(page_title = 'Bank Statement Automation')
st.markdown(
    f"""
<style>
        .appview-container .main .block-container{{
        max-width: {1300}px;
        padding-top: {6}rem;
        padding-right: {1}rem;
        padding-left: {1}rem;
        padding-bottom: {1}rem;
        }}
        .uploadedFile {{display: none}}
        footer {{visibility: hidden;}}
    """,
    unsafe_allow_html=True
)


logger = logging.getLogger('main_logger')

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

def aggridTableFormatIntColumnWithCommas(table_grid_options_builder, col_name):
    table_grid_options_builder.configure_column(col_name,
        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
        valueFormatter = f"data.{col_name}.toLocaleString('en-US');"
    )
    return table_grid_options_builder


# def main():    
#     p_num_check = int(config['page_numbers_to_read'])
#     out_dir = config['output_directory']
#     condense_output = config['condense_output']
#     file_prefix = config['condensed_filename_prefix']
#     transaction_categories = config['categories']
#     bank_type = config['bank_type']
    
#     condensed_all_transactions = {'Date': [], 'Description': [], 'Amount': [], 'Category': []}
#     logger.debug(f'Output directory is: {out_dir}')
#     if not os.path.exists(config['output_directory']):
#         os.mkdir(config['output_directory'])

#     for filepath in pathlib.Path(config['statements_path']).glob('**/*'):
#         statement_path = filepath.absolute()
#         fname = os.path.basename(statement_path).split(".")[0]
#         if os.path.isdir(os.path.abspath(statement_path)):
#             print('Found a directory, skipping...')
#             continue
#         statement_parser = process_statement.ProcessStatement(statement_path,
#                                                               raw=config['raw_pdf_content'],
#                                                               physical=config['physical_pdf_content'],
#                                                               categories=transaction_categories,
#                                                               bank_type=bank_type,
#                                                               year_of_statements=config['year_of_statements'])
#         statement_parser.read_pdf_file()
#         page_numbers = statement_parser.get_page_numbers()
#         #print(page_numbers)
#         if p_num_check > 0:
#             # logger.info(f'Processing page #{p_num_check} only')
#             output_pagefile_name = os.path.abspath(os.path.join(out_dir, f'{fname}_page_{p_num_check}.txt'))
#             logger.debug(f'Writing page #{p_num_check} only to {output_pagefile_name}')
#             # statement_parser.write_page_to_txt_file(p_num_check, output_pagefile_name)
#             statement_parser.process_pdf_page(p_num_check)
#         else:
#             #logger.info(f'Will process all pages of the document')
#             for page_num in page_numbers:
#                 output_pagefile_name = os.path.abspath(os.path.join(out_dir, f'{fname}_page_{page_num}.txt'))
#                 logger.debug(f'Writing page #{page_num} to {output_pagefile_name}')
#                 # statement_parser.write_page_to_txt_file(page_num, output_pagefile_name)
#                 statement_parser.process_pdf_page(page_num)
#         statement_parser.set_dataframe_from_data_dictionary()
#         if not condense_output:
#             output_file_name = os.path.abspath(os.path.join(out_dir, f'{fname}_transactions.csv'))
#             statement_parser.save_transactions_df_to_csv(output_file_name)
#         else:
#             condensed_all_transactions['Date'] += statement_parser.transactions['Date']
#             condensed_all_transactions['Description'] += statement_parser.transactions['Description']
#             condensed_all_transactions['Amount'] += statement_parser.transactions['Amount']
#             condensed_all_transactions['Category'] += statement_parser.transactions['Category']
#         transaction_categories = statement_parser.categories
#     if condense_output:
#         output_file_name = os.path.abspath(os.path.join(out_dir, f'{file_prefix}_transactions.csv'))
#         condensed_all_transactions_df = pd.DataFrame.from_dict(condensed_all_transactions)
#         try:
#             condensed_all_transactions_df.to_csv(output_file_name)
#             print(f'Saved transactions to {output_file_name}')
#         except Exception as e:
#             logging.error(e)

#         print(f'Finished parsing statements, please check {out_dir}')

#     config['categories'] = transaction_categories
#     updated_config_path = in_args.config.replace('config', 'updated_config')
#     f = open(updated_config_path, 'w')
#     json.dump(config, f, indent=2) #\t
#     f.close()
#     print(f'Saved updated config to: {updated_config_path}')



st.title('Bank Statement Automation')

c1, c2 = st.columns(2)

with c1:
    list_of_statements = st.file_uploader(label='Upload bank statements', type=['pdf', 'csv'], accept_multiple_files=True)

    with open('data_input/Demo Bank Statement.pdf', 'rb') as bank_statement:
        btn = st.download_button(
            label='Download Demo Statement', 
            data=bank_statement, 
            file_name=f'Demo Bank Statement.pdf'
        )


with c2:
    bank_choice = st.selectbox(label='Select your bank: ',
                               options = ['Demo']
                               )
    st.session_state['bank_type'] = bank_choice


    # #transactions_upload = st.file_uploader(label='Upload transactions CSV instead', type=['csv'], accept_multiple_files=False)
    # config_path = 'data_input/config.json'
    # config = json.load(open(config_path))
    # p_num_check = int(config['page_numbers_to_read'])
    # out_dir = config['output_directory']
    # condense_output = config['condense_output']
    # file_prefix = config['condensed_filename_prefix']
    # transaction_categories = config['categories']
    # bank_type = config['bank_type']
    # # bank_type = 'chase'
    # st.session_state['bank_type'] = bank_type
    # raw_file = config['raw_pdf_content']
    # # raw_file = False
    # physical_file = config['physical_pdf_content']
    # # physical_file = True
    # condensed_all_transactions = {'Date': [], 'Description': [], 'Amount': [], 'Category': []}
    # verbose_logging = config['verbose_logging']
    
condense_output = True
condensed_all_transactions = {'Date': [], 'Description': [], 'Amount': [], 'Category': []}
config_path = 'data_input/config.json'
config = json.load(open(config_path))
raw_file = config['raw_pdf_content']
physical_file = config['physical_pdf_content']
file_prefix = config['condensed_filename_prefix']
transaction_categories = config['categories']
statements_year = 2024

# print(bank_type, raw_file, physical_file, verbose_logging, sep='\n')
with st.spinner(text = 'Preparing transactions...'):
    if list_of_statements is not None and 'transactions_df' not in st.session_state:
        # st.write(len(list_of_statements))
        # if len(list_of_statements) == 1:
        #     st.session_state['transactions_df'] = pd.read_csv(list_of_statements[0])
        # else:
        for statement in list_of_statements:
            statement_parser = process_statement.ProcessStatement(pdffileobject=statement,
                                                                raw=raw_file,
                                                                physical=physical_file,
                                                                categories=transaction_categories,
                                                                bank_type=bank_choice,
                                                                year_of_statements=statements_year)
            statement_parser.read_pdf_file()
            page_numbers = statement_parser.get_page_numbers()
            for page_num in page_numbers:
                statement_parser.process_pdf_page(page_num)
            statement_parser.set_dataframe_from_data_dictionary()
            #if not condense_output:
            #    output_file_name = os.path.abspath(os.path.join(out_dir, f'{fname}_transactions.csv'))
            #    statement_parser.save_transactions_df_to_csv(output_file_name)
            if condense_output:
                condensed_all_transactions['Date'] += statement_parser.transactions['Date']
                condensed_all_transactions['Description'] += statement_parser.transactions['Description']
                condensed_all_transactions['Amount'] += statement_parser.transactions['Amount']
                condensed_all_transactions['Category'] += statement_parser.transactions['Category']
            transaction_categories = statement_parser.categories
        if condense_output:
            #output_file_name = os.path.abspath(os.path.join(out_dir, f'{file_prefix}_transactions.csv'))
            condensed_all_transactions_df = pd.DataFrame.from_dict(condensed_all_transactions).sort_values(by='Date')
            csv_download = convert_df_to_csv(condensed_all_transactions_df)
            if condensed_all_transactions_df.shape[0] > 0:
                st.session_state['transactions_df'] = condensed_all_transactions_df
                st.download_button('Download Transactions', data=csv_download, file_name=f'{file_prefix}_transactions.csv')
            # try:
            #     condensed_all_transactions_df.to_csv(output_file_name)
            #     print(f'Saved transactions to {output_file_name}')
            # except Exception as e:
            #     logging.error(e)

            # print(f'Finished parsing statements, please check {out_dir}')
        if 'transactions_df' in st.session_state:
            st.session_state['transactions_df'] = st.session_state['transactions_df'].sort_values(by='Date')
            st.session_state['transactions_df'].reset_index(drop=True, inplace=True)
            config['categories'] = transaction_categories
            updated_config_path = config_path.replace('config', f"updated_config_{datetime.now().strftime('%Y%m%d')}")
            f = open(updated_config_path, 'w')
            json.dump(config, f, indent=2) #\t
            f.close()
            print(f'Saved updated config to: {updated_config_path}')

if 'transactions_df' in st.session_state:
    st.write(f"Total number of rows in transactions DF: {st.session_state['transactions_df'].shape[0]}")
    if st.session_state['transactions_df'].shape[0] > 1:
        gb = GridOptionsBuilder.from_dataframe(st.session_state['transactions_df'])
        # gb.configure_auto_height(False)
        # gb.configure_column(field='', width=395)
        gb.configure_pagination(
            enabled=True,
            paginationAutoPageSize=False,
            paginationPageSize=15
        )
        # gb.configure_default_column('editable=True')
        gb.configure_side_bar()
        # gb.configure_selection(selection_mode='single', use_checkbox=True)
        #gb.configure_grid_options(suppressMenuHide=False)#, icons={'menu': ':+1:'})
        grid_options = gb.build()
        grid_response = AgGrid(
            st.session_state['transactions_df'],
            gridOptions=grid_options,
            # data_return_mode = 'AS_INPUT',
            # update_mode = 'NO_UPDATE', # MODEL_CHANGED for sending subset of rows
            # update_mode = 'SELECTION_CHANGED',
            fit_columns_on_grid_load=True,
            # theme='balham', #balham, material, alpine
            # height=537,
            # width='100%',
            # reload_date=True
            
        )

        # selected = grid_response['selected_rows']
