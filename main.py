
import streamlit as st
import pandas as pd
import numpy as np
from web_scraping import get_tw

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

# LOADING DATA
DATE_TIME = "date/time"
DATA_URL = (
    "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data

dict1 = get_tw()
tws = pd.DataFrame.from_dict(dict1,orient='index')

data = load_data(100000)


#st.dataframe(data)
st.dataframe(tws)
st.table(tws)