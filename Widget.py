import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

st.title("Widget Playground")

##################
st.write("### 现在几点")
@st.fragment(run_every=1)
def show_current_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    st.write(f"#### Current time: {current_time}")

show_current_time()

##################

# if 'start_time' not in st.session_state:
#     st.session_state.start_time = None
#     st.session_state.elapsed_time = timedelta()
#     st.session_state.running = False

# def start_timer():
#     if not st.session_state.running:
#         st.session_state.start_time = time.time()
#         st.session_state.running = True

# def stop_timer():
#     if st.session_state.running:
#         st.session_state.elapsed_time += timedelta(seconds=time.time() - st.session_state.start_time)
#         st.session_state.running = False
#         st.session_state.start_time = None

# st.title("Timer App")

# col1, col2 = st.columns(2)

# with col1:
#     if st.button("Start"):
#         start_timer()

# with col2:
#     if st.button("Stop"):
#         stop_timer()


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int(seconds % 3600 // 60)
    return f"{hours} hr {minutes} min"

# if st.session_state.running:
#     elapsed = st.session_state.elapsed_time + timedelta(seconds=time.time() - st.session_state.start_time)
# else:
#     elapsed = st.session_state.elapsed_time

# @st.fragment(run_every=1)
# def show_elapsed_time():
#     st.write(f"Elapsed time: {format_time(elapsed)}")

# show_elapsed_time()

##################

st.write("### 测试按钮")
# 数据存储
DATA_FILE = "work_time_records.csv"

# 初始化数据
def load_data():
    try:
        return pd.read_csv(DATA_FILE, parse_dates=["Start time", "End time"])
    except FileNotFoundError:
        return pd.DataFrame(columns=["Start time", "Endtime"])

def save_data(data):
    data.to_csv(DATA_FILE, index=False)

# 加载记录数据
work_data = load_data()

# def time_diff():
#     df = work_data.copy()
#     df["time_diff_sec"] = (df["end_time"] - df["start_time"]).dt.total_seconds()
#     df["formatted_time"] = df["time_diff_sec"].apply(format_time)
#     work_data = df
#     return work_data
# time_diff()


col1, col2 = st.columns(2)

if 'running' not in st.session_state:
    st.session_state.running = False

with col1:
    if st.button("Start", disabled=st.session_state.running):
        st.session_state.start_time_a = datetime.now().replace(microsecond=0)
        st.session_state.start_time_b = time.time()
        st.session_state.running = True
        st.rerun()
@st.fragment(run_every=1)
def show_elapsed_time():
    elapsed = time.time() - st.session_state.start_time_b
    st.write(f"Elapsed time: {int(elapsed // 3600)}小时 {int(elapsed % 3600 // 60)}分钟 {int(elapsed % 60)}秒")
        

with col2:
    if st.button("Stop", disabled=not st.session_state.running):
        st.session_state.running = False
        st.session_state.end_time_a = datetime.now()
        st.session_state.end_time_b = time.time()
        st.write(f"计时结束, 结束时间：{st.session_state.end_time_a.strftime("%Y-%m-%d %H:%M:%S")}")
        end_time = datetime.now().replace(microsecond=0)
        new_entry = {"Start time": st.session_state.start_time_a, "End time": end_time}
        work_data = pd.concat([work_data, pd.DataFrame([new_entry])], ignore_index=True)
        st.rerun()

if st.session_state.running:
    st.write(f"开始计时, 开始时间：{st.session_state.start_time_a}")
    show_elapsed_time()


# 工作时间记录（倒序排列）
st.write("### 工作时间记录")
if not work_data.empty:
    df = work_data
    df["Time Difference"] = (df["End time"] - df["Start time"])
    df["Time Difference"] = df["Time Difference"].dt.components.apply(lambda x: f"{x['hours']:02}:{x['minutes']:02}:{x['seconds']:02}", axis=1)
    work_data = df
    save_data(work_data)
    work_data = work_data.sort_values(by="End time", ascending=False).reset_index(drop=True)
    st.data_editor(work_data, use_container_width=True, num_rows="dynamic", height=300)


col3, col4 = st.columns(2)
with col3:
    if not work_data.empty:
        work_data["work_duration"] = (work_data["End time"] - work_data["Start time"]).dt.total_seconds() / 3600
        daily_summary = work_data.groupby(work_data["Start time"].dt.date)["work_duration"].sum().round(1)
    st.write(daily_summary)

with col4:
    if not work_data.empty:
        work_data["work_duration"] = (work_data["End time"] - work_data["Start time"]).dt.total_seconds() / 3600
        weekly_summary = work_data.groupby(work_data["Start time"].dt.to_period("W"))["work_duration"].sum().round(1)
    st.write(weekly_summary)

col5, col6 = st.columns(2)
with col5:
    # 修改已有记录
    st.write("#### 修改已有时间记录")
    if not work_data.empty:
        selected_row = st.selectbox("选择要修改的时间段", options=work_data.index, format_func=lambda x: f"开始: {work_data.loc[x, 'Start time']}, 结束: {work_data.loc[x, 'End time']}")
        with st.form("edit_time_form"):
            start_date = st.date_input("开始日期", value=work_data.loc[selected_row, "Start time"].date())
            start_time = st.time_input("开始时间", value=work_data.loc[selected_row, "Start time"].time())
            end_date = st.date_input("结束日期", value=work_data.loc[selected_row, "End time"].date())
            end_time = st.time_input("结束时间", value=work_data.loc[selected_row, "End time"].time())
            submitted = st.form_submit_button("保存修改")
            if submitted:
                new_start = datetime.combine(start_date, start_time)
                new_end = datetime.combine(end_date, end_time)
                if new_start >= new_end:
                    st.error("结束时间必须晚于开始时间！")
                else:
                    work_data.loc[selected_row, "Start time"] = new_start
                    work_data.loc[selected_row, "End time"] = new_end
                    save_data(work_data)
                    st.rerun()
                    st.success("时间记录已更新！")

with col6:
    # 增加时间段
    st.write("#### 增加时间段")
    with st.form("add_time_form"):
        start_date = st.date_input("开始日期", value=datetime.now().date())
        start_time = st.time_input("开始时间", value=datetime.now().time())
        end_date = st.date_input("结束日期", value=datetime.now().date())
        end_time = st.time_input("结束时间", value=(datetime.now() + timedelta(hours=1)).time())
        submitted = st.form_submit_button("添加时间段")
        if submitted:
            start_datetime = datetime.combine(start_date, start_time)
            end_datetime = datetime.combine(end_date, end_time)
            if start_datetime >= end_datetime:
                st.error("结束时间必须晚于开始时间！")
            else:
                new_entry = {"Start time": start_datetime, "End time": end_datetime}
                work_data = pd.concat([work_data, pd.DataFrame([new_entry])], ignore_index=True)
                save_data(work_data)
                st.success("时间段已添加！")
                st.rerun()

    # 删除时间段
    st.write("#### 删除时间段")
    if not work_data.empty:
        selected_row = st.selectbox("选择要删除的时间段", options=work_data.index, format_func=lambda x: f"开始: {work_data.loc[x, 'Start time']}, 结束: {work_data.loc[x, 'End time']}")
        if st.button("删除所选时间段"):
            work_data = work_data.drop(index=selected_row).reset_index(drop=True)
            save_data(work_data)
            st.success("时间段已删除！")
            st.rerun()
