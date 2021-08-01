#!/usr/bin/env python3

from mastodon import Mastodon, StreamListener
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
#API_BASE = 'https://dogukankefeli.tech'
class Pure(Mastodon):
    def __init__(self):
        Mastodon.__init__(self,access_token = 'secrets/usercred.secret',
            api_base_url = 'https://mastodon.social')
    def title_and_desc(self):
        size = 'width="20" height="20"'
        instance_logs = self.instance()
        title = instance_logs['uri']
        note = instance_logs['short_description']
        desc = note[:note.find('/>')]+size+note[note.find('/>'):]
        return title, desc
    
    def get_timeline_users(self):
        timeline = self.timeline()
        user = []
        for i in range(len(timeline)):
            user.append(timeline[i]['account']['id'])
        self.unique = np.unique(user)
    
    def create_df(self):
        user_ids = []
        usernames = []
        toot_ids = []
        toot_time = []
        toot_favourites_count = []
        content = []
        for user in self.unique:
            statuses = self.account_statuses(user)
            for toot in statuses:
                user_ids.append(toot['account']['id'])
                usernames.append(toot['account']['username'])
                toot_ids.append(toot['id'])
                toot_time.append(toot['created_at'])
                toot_favourites_count.append(toot['favourites_count'])
                soup = BeautifulSoup(toot['content'],features="lxml")
                content.append(soup.get_text())
        data = {}
        data['user_ids'] = user_ids
        data['usernames'] = usernames
        data['toot_ids'] = toot_ids
        data['toot_time'] = toot_time
        data['favourites_count'] = toot_favourites_count
        data['content']=content
        df = pd.DataFrame(data)
        return df

    def get_user_id(self,name2):
        search_results = self.account_search(name2)
        id = search_results[0]['id']
        return id
    
    def get_user_toots(self,id):
        username = []
        user_ids = []
        toot_ids = []
        toot_time = []
        toot_favourites_count = []
        content = []
        statuses = self.account_statuses(id,limit=40)
        for toot in statuses:
            user_ids.append(id)
            username.append(toot['account']['username'])
            toot_ids.append(toot['id'])
            toot_time.append(toot['created_at'])
            toot_favourites_count.append(toot['favourites_count'])
            soup = BeautifulSoup(toot['content'],features="lxml")
            content.append(soup.get_text())
        data = {}
        data['user_ids'] = user_ids
        data['username'] = username
        data['toot_ids'] = toot_ids
        data['toot_time'] = toot_time
        data['favourites_count'] = toot_favourites_count
        data['content']=content
        df = pd.DataFrame(data)
        return df
    def account_info(self,id=106555351749444654):
        return self.account(id)