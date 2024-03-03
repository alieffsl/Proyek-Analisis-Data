import pandas as pd
import numpy as np
import seaborn as sns

import streamlit as st
import os, datetime
from utils import *

# dir = "../data/"
df_day = pd.read_csv("https://raw.githubusercontent.com/alieffsl/Proyek-Analisis-Data/main/data/day.csv?token=GHSAT0AAAAAACO7JKVX2DZAM5NYOSD6SLQKZPD65MQ")
df_hour = pd.read_csv("https://raw.githubusercontent.com/alieffsl/Proyek-Analisis-Data/main/data/hour.csv?token=GHSAT0AAAAAACO7JKVXYRUF6E6BEBGQKV3OZPD66RA")

if not os.path.isfile(df_day):
    print(f"Error: {df_day} does not exist.")

if not os.path.isfile(df_hour):
    print(f"Error: {df_hour} does not exist.")

# Preproc
df_day = preprocess_data(df_day)
df_hour = preprocess_data(df_hour)

min_date = df_day['dteday'].min()
max_date = df_day['dteday'].max()

#Sidebar
header, _ = st.columns([0.8, 0.2])

mode_col, date_col, time_start_col, time_end_col = header.columns([10, 15, 8, 8])

selected_mode = mode_col.radio("Select mode:", ["Daily", "Hourly"])

if selected_mode == "Daily":
    date_range = date_col.date_input(
        label='Select Date Range:',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    df_cur = filter_data(df_day, date_range)

    monthly_plot = monthly_plot(df_cur)
    st.pyplot(monthly_plot.figure)

    seasonly_group_plot = monthly_or_seasonly_pie(df_cur, by='season')
    monthly_group_plot = monthly_or_seasonly_pie(df_cur, by='mnth')

    with st.columns([0.5, 0.5]):
        st.pyplot(seasonly_group_plot, use_container_width=True)
        st.pyplot(monthly_group_plot, use_container_width=True)

else:
    date_range = date_col.date_input(
        label='Select Date Range:',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    time_start = time_start_col.time_input('Start Time:', datetime.time(0, 0))
    time_end = time_end_col.time_input('End Time:', datetime.time(23, 0))

    df_cur = filter_data(df_hour, date_range, (time_start, time_end))

    hourly_plot = hourly_bar(df_cur)
    st.pyplot(hourly_plot.figure)

    seasonly_group_plot = monthly_or_seasonly_pie(df_cur, by='season')
    monthly_group_plot = monthly_or_seasonly_pie(df_cur, by='mnth')

    with st.columns([0.5, 0.5]):
        st.pyplot(seasonly_group_plot, use_container_width=True)
        st.pyplot(monthly_group_plot, use_container_width=True)

st.dataframe(df_cur)




