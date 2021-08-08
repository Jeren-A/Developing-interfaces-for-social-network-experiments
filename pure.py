#!/usr/bin/env python3

from mastodon import Mastodon
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
#API_BASE = 'https://dogukankefeli.tech'
class Pure(Mastodon):
    def __init__(self,access_token = 'secrets/usercred.secret',
            api_base_url = 'https://mastodon.social'):
        super().__init__(access_token = 'secrets/usercred.secret',
            api_base_url = 'https://mastodon.social')
    def title_and_desc(self):
        """Gives the title and description for the server"""
        size = 'width="20" height="20"'
        instance_logs = self.instance()
        title = instance_logs['uri']
        note = instance_logs['short_description']
        desc = note[:note.find('/>')]+size+note[note.find('/>'):]
        return title, desc
    
    def get_timeline_users(self):
        """Fetches the timeline toots for unique users at the moment"""
        timeline = self.timeline()
        user = []
        for i in range(len(timeline)):
            user.append(timeline[i]['account']['id'])
        self.unique = np.unique(user)
    
    def create_df(self):
        """Creates a DataFrame of users"""
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

    def get_user_id(self,name):
        """Searches the server for given name and returns the id number of first result""" 
        search_results = self.account_search(name)
        id = search_results[0]['id']
        return id
    
    def get_user_toots(self,id):
        """Returns a dataframe of toots for given user id"""
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


    def timeline_network(self,id=958614):
        
        timeline = self.timeline(limit=200)
        user = {}
        for toot in timeline:
          user[toot['account']['id']] = toot['account']['username']
        source = [] #users
        target = [] #followers

        for key, value in user.items():
          u_follower = self.account_followers(key)
          for k in u_follower:
              source.append(value)
              target.append(k['username'])
        df = pd.DataFrame()
        df['Source'] = source
        df['Target'] = target
        df['Weight'] = 0.1
        return df

    def followings_network(self,id=958614):
        minid=0
        followings = self.account_following(id)
        df = pd.DataFrame(followings)
        more_followings = [followings]
        for _ in range(10):
            minid = df['id'].max()
            followings = self.account_following(149988,min_id=minid)
            more_followings+=followings
            df2 = pd.DataFrame(followings)
            df = df.append(df2,ignore_index=True)
        username = self.account(id)['username']

        
        users={}
        source = [] #users
        target = [] #followers
        color = [] #color for bots
        size = [] #size 
        for following in followings:
            users[following['id']]=following['username']
            source.append(username)
            target.append(following['username'])
            size.append(following['followers_count'])
            if following['bot']==True:
                color.append('#cc0000')
            else:
                color.append('#1f368e')


        for key, value in users.items():
            u_follower = self.account_following(key)
            for k in u_follower:
                source.append(value)
                target.append(k['username'])
                size.append(k['followers_count'])
                if k['bot']==True:
                    color.append('#cc0000')
                else:
                    color.append('#1f368e')
        df = pd.DataFrame()
        df['Source'] = source
        df['Target'] = target
        df['Weight'] = 0.1
        df['Color'] = color
        df['Size'] = size
        df.loc[df['Source']==username,'Weight']=0.2
        return df



    def account_info(self,id=106555351749444654):

        acc_dict = self.account(id)
        smtxt="""
        <html lang="en" ng-app="myApp" class="ng-scope"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><style type="text/css">[uib-typeahead-popup].dropdown-menu{display:block;}</style><style type="text/css">.uib-time input{width:50px;}</style><style type="text/css">[uib-tooltip-popup].tooltip.top-left > .tooltip-arrow,[uib-tooltip-popup].tooltip.top-right > .tooltip-arrow,[uib-tooltip-popup].tooltip.bottom-left > .tooltip-arrow,[uib-tooltip-popup].tooltip.bottom-right > .tooltip-arrow,[uib-tooltip-popup].tooltip.left-top > .tooltip-arrow,[uib-tooltip-popup].tooltip.left-bottom > .tooltip-arrow,[uib-tooltip-popup].tooltip.right-top > .tooltip-arrow,[uib-tooltip-popup].tooltip.right-bottom > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.top-left > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.top-right > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.bottom-left > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.bottom-right > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.left-top > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.left-bottom > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.right-top > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.right-bottom > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.top-left > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.top-right > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.bottom-left > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.bottom-right > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.left-top > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.left-bottom > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.right-top > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.right-bottom > .tooltip-arrow,[uib-popover-popup].popover.top-left > .arrow,[uib-popover-popup].popover.top-right > .arrow,[uib-popover-popup].popover.bottom-left > .arrow,[uib-popover-popup].popover.bottom-right > .arrow,[uib-popover-popup].popover.left-top > .arrow,[uib-popover-popup].popover.left-bottom > .arrow,[uib-popover-popup].popover.right-top > .arrow,[uib-popover-popup].popover.right-bottom > .arrow,[uib-popover-html-popup].popover.top-left > .arrow,[uib-popover-html-popup].popover.top-right > .arrow,[uib-popover-html-popup].popover.bottom-left > .arrow,[uib-popover-html-popup].popover.bottom-right > .arrow,[uib-popover-html-popup].popover.left-top > .arrow,[uib-popover-html-popup].popover.left-bottom > .arrow,[uib-popover-html-popup].popover.right-top > .arrow,[uib-popover-html-popup].popover.right-bottom > .arrow,[uib-popover-template-popup].popover.top-left > .arrow,[uib-popover-template-popup].popover.top-right > .arrow,[uib-popover-template-popup].popover.bottom-left > .arrow,[uib-popover-template-popup].popover.bottom-right > .arrow,[uib-popover-template-popup].popover.left-top > .arrow,[uib-popover-template-popup].popover.left-bottom > .arrow,[uib-popover-template-popup].popover.right-top > .arrow,[uib-popover-template-popup].popover.right-bottom > .arrow{top:auto;bottom:auto;left:auto;right:auto;margin:0;}[uib-popover-popup].popover,[uib-popover-html-popup].popover,[uib-popover-template-popup].popover{display:block !important;}</style><style type="text/css">.uib-datepicker-popup.dropdown-menu{display:block;float:none;margin:0;}.uib-button-bar{padding:10px 9px 2px;}</style><style type="text/css">.uib-position-measure{display:block !important;visibility:hidden !important;position:absolute !important;top:-9999px !important;left:-9999px !important;}.uib-position-scrollbar-measure{position:absolute !important;top:-9999px !important;width:50px !important;height:50px !important;overflow:scroll !important;}.uib-position-body-scrollbar-measure{overflow:scroll !important;}</style><style type="text/css">.uib-datepicker .uib-title{width:100%;}.uib-day button,.uib-month button,.uib-year button{min-width:100%;}.uib-left,.uib-right{width:100%}</style><style type="text/css">.ng-animate.item:not(.left):not(.right){-webkit-transition:0s ease-in-out left;transition:0s ease-in-out left}</style><style type="text/css">@charset "UTF-8";[ng\:cloak],[ng-cloak],[data-ng-cloak],[x-ng-cloak],.ng-cloak,.x-ng-cloak,.ng-hide:not(.ng-hide-animate){display:none !important;}ng\:form{display:block;}.ng-animate-shim{visibility:hidden;}.ng-anchor{position:absolute;}</style>
        """
        full_text = """
          <base href="/">
          <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
          <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
          <link rel="stylesheet" href="https://botometer.osome.iu.edu/static/app.css">
        </head>
        <body>
            <div role="main" class="container">
                <!-- ngView: --><div ng-view="" class="ng-scope"><h1 class="user-detail-screen-name ng-binding ng-scope">
              @{username}
              <icon-verified user="user" class="ng-isolate-scope"><!-- ngIf: user.userData.verified --></icon-verified>
            </h1>
            <a class="user-detail-profile-link ng-scope" ng-href="https://mastodon.social/@{username}" href="https://mastodon.social/@{username}" target="_blank">
              <i class="glyphicon glyphicon-user"></i>
            </a>
            <div class="user-detail-banner-container ng-scope">
              <img style=" max-height: 200px; max-width: 100%;" ng-src="{header_static}" src="{header_static}">
              <img style="height: 75px;width: 75px;  margin-right: 10px;border: 3px solid white; position: absolute; top: 70px; left: 40px; border-radius: 50%" ng-src="{avatar_static}" src="{avatar_static}">
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
                  <dt>URL</dt>
                  <dd><a href="{url}">{url}</a></dd>
                </dl>
              </div>
              <div class="col-sm-4">
                <dl class="dl-horizontal">
                  <dt>Toots</dt>
                  <dd class="ng-binding">{statuses_count}</dd>
                  <dt>Following</dt>
                  <dd class="ng-binding">{following_count}</dd>
                  <dt>Followers</dt>
                  <dd class="ng-binding">{followers_count}</dd>
                </dl>
              </div>
            </div>
        <dl class="dl-horizontal ng-scope">
            <dt>Mastodon user ID</dt>
            <dd class="ng-binding">{id}</dd>
        </dl>
        </div>
          </div>
        """.format(id=acc_dict['id'],header_static=acc_dict['header_static'],avatar_static=acc_dict['avatar_static'],username=acc_dict['username'],display_name=acc_dict['display_name'],note=acc_dict['note'],url=acc_dict['url'],statuses_count=acc_dict['statuses_count'],following_count=acc_dict['following_count'],followers_count=acc_dict['followers_count'])

        Html_file = open("profile.html","w",encoding="utf-8")
        Html_file.write(full_text)
        Html_file.close()