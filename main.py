
from mastodon_api import Pure
import streamlit as st
import pandas as pd
import numpy as np
from web_scraping import get_tw
import plotly.express as px



def display_toots(username_input):
    id_searched = pure.get_user_id(username_input)
    user_toots_df = pure.get_user_toots(id_searched)
    st.markdown("User's toots")
<<<<<<< HEAD
    st.dataframe(user_toots_df)
=======
    st.dataframe(user_toots_df[['toot_time','content','favourites_count']])
>>>>>>> 208d190fc8034391c6b4680eb375f7739cc19d0e
 
# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(page_title = 'Dashboard', page_icon = '💯')


pure = Pure()
title, rule = pure.title_and_rule()
st.title(title)
st.markdown(rule)

try:
    username_input = st.text_input('Enter username',key='Enter a username')
    display_toots(username_input)
except:
    pass
try:
    id_searched = pure.get_user_id(username_input)
    user_toots_df = pure.get_user_toots(id_searched)
    fig2 = px.scatter(user_toots_df, x="toot_time", y="favourites_count", hover_name="usernames", hover_data=["content", "user_ids"], )
<<<<<<< HEAD
    fig2.update_layout(plot_bgcolor = '#0E1117')
    st.plotly_chart(fig2)
except:
    pass


"""
pure.get_timeline_users()
df1 = pure.create_df()
#st.table(df1)
st.dataframe(df1)





fig = px.scatter(df1, x="toot_time", y="favourites_count", hover_name="usernames", hover_data=["content", "user_ids"], )
fig.update_layout(plot_bgcolor = '#0E1117')


st.plotly_chart(fig)
"""
=======
    fig2.update_layout(plot_bgcolor = '#CCCCCC')
    st.plotly_chart(fig2)
except Exception as ex:

    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print (message)
>>>>>>> 208d190fc8034391c6b4680eb375f7739cc19d0e
