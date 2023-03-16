import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path

df_file_path = Path().absolute()/"data/banijay_merged.csv"

#helper function (TODO: Refactor)
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
df_merged = pd.read_csv("./banijay/data/banijay_merged.csv", infer_datetime_format=True)

#visualize monthly trends
monthly_trend = (df_merged
    .pipe(to_datetime, ['date_time'], '%Y-%m-%d %H:%M:%S')
    .assign(
        month = lambda x: x['date_time'].dt.month)
    .loc[df_merged['ratings type'] == 'totaal', :]
    .groupby(['month'])['kdh000']
    .mean()
)

#visualize day of the week trends
day_of_week_trend = (df_merged
    .pipe(to_datetime, ['date_time'], '%Y-%m-%d %H:%M:%S')
    .assign(
        day_of_week = lambda x: x['date_time'].dt.dayofweek)
    .loc[df_merged['ratings type'] == 'totaal', :]
    .groupby(['day_of_week'])['kdh000']
    .mean()
)

#visualize yearly trends
yearly_trend = (df_merged
    .pipe(to_datetime, ['date_time'], '%Y-%m-%d %H:%M:%S')
    .assign(
        year = lambda x: x['date_time'].dt.year)
    .loc[df_merged['ratings type'] == 'totaal', :]
    .groupby(['year'])['kdh000']
    .mean()
)

        

#target group analysis
df_target = (df_merged
    .loc[df_merged['ratings type'] == 'totaal', :]
    .groupby(['target group'])['kdh000']
    .mean()
    .sort_values(ascending=False)
)

'''
# Banijay: Content and Ratings Analysis :tv:

This is an app that is dynamically updated when new data is available.
'''

'''
## Trend Analysis
'''
temporal_level = st.radio(
        "Choose temporal level👇",
        ["Day of the week", "Monthly", "Yearly"],
        key="visibility",
        label_visibility="hidden",
        horizontal=True,
    )

if temporal_level == "Daily":
    st.line_chart(day_of_week_trend)
elif temporal_level == "Monthly":
    st.line_chart(monthly_trend)
else:
    st.line_chart(yearly_trend)


'''
## Target Group Analysis
'''
st.bar_chart(df_target)
