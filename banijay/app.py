import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path
import time

'''
# Banijay: Content and Ratings Analysis :tv:

'''

df_file_path = Path().absolute()/"banijay/data/banijay_merged.csv"

#helper function to load data
@st.cache_data
def load_data(file_path):
    df_merged = pd.read_csv(df_file_path, infer_datetime_format=True)
    return df_merged

@st.cache_data
def filter_data(df, tg):
     return (df
    .pipe(to_datetime, ['date_time'], '%Y-%m-%d %H:%M:%S')
    .query('`ratings type` == "totaal" &\
            `target group` == @tg')
    ) 

@st.cache_data
def get_metrics(df):
    kdh = df['kdh000'].mean()
    print(kdh)
    kdh_delta = df['kdh000'].pct_change().mean()
    zadl = df['zadl%'].mean()
    zadl_delta = df['zadl%'].pct_change().mean()
    return(kdh, kdh_delta, zadl, zadl_delta)

@st.cache_data
def aggregate_data(df, agg, tg):
    return (df
    .pipe(to_datetime, ['date_time'], '%Y-%m-%d %H:%M:%S')
    .assign(
        month = lambda x: x['date_time'].dt.month, 
        year = lambda x: x['date_time'].dt.year, 
        day_of_week = lambda x: x['date_time'].dt.dayofweek)
    .loc[df_merged['ratings type'] == 'totaal', :]
    .loc[df_merged['target group'] ==  tg, :]
    .groupby([agg])['kdh000']
    .mean()
    )

#helper function (TODO: Refactor)
@st.cache_data
def to_datetime(df, cols, format):
    '''
    Function to convert a column to datetime 

    :param df: pandas dataframe
    :param cols: column to convert
    :param format: format of the date time (2022-09-16 23:19:00)
    '''
    def to_datetime(col):
        return pd.to_datetime(col, format = format)
    df[cols] = df[cols].apply(to_datetime)
    return df

#read in the dataframe
df_merged = load_data(file_path=df_file_path)
    
target_groups = df_merged['target group'].unique().tolist()
tg = st.selectbox("Select a target group of interest", target_groups)

f'''
## Key KPIs
### Weekly Report
'''

df_filter = filter_data(df=df_merged, tg=tg).set_index('date_time').last('7D')

kdh, kdh_delta, zadl, zadl_delta = get_metrics(df_filter)

col1, col2 = st.columns(2)
col1.metric("Kdh000", "{:2.2f}".format(kdh), "{:2.2f}".format(kdh_delta))
col2.metric("Zadl%", "{:2.2f}".format(zadl), "{:2.2f}".format(zadl_delta))

'''
## Show Analysis
'''
df_filter_id = df_filter.groupby('id').mean()
col1, col2 = st.columns(2)
with col1:
    st.bar_chart(df_filter_id, y=['kdh000','zadl%'])
with col2:
    st.dataframe(df_filter_id)


f'''
## Trend Analysis
Target Group: {tg}
'''
temporal_level = st.radio(
        "Choose temporal level👇",
        ["Day of the week", "Monthly", "Yearly"],
        key="visibility",
        label_visibility="hidden",
        horizontal=True,
    )

with st.spinner('The requested visualization is being generated...'):
    if temporal_level == "Day of the week":
        day_of_week_trend = aggregate_data(df=df_merged, agg = "day_of_week", tg=tg)
        st.area_chart(day_of_week_trend)
    elif temporal_level == "Monthly":
        monthly_trend = aggregate_data(df=df_merged, agg = "month", tg=tg)
        st.area_chart(monthly_trend)
    else:
        yearly_trend = aggregate_data(df=df_merged, agg = "year", tg=tg)
        st.area_chart(yearly_trend)




