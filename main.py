
import streamlit as st
import pandas as pd
import numpy as np
from web_scraping import get_tw

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")



@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data

dict1 = get_tw()
tws = pd.DataFrame.from_dict(dict1,orient='index')


st.title('Dashboard')
st.markdown('Welcome to dashboard for the project XXXXX')
st.markdown('* this is a bulletpoint')

df = pd.read_csv("data.csv",names=['Time','mq4'])
df['Time'] = pd.to_datetime(df['Time'],format=("%H:%M:%S"))
st.dataframe(df)
data=df['mq4']
st.line_chart(data)
st.area_chart(data)
st.bar_chart(data)



#st.dataframe(tws)
st.table(tws)