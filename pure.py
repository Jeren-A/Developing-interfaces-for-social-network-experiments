#!/usr/bin/env python3

from mastodon import Mastodon, StreamListener


API_BASE = 'https://dogukankefeli.tech'


def login():
    global mastodon
    mastodon = Mastodon(client_id='secrets/clientcred.secret',access_token = 'secrets/usercred.secret',api_base_url = 'https://dogukankefeli.tech')

login()
print(mastodon.instance())