<<<<<<< HEAD
from mastodon import Mastodon

mastodon = Mastodon(
    client_id = 'pytooter_clientcred.secret',
    api_base_url = 'https://dogukankefeli.tech'
)
mastodon.log_in(
    'dogukankefeli@protonmail.com',
    '20bad20e27a864a705234e4839fb77c1',
    to_file = 'pytooter_usercred.secret'
)
=======
from mastodon import Mastodon

mastodon = Mastodon(
    client_id = 'pytooter_clientcred.secret',
    api_base_url = 'https://dogukankefeli.tech'
)
mastodon.log_in(
    'dogukankefeli@protonmail.com',
    '20bad20e27a864a705234e4839fb77c1',
    to_file = 'pytooter_usercred.secret'
)
>>>>>>> 58f19f69fc2e9677f00dc0687c7bb13141e9827e
mastodon.toot('xdd')