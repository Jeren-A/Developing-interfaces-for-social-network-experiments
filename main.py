
from mastodon_api import Pure
import streamlit as st
import pandas as pd
import numpy as np
from web_scraping import get_tw
import plotly.express as px



# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(page_title = 'Dashboard', page_icon = '💯')


pure = Pure()
title, rule = pure.title_and_rule()
st.title(title)
st.markdown(rule)
pure.get_timeline_users()
df1 = pure.create_df()
#st.table(df1)
st.dataframe(df1)





fig = px.scatter(df1, x="toot_time", y="favourites_count", hover_name="usernames", hover_data=["content", "user_ids"], )
fig.update_layout(plot_bgcolor = '#0E1117')


st.plotly_chart(fig)
<<<<<<< HEAD
#BURADAAA
# import PyPDF2
# import numpy as np
# import time 

# pdfFileObj = open('book.pdf', 'rb')
 
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# pageObj = pdfReader.getPage(np.random.randint(0,968))

# try:
#     text = pageObj.extractText().split('\n')
#     text2 = text[np.random.randint(len(text)-3):np.random.randint(len(text)-3)+3]
#     text3 = " ".join(text2)
#     text3
# except:
#     pass

=======
>>>>>>> 0e88e4ca1c4f45e4ac491f010fab1de46f2eadf4

