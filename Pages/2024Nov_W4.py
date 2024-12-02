import streamlit as st
import pandas as pd
import numpy as np
# import gspread
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
st.markdown('''
            - Figure 1: Finished
            - Figure 2: Finished
            - Figure 3: Working on
            - Figure 4: 
            - Figure 5:
            - Figure S1:
            - Figure S2:
            ''')

st.header('Experiments')
st.subheader('20% conc. PLLA SGC')
st.markdown(''' 
            - actual conc. ~15% (23 mg PLLA in 150 mg AA)
            - 135C for ~ 1 hr 30 min
            - still can see the PLLA at the bottom of the glass tube
            - increase the temp to 136.5C for ~ 30 min
            - transfer to 90 C oil bath, color change can be observed within 30s, from transparent to white
            - 90 C for overnight
            ''')