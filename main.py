
from mastodon_api import Pure
import streamlit as st
import pandas as pd
import numpy as np
import graphviz as graphviz
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
    username_input = st.text_input('Enter username2',key='3696216')
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

def follow_df():


  from mastodon import Mastodon

  mastodon = Mastodon(
      client_id = 'pytooter_clientcred.secret',
      api_base_url = 'https://dogukankefeli.tech'
  )
  mastodon.log_in(
      'dogukankefeli@gmail.com',
      '9a65202322deed907dd86175d27aa66c',
      to_file = 'pytooter_usercred.secret'
  )
  
  timeline = mastodon.timeline(limit=200)
  user = {}
  for toot in timeline:
      user[toot['account']['id']] = toot['account']['username']
  
  source = [] #users
  target = [] #followers
  
  for key, value in user.items():
      u_follower = mastodon.account_followers(key)
      for k in u_follower:
          source.append(value)
          target.append(k['username'])
  df = pd.DataFrame()
  df['Source'] = source
  df['Target'] = target
  df['Weight'] = 1
  return df

data_frame = follow_df()
graph = graphviz.Digraph()
for a, b in zip(data_frame['Source'].values, data_frame['Target'].values):
    graph.edge(a, b)
st.graphviz_chart(graph)