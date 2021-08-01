
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
import got 


# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(page_title = 'Dashboard', page_icon = '💯')

pure = Pure()

title, rule = pure.title_and_desc()
st.title(title)
st.markdown(rule,unsafe_allow_html=True)


@st.cache(suppress_st_warning=True)
def account_info(id=106555351749444654):
    acc_dict = pure.account(id)
    styling ="""<head>
    <style type="text/css">.uib-position-measure{display:block !important;visibility:hidden !important;position:absolute !important;top:-9999px !important;left:-9999px !important;}.uib-position-scrollbar-measure{position:absolute !important;top:-9999px !important;width:50px !important;height:50px !important;overflow:scroll !important;}.uib-position-body-scrollbar-measure{overflow:scroll !important;}</style>
    <style type="text/css">.ng-animate.item:not(.left):not(.right){-webkit-transition:0s ease-in-out left;transition:0s ease-in-out left}</style>
    <style type="text/css">@charset "UTF-8";[ng\:cloak],[ng-cloak],[data-ng-cloak],[x-ng-cloak],.ng-cloak,.x-ng-cloak,.ng-hide:not(.ng-hide-animate){display:none !important;}ng\:form{display:block;}.ng-animate-shim{visibility:hidden;}.ng-anchor{position:absolute;}</style>
    <link rel="stylesheet" href="/static/app.css">
    </head>
    """
    table = """
    <div role="main" class="container">
        <!-- ngView: --><div ng-view="" class="ng-scope"><h1 class="user-detail-screen-name ng-binding ng-scope">
      @dogukanburda
      <icon-verified user="user" class="ng-isolate-scope"><!-- ngIf: user.userData.verified --></icon-verified>
    </h1>
    <a class="user-detail-profile-link ng-scope" ng-href="https://mastodon.social/web/accounts/{id}" href="https://mastodon.social/web/accounts/{id}">
      <i class="glyphicon glyphicon-user"></i>
    </a>
    <div class="user-detail-banner-container ng-scope">
      <img class="user-detail-banner-img" ng-src="{header_static}" src="{header_static}">
      <img class="user-detail-profile-img img-circle" ng-src="{avatar_static}" src="{avatar_static}">
    </div>
    <div class="row ng-scope">
      <div class="col-sm-8 col-md-6">
        <dl class="dl-horizontal">
          <dt>Screen name</dt>
          <dd ng-show="user.userData" class="ng-binding">@{username}</dd>
          <dt>Display name</dt>
          <dd class="ng-binding">{display_name}</dd>
          <dt>Description</dt>
          <dd class="ng-binding">{note}</dd>
        </dl>
      </div>
      <div class="col-sm-4">
        <dl class="dl-horizontal">
          <dt>Tweets</dt>
          <dd class="ng-binding">{statuses_count}</dd>
          <dt>Following</dt>
          <dd class="ng-binding">{following_count}</dd>
          <dt>Followers</dt>
          <dd class="ng-binding">{followers_count}</dd>
        </dl>
      </div>
    </div>
    """.format(id=acc_dict['id'],header_static=acc_dict['header_static'],avatar_static=acc_dict['avatar_static'],username=acc_dict['username'],display_name=acc_dict['display_name'],note=acc_dict['note'],statuses_count=acc_dict['statuses_count'],following_count=acc_dict['following_count'],followers_count=acc_dict['followers_count'])
    return table
    
div_string = account_info()
st.markdown(div_string,unsafe_allow_html=True)


try:
    username_input = st.text_input('Enter username2',key='3696216')
    display_toots(username_input)
except:
    pass
try:
    id_searched = pure.get_user_id(username_input)
    user_toots_df = pure.get_user_toots(id_searched)
    fig2 = px.scatter(user_toots_df, x="toot_time", y="favourites_count", hover_name="usernames", hover_data=["content", "user_ids"], )
    fig2.update_layout(plot_bgcolor = '#0E1117')
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
  pure = Pure()
  timeline = pure.timeline(limit=200)
  user = {}
  for toot in timeline:
      user[toot['account']['id']] = toot['account']['username']
  
  source = [] #users
  target = [] #followers
  
  for key, value in user.items():
      u_follower = pure.account_followers(key)
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

