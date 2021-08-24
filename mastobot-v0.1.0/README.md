# Mastobot - cheap mastodon bots

## Important

Nothing in this project is set in stone except that it's for cheap bots only. Consider your use cases before adopting this library (consult [§Use cases](#use-cases)). Mastobot is suitable for bots which do not require intensive interaction, e.g. media or polls. Just write your own bot from scratch if you want juicy features. It also aims to be beginner-friendly, even (especially) those who don't understand decorators. You're welcome to contribute if you do (see HACKING.md).

## Why

Here is a code excerpt, using the stock Mastodon.py library, which is undoubtedly amazing but somewhat painful to write clean code with.

```python
class Listener(StreamListener):
    def on_notification(self, ntf):
        if ntf["type"] == "mention":
            content = html_to_text(ntf["status"]["content"])
            req = content.split(" ")[1]
            if content.startswith("GET "):
                masto.status_reply(ntf["status"], get(req))
            elif content.startswith("POST "):
                masto.status_reply(ntf["status"], post(req))
            elif content.startswith("DELETE "):
                masto.status_favourite(ntf["status"]["id"])
        # ... and everything else.

listener = Listener()
mastodon.stream_user(listener)
```

See, as attempts are made to expand the amount of event handlers, complexity quickly accumulates. Mastobot exists to get rid of this problem. Instead, you can save yourself from this cloggy syntax and spaghetti-prone code structure with Mastobot, because it takes care of listener registration and event handling, allowing bot devs to build modularized 2nd-level (1 level of indent) blocks of code. Moreover, Mastobot wraps awkward Mastodon.py dict objects into fancy `NamedTuples`, which grants you the power to access attributes via dots (`obj.attr`), not brackets and quoted strings (`obj["attr"]`). See? Three (3) characters saved!

## Examples

### Basic usage

```python
from mastobot import Bot
bot = Bot(
    instance_url="https://mastodon.instance",
    access_token="your_access_token",
)

@bot.on_mention("hi")
def respond_to_hi(status):
    name = status.account.username
    return f"hey, {name}!"

bot.run()
```

In this example, if a user sends the bot "hi", the bot will reply with "hey, {the user's name (handle without instance domain)}!".

### Advanced usage

```python
from mastobot import *
import re
bot = Bot(
    instance_url="https://mastodon.instance",
    access_token="your_access_token",
)

def looks_like_brainsize_meme(content: str):
    lines = content.splitlines()
    brain_count = 0
    for ln in lines:
        if re.match("^:brain[0-9]+:", ln):
            count += 1

    if brain_count > 2:
        # looks like brainsize meme
        return True

    return False

# if looks_like_brainsize_meme(status_dict["content"]) == True,
# invoke compliment_meme
@bot.on_home_update(looks_like_brainsize_meme, validation=EVALUATE)
def compliment_meme(status):
    return [
            Boost,
            Favourite,
            Reply("brilliant meme!", visibility=PRIVATE),
        ]

# invoke when re.search("(:hacker_[a-z]:\s)+", status_dict["content"]) is not None
@bot.on_home_update("(:hacker_[a-z]:\s)+", validation=REGEX)
def nice_hacker_font(status):
    return Reply("nice hacker font you have", visibility=DIRECT)

bot.run()
```

In this one, it will favboost and reply "brilliant meme!" to a post on its home timeline that resembles a brainsize meme.

## Installation

It's not on PyPI yet. Mastobot is such a good name, it took me eight seconds to come up with it. I anticipate that it will be, soon.

### Install via setuptools

Clone and cd into this repo, `python setup.py install --user`.

## Use cases

Use Mastobot when:

- Your bot replies to or interacts with certain posts on its home timeline; or
- Your bot answers some questions people ask it; or
- Your bot keeps track of some users it's following.

Think of mastobot as a web server. It takes input, catches certain routes, and gives output. Similarly, bots made with mastobot will be able to listen to events and trigger some actions when a certain event occurs.

Don't use Mastobot when:

- It is merely a shitpost bot who posts hourly, daily, etc. Use a cron job instead.
- You need to post images or other media. Too fancy. Write your own.
- You want to harass users. No substitute. Simply don't.

## Terminology

I try to keep my terms consistent. Here is a table of them.

| Term (in descending order of priority) | Definition                                                                                                                 |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| status/post/toot                       | self-explanatory                                                                                                           |
| reply                                  | a status that is a reply to another                                                                                        |
| reblog/boost                           | an action that reposts a status                                                                                            |
| favourite/fav                          | a self-explanatory action                                                                                                  |
| response                               | a reply, boost, or favourite                                                                                               |
| account/acct                           | an identity registered on mastodon or other fediverse backend with a distinct `user@instance` handle                       |
| user                                   | a real person or organization who owns and operates an account                                                             |
| bot developer/botdev                   | a real person or organization who has made a mastodon bot with mastobot                                                    |
| the bot                                | an application that the bot developer has made, designated a mastodon account for, and deployed                            |
| notification/notif                     | an event sent from mastodon concerning the bot                                                                             |
| mention                                | an account addressed (@) in a status; or a notification addressed to the bot containing a status sent from another account |
| timeline/TL                            | a stream of statuses visible to the bot, incl. home, local, and public(federated)                                          |
| update                                 | a new status visible to the bot on a timeline                                                                              |
