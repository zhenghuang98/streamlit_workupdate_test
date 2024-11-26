import streamlit as st
import pandas as pd
import numpy as np
import gspread
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt

##############################
Report_date = '2024 Nov W4'
##############################

##############################
# Repetitive code for each page
st.title(Report_date + ' Update')
st.write('This is the '+Report_date+' work report for Miyoshi group research')
st.write('11/23/2024-11/30/2024, Thanksgiving week')

st.header('Work Summary')
st.markdown('''
            1. Data Analysis
                - CODEX data analysis
                - WAXS data analysis
                - DSC data analysis
            2. Paper Writing
                - Figure revision
                - SI information
                - manuscript revision
            3. Experiments
                - 20% conc. PLLA SGC
                - DSC Test 
            ''')
##############################

st.header('Data Analysis')

st.subheader('CODEX data analysis')

st.header('Paper Writing')
st.subheader('Figure revision')