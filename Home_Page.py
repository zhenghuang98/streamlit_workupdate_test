import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.express as px
import time

st.title("工作时间记录工具")
@st.fragment(run_every=1)
def show_current_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    st.write(f"#### Current time: {current_time}")

show_current_time()

# 数据存储
DATA_FILE = "work_time_records.csv"

# 初始化数据
def load_data():
    try:
        return pd.read_csv(DATA_FILE, parse_dates=["start_time", "end_time"])
    except FileNotFoundError:
        return pd.DataFrame(columns=["start_time", "end_time"])

def save_data(data):
    data.to_csv(DATA_FILE, index=False)

# 加载记录数据
work_data = load_data()

#col1, col2 = st.columns(2)
#with col1:
#    if st.button("Start"):
#       start_timer()

#with col2:
 #   if st.button("Stop"):
 #       stop_timer()


# 显示实时工作时长（每分钟刷新）
if "start_time" in st.session_state:
    elapsed_time_placeholder = st.empty()
    if "start_time_last_updated" not in st.session_state:
        st.session_state["start_time_last_updated"] = datetime.now()

# 开始按钮
if st.button("开始"):
    if "start_time" not in st.session_state:
        st.session_state["start_time"] = datetime.now()
        st.success(f"记录开始时间：{st.session_state['start_time']}")
        elapsed_time_placeholder = st.empty()
    else:
        st.info(f"计时已开始于：{st.session_state['start_time']}")
# 结束按钮
if st.button("结束"):
    if "start_time" in st.session_state:
        end_time = datetime.now()
        new_entry = {"start_time": st.session_state["start_time"], "end_time": end_time}
        work_data = pd.concat([work_data, pd.DataFrame([new_entry])], ignore_index=True)
        save_data(work_data)
        st.success(f"记录结束时间：{end_time}")
        del st.session_state["start_time"]
    else:
        st.warning("请先点击'开始'按钮！")

# 实时显示工作时长（每分钟更新一次）
if "start_time" in st.session_state:
    start_time = st.session_state["start_time"]
    elapsed_time = datetime.now() - start_time
    elapsed_time_placeholder.write(f"已经工作了：{elapsed_time.seconds // 3600}小时 {elapsed_time.seconds % 3600 // 60}分钟 {elapsed_time.seconds % 60}秒")

# 工作时间记录（倒序排列）
st.write("### 工作时间记录")
if not work_data.empty:
    work_data = work_data.sort_values(by="end_time", ascending=False).reset_index(drop=True)
    st.data_editor(work_data, use_container_width=True)

# 每日和每周统计
if not work_data.empty:
    work_data["work_duration"] = (work_data["end_time"] - work_data["start_time"]).dt.total_seconds() / 3600
    daily_summary = work_data.groupby(work_data["start_time"].dt.date)["work_duration"].sum()
    weekly_summary = work_data.groupby(work_data["start_time"].dt.to_period("W"))["work_duration"].sum()

    # 格式化每周的时间段
    weekly_summary.index = weekly_summary.index.map(lambda x: f"{x.start_time:%Y %b} W{x.week}")

    st.write("### 每日工作时间")
    st.bar_chart(daily_summary,x_label='Date',y_label='Hours',color='#75cbcd')

    st.write("### 每周工作时间")
    st.bar_chart(weekly_summary,x_label='Week',y_label='Hours',color='#75cbcd')

# 时间线展示（X/Y 轴互换）
if not work_data.empty:
    st.write("### 时间线展示")
    fig = px.timeline(
        work_data,
        y="start_time",
        x_start="start_time",
        x_end="end_time",
        title="工作时间线",
        labels={"start_time": "开始时间", "end_time": "结束时间", "y": "日期"},
    )
    st.plotly_chart(fig, use_container_width=True)
# 绘制时间线
if not work_data.empty:
    st.write("### 时间线展示")
    work_data["start_date"] = work_data["start_time"].dt.date
    work_data["start_hour"] = work_data["start_time"].dt.hour + work_data["start_time"].dt.minute / 60
    work_data["end_hour"] = work_data["end_time"].dt.hour + work_data["end_time"].dt.minute / 60

    fig = px.timeline(
        work_data,
        x_start="start_time",
        x_end="end_time",
        y="start_date",
        title="工作时间线",
        labels={"start_date": "日期", "start_time": "开始时间", "end_time": "结束时间"},
    )
    st.plotly_chart(fig, use_container_width=True)

edited_data = st.data_editor(work_data, use_container_width=True, key="editable_data")



# 修改已有记录
st.write("### 修改已有时间记录")
if not work_data.empty:
    selected_row = st.selectbox("选择要修改的时间段", options=work_data.index, format_func=lambda x: f"开始: {work_data.loc[x, 'start_time']}, 结束: {work_data.loc[x, 'end_time']}")
    with st.form("edit_time_form"):
        start_date = st.date_input("开始日期", value=work_data.loc[selected_row, "start_time"].date())
        start_time = st.time_input("开始时间", value=work_data.loc[selected_row, "start_time"].time())
        end_date = st.date_input("结束日期", value=work_data.loc[selected_row, "end_time"].date())
        end_time = st.time_input("结束时间", value=work_data.loc[selected_row, "end_time"].time())
        submitted = st.form_submit_button("保存修改")
        if submitted:
            new_start = datetime.combine(start_date, start_time)
            new_end = datetime.combine(end_date, end_time)
            if new_start >= new_end:
                st.error("结束时间必须晚于开始时间！")
            else:
                work_data.loc[selected_row, "start_time"] = new_start
                work_data.loc[selected_row, "end_time"] = new_end
                save_data(work_data)
                st.success("时间记录已更新！")

# 增加时间段
st.write("### 增加时间段")
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
            new_entry = {"start_time": start_datetime, "end_time": end_datetime}
            work_data = pd.concat([work_data, pd.DataFrame([new_entry])], ignore_index=True)
            save_data(work_data)
            st.success("时间段已添加！")

# 删除时间段
st.write("### 删除时间段")
if not work_data.empty:
    selected_row = st.selectbox("选择要删除的时间段", options=work_data.index, format_func=lambda x: f"开始: {work_data.loc[x, 'start_time']}, 结束: {work_data.loc[x, 'end_time']}")
    if st.button("删除所选时间段"):
        work_data = work_data.drop(index=selected_row).reset_index(drop=True)
        save_data(work_data)
        st.success("时间段已删除！")


