import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

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

'''
# Banijay: Content and Ratings Analysis :tv:

This is an app that is dynamically updated. 
Sit back and enjoy the show.
'''


#read in the dataframe
df_merged = pd.read_csv("/workspaces/banijay-streamlit-app/banijay/data/banijay_merged.csv", infer_datetime_format=True)

st.write("Monthly trends")

#visualize monthly trends
monthly_trend = (df_merged
    .pipe(to_datetime, ['date_time'], '%Y-%m-%d %H:%M:%S')
    .assign(
        month = lambda x: x['date_time'].dt.month)
    .loc[df_merged['ratings type'] == 'totaal', :]
    .groupby(['month'])['kdh000']
    .mean()
)

st.area_chart(monthly_trend)

#target group analysis
(df_merged
    .loc[df_merged['ratings type'] == 'totaal', :]
    .groupby(['target group'])['kdh000']
    .mean()
    .sort_values(ascending=False)
    .plot(kind='bar', 
          figsize=(10,5), 
          title='Mean kdh000 per target group based on ratings type totaal',
          grid=True,
          color='orange',
          legend=True)
)