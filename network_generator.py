import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
from pure import Pure

pure = Pure()

def social_net_function(social_data):
  social_net = Network(height="600px", width="100%")

# set the physics layout of the network
  social_net.barnes_hut()
  sources = social_data['Source']
  targets = social_data['Target']
  weights = social_data['Weight']
  color = social_data['Color']
  size = social_data['Size']
  #size = [float(i)/max(size) for i in size]*

  edge_data = zip(sources, targets, weights, color, size)

  for e in edge_data:
    src = e[0]
    dst = e[1]
    w = e[2]
    c = e[3]
    s = e[4]
    social_net.add_node(src, src, title=src ,color=c, size=s)
    social_net.add_node(dst, dst, title=dst ,color=c, size=s)
    social_net.add_edge(src, dst, value=w)

  neighbor_map = social_net.get_adj_list()

# add neighbor data to node hover data
  for node in social_net.nodes:
    node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
    node["value"] = len(neighbor_map[node["id"]])
  social_net.show("diff_network.html")
  

def simple_func(physics): 
  nx_graph = nx.cycle_graph(10)
  nx_graph.nodes[1]['title'] = 'Number 1'
  nx_graph.nodes[1]['group'] = 1
  nx_graph.nodes[3]['title'] = 'I belong to a different group!'
  nx_graph.nodes[3]['group'] = 10
  nx_graph.add_node(20, size=20, title='couple', group=2)
  nx_graph.add_node(21, size=15, title='couple', group=2)
  nx_graph.add_edge(20, 21, weight=5)
  nx_graph.add_node(25, size=25, label='lonely', title='lonely node', group=3)


  nt = Network("500px", "500px",notebook=True,heading='')
  nt.from_nx(nx_graph)
  #physics=st.sidebar.checkbox('add physics interactivity?')
  nt.show('test.html')


def karate_func(physics): 
  G = nx.karate_club_graph()


  nt = Network("500px", "500px",notebook=True,heading='Zachary’s Karate Club graph')
  nt.from_nx(G)

  nt.show('karate.html')
