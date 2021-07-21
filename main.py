
from mastodon_api import Pure
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
  
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import got 


def display_toots(username_input):
    id_searched = pure.get_user_id(username_input)
    user_toots_df = pure.get_user_toots(id_searched)
    st.markdown("User's toots")
    st.dataframe(user_toots_df[['toot_time','content','favourites_count']])
 
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
    fig2.update_layout(plot_bgcolor = '#CCCCCC')
    st.plotly_chart(fig2)
except Exception as ex:
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print (message)

st.title(' Pyvis Network Visualization')
# make Network show itself with repr_html

#def net_repr_html(self):
#  nodes, edges, height, width, options = self.get_network_data()
#  html = self.template.render(height=height, width=width, nodes=nodes, edges=edges, options=options)
#  return html

physics=False
#physics=st.sidebar.checkbox('add physics interactivity?')

got.got_func(physics)

HtmlFile = open("gameofthrones.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height = 1200,width=800)
