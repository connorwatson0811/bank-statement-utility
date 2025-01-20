import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode # , JSCode
import pandas as pd
import pdftotext
import process_statement
import argparse
import json
import logging
import os
import sys
import pathlib
from datetime import datetime

date_format = "%m/%d/%y" if st.session_state['bank_type'] == 'boa' else "%m/%d/%Y"
# Date | Description | Amount | Category | 
if 'transactions_df' not in st.session_state:
    st.warning('Please parse your bank statements first')
else:
    st.session_state['transactions_df']['Date'] = pd.to_datetime(st.session_state['transactions_df']['Date'], format=date_format)
    
    
    max_date = st.session_state['transactions_df']['Date'].max()
    min_date = st.session_state['transactions_df']['Date'].min()
    min_date_filter = datetime.combine(st.sidebar.date_input('Start Date', value=min_date, min_value=min_date, max_value=max_date), datetime.min.time())
    max_date_filter = datetime.combine(st.sidebar.date_input('End Date', value=max_date, min_value=min_date, max_value=max_date), datetime.min.time())
    
    filtered_df = st.session_state['transactions_df'].loc[(st.session_state['transactions_df']['Date'] >= min_date_filter) & 
                                                          (st.session_state['transactions_df']['Date'] <= max_date_filter)]

    st.line_chart(
        data=filtered_df,
        x='Date',
        y='Amount'
    )

    st.bar_chart(
        data = filtered_df,
        x='Category',
        y='Amount'
    )