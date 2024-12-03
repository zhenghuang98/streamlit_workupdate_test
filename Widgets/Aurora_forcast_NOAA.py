import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import schedule
from paddleocr import PaddleOCR,draw_ocr

st.title("Aurora Forecast")
ocr = PaddleOCR(lang='en')

@st.fragment(run_every=1800)
def show_current_forecast():
    # 设置图片的 URL
    image_url1 = "https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tonights_static_viewline_forecast.png"
    image_url2 = "https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tomorrow_nights_static_viewline_forecast.png"
    image_url3 = "https://services.swpc.noaa.gov/images/swx-overview-small.gif"

    col1, col2 = st.columns(2)
    with col1:
        st.image(image_url1, caption="Tonight's Aurora Forecast", use_container_width=True)
        result = ocr.ocr(image_url1, cls=True)
        extracted_texts = [item[1][0] for item in result[0]]
        st.write(extracted_texts)
    with col2:
        st.image(image_url2, caption="Tomorrow Night's Aurora Forecast", use_container_width=True)
        result = ocr.ocr(image_url2, cls=True)
        extracted_texts = [item[1][0] for item in result[0]]
        st.write(extracted_texts)
    # 使用 st.image 展示图片
    st.image(image_url3, caption="Space Weather Overview",  use_container_width=True)


show_current_forecast()