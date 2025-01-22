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

date_format = "%m/%d/%y" if st.session_state['bank_type'] in ('boa', 'Demo') else "%m/%d/%Y"
# Date | Description | Amount | Category | 
if 'transactions_df' not in st.session_state:
    st.warning('Please parse your bank statements first')
else:
    if 'Date_As_Datetime' not in st.session_state['transactions_df'].columns:
        st.session_state['transactions_df']['Date_As_Datetime'] = pd.to_datetime(st.session_state['transactions_df']['Date'], format=date_format)
        # st.session_state['transactions_df']['Date'] = st.session_state['transactions_df']['Date'].dt.strftime('%Y-%m-%d')
    st.session_state['transactions_df']['Amount'] = st.session_state['transactions_df']['Amount'].astype(float)
    
    max_date = st.session_state['transactions_df']['Date_As_Datetime'].max()
    min_date = st.session_state['transactions_df']['Date_As_Datetime'].min()
    min_date_filter = datetime.combine(st.sidebar.date_input('Start Date', value=min_date, min_value=min_date, max_value=max_date), datetime.min.time())
    max_date_filter = datetime.combine(st.sidebar.date_input('End Date', value=max_date, min_value=min_date, max_value=max_date), datetime.min.time())
    
    filtered_df = st.session_state['transactions_df'].loc[(st.session_state['transactions_df']['Date_As_Datetime'] >= min_date_filter) & 
                                                          (st.session_state['transactions_df']['Date_As_Datetime'] <= max_date_filter)]

    st.line_chart(
        data=filtered_df,
        x='Date',
        y='Amount'
    )

    st.dataframe(st.session_state['transactions_df'])

    # st.bar_chart(
    #     data = filtered_df,
    #     x='Category',
    #     y='Amount'
    # )