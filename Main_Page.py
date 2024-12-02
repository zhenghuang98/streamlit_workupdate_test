import streamlit as st
import pandas as pd
import numpy as np



pages = {
    "Home": [
        st.Page("Home_Page.py", title="Home"),
        st.Page("Widget.py", title="Widget"),
    ],
    "Weekly Update": [
        st.Page("Pages/2024Nov_W3.py", title="2024 Nov W3 Update"),
        st.Page("Pages/2024Nov_W4.py", title="2024 Nov W4 Update"),

    ],
    "Report": [
        st.Page("Reports/PaperII_discuss.py", title="Paper II Discussion"),

    ],
}

pg = st.navigation(pages)
pg.run()