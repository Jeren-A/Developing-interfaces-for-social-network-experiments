from re import A
from mastodon import Mastodon
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
class Pure:
    def __init__(self):
        self.data= Mastodon(
            access_token = 'pytooter_clientcred.secret',
            api_base_url = 'https://dogukankefeli.tech')
        self.unique = []

    def title_and_rule(self):
        instance_logs = self.data.instance()
        title = instance_logs['uri']
        rule = instance_logs['rules'][0]['text']
        return title, rule
    
    def get_timeline_users(self):
        timeline = self.data.timeline()
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
            statuses = self.data.account_statuses(user)
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
        search_results = self.data.account_search(name2)
        id = search_results[0]['id']
        return id
    
    def get_user_toots(self,id):
        usernames = []
        user_ids = []
        toot_ids = []
        toot_time = []
        toot_favourites_count = []
        content = []
        statuses = self.data.account_statuses(id,limit=100)
        for toot in statuses:
            user_ids.append(id)
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