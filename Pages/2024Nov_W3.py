import streamlit as st
import pandas as pd
import numpy as np
import gspread
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt

##############################
Report_date = '2024 Nov W3'
##############################

##############################
# Repetitive code for each page
st.title(Report_date + ' Update')
st.write('This is the '+Report_date+' work report for Miyoshi group research')

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
            ''')
##############################

st.header('Data Analysis')

st.subheader('CODEX data analysis')
conn1 = st.connection("gsheets", type=GSheetsConnection)
df1 = conn1.read(spreadsheet=st.secrets.connections.gsheets.spreadsheet1,
                 ttl= 0)
st.write(df1)
st.image("Images/截图_20241123171056.png", caption="CODEX MGC data", use_container_width=True)



st.subheader('SGC DSC data analysis')


conn2 = st.connection("gsheets", type=GSheetsConnection)
df2 = conn2.read(spreadsheet=st.secrets.connections.gsheets.spreadsheet2,
                 ttl="10s")

st.write(df2)
numeric_df = df2.select_dtypes(include=["number"])
# st.line_chart(numeric_df, x= df['Sample'])
#st.write(df["Sample"].dtype)
# df["Sample"] = df["Sample"].astype(str)
# st.write(df["Sample"].dtype)

fig, ax = plt.subplots(figsize=(8, 6))
for column in numeric_df.columns:
    ax.plot(numeric_df.index, numeric_df[column], label=column)

ax.set_title("Line Chart of DSC Temperature")
ax.set_xlabel("Index")
ax.set_ylabel("Temperature")
ax.legend()
ax.grid(True)

st.pyplot(fig)
st.image("Images/截图_20241123172558.png", caption="DSC data", use_container_width=True)



st.subheader('WAXS data analysis')
col1, col2 = st.columns(2)

# 在左列显示第一张图片
with col1:
    st.image("Images/截图_20241123153325.png", caption="Weichen Paper Image", use_container_width=True)
# 在右列显示第二张图片
with col2:
    st.image("Images/截图_20241123153723.png", caption="155C crystallize fit", use_container_width=True)
    st.write('Crystallinity is ~77.5%')
    st.image("Images/截图_20241123153755.png", caption="90C crystallize fit", use_container_width=True)
    st.write('Crystallinity is ~55.7%')
st.markdown('''
            - haven't apply the empty hole correction
            - looks similar to Weichen's result
            - Privous NMR result for annealed MGC crystallinity is ~73%
            ''')

