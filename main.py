from pure import Pure
import streamlit as st
import pandas as pd
import numpy as np
import graphviz as graphviz
import plotly.express as px
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import network_generator 


# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(page_title = 'Dashboard', page_icon = '💯')

pure = Pure()

title, rule = pure.title_and_desc()
st.title(title)
st.markdown(rule,unsafe_allow_html=True)


#pure.account_info()
#HtmlFile = open("profile.html", 'r')
#source_code = HtmlFile.read() 
#components.html(source_code, height = 2000,width=800)


username_input = st.text_input('Enter username',value='stux')

id_searched = pure.get_user_id(username_input)
user_toots_df = pure.get_user_toots(id_searched)
fig2 = px.scatter(user_toots_df, x="toot_time", y="favourites_count", hover_name="username", hover_data=["content", "user_ids"], )
fig2.update_layout(plot_bgcolor = '#0E1117')
st.plotly_chart(fig2)
# except Exception as ex:
#     template = "An exception of type {0} occurred. Arguments:\n{1!r}"
#     message = template.format(type(ex).__name__, ex.args)
#     print (message)



# make Network show itself with repr_html

#def net_repr_html(self):
#  nodes, edges, height, width, options = self.get_network_data()
#  html = self.template.render(height=height, width=width, nodes=nodes, edges=edges, options=options)
#  return html


#df_table = pure.timeline_network()
df_table = pure.followings_network()

@st.cache
def show_network():
    st.title(' Pyvis Network Visualization')
    network_generator.social_net_function(df_table) #pass the dataframe to got_func
    HtmlFile = open("diff_network.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 1200,width=800)



#data_frame = followings_df()
# graph = graphviz.Digraph()
# for a, b in zip(data_frame['Source'].values, data_frame['Target'].values):
#     graph.edge(a, b)
# st.graphviz_chart(graph)