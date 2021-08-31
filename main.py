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
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def show_network(df_table):
    st.title('Diffusion Network Visualization')
    network_generator.social_net_function(df_table) #pass the dataframe to got_func
    HtmlFile = open("diff_network.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 1400,width=1000)
# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(page_title = 'Dashboard', page_icon = '💯',layout="wide")

radio_select = st.sidebar.radio(  #options menu
    "Show:",
    ('User Toots','User Profile','Diffusion Netwok', 'Word Cloud'))
def toots_graphs(id=149988):
    import altair as alt
    import pandas as pd
    df = pure.get_user_toots(id) #get user toots
    df_toottime = df.groupby([df['toot_time'].dt.date]).count() #groupby datetime.days

    df_toottime.index = pd.to_datetime(df_toottime.index) #convert index string to datetime obj
    df_toottime.drop(columns=['toot_time'],inplace=True) #drop existing 'toot_time' columns
    df_toottime.reset_index(inplace=True) #make toot_time date acccesible 

    df_toottime['DoW'] = df_toottime['toot_time'].dt.day_name() #create new columns for day of the week

    cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] #categorical dow
    df_toottime['DoW'] = pd.Categorical(df_toottime['DoW'], categories=cats, ordered=True)
    df_toottime = df_toottime.sort_values('DoW') #sort by days
    df_hist = df_toottime.groupby([df_toottime['DoW']]).count() #count how many toots in days

    df_hist.reset_index(inplace=True)

    # Toots by day of week 
    alt_dow = alt.Chart(df_hist).mark_bar().encode(
    alt.X('DoW', title='Day',sort=None),
        alt.Y('username', title='Toot Counts'),
        color=alt.Color('DoW', sort=['GOOG'])).properties(width=500).interactive()

    # Toots timeseries
    alt_timeseries = alt.Chart(df_toottime).mark_bar(size=12).encode(
    alt.X('toot_time:T', title='Day'),
        alt.Y('username', title='Toot Counts'),
    color='DoW').properties(width=500).interactive()

    return alt_dow,alt_timeseries

pure = Pure()

title, rule = pure.title_and_desc()
st.title(title)
st.markdown(rule,unsafe_allow_html=True)


#pure.account_info()
#HtmlFile = open("profile.html", 'r')
#source_code = HtmlFile.read() 
#components.html(source_code, height = 2000,width=800)
def word_cloud(text):
    text = text.lower()
    stopwords = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"}
    mask = np.array(Image.open('img/mmm.png'))
    wordcl = WordCloud(stopwords=stopwords, background_color='white', mask=mask, mode='RGB', 
             max_words=3000, width=1600, height=800, max_font_size=120, random_state=1).generate(text)
    image = wordcl.to_image()
    st.image(image, width=None)

if radio_select=='User Toots':
    st.title('User Toots')
    username_input = st.text_input('Enter username',value='stux')
    if not username_input:
        st.warning('Please input a name.')
        st.stop()
        st.success('Thank you for inputting a name.')
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

elif radio_select=='Diffusion Netwok':
    st.title('Diffusion Netwok')
    username_input = st.text_input('Enter username')
    if not username_input:
        st.warning('Please input a name.')
        st.stop()
        st.success('Thank you for inputting a name.')
    id_of_user = pure.get_user_id(username_input)
    df_table = pure.followings_network(id=id_of_user)
    st.balloons()
    show_network(df_table)


elif radio_select=='User Profile':
    st.title('User Profile')
    username_input = st.text_input('Enter username')
    if not username_input:
        st.warning('Please input a name.')
        st.stop()
        st.success('Thank you for inputting a name.')
    id_of_user = pure.get_user_id(username_input)
    pure.account_info(id_of_user)
    HtmlFile = open("profile.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600,width=1000)
    alt_day_ot_week, alt_timelinegraph = toots_graphs(id_of_user)

    col1, col2 = st.columns(2)

    with col1:
        st.header("Toots by day of week")
        st.altair_chart(alt_day_ot_week,use_container_width=True)

    with col2:
        st.header("Toots timeseries")
        st.altair_chart(alt_timelinegraph,use_container_width=True)

elif radio_select=='Word Cloud':
    text = pure.toots_text()
    st.title("Word Cloud")
    word_cloud(text)




    # st.altair_chart(alt_day_ot_week,use_container_width=True)
    # st.altair_chart(alt_timelinegraph,use_container_width=True)







    #col1, col2 = st.columns(2)
    #col1.subheader('Toots by day of the week')
    #col1.altair_chart(alt_day_ot_week,use_container_width=True)
    #col2.subheader('Toot counts by day')
    #col2.altair_chart(alt_timelinegraph,use_container_width=True)
#data_frame = followings_df()
# graph = graphviz.Digraph()
# for a, b in zip(data_frame['Source'].values, data_frame['Target'].values):
#     graph.edge(a, b)
# st.graphviz_chart(graph)

