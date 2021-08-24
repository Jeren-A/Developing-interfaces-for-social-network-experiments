# Hacking Mastobot

This document is a WIP draft, and will be enriched after a certain degree of community contribution. It assumes you have read the README.

## Reading code

The entry point from which you should begin reading Mastobot code is `mastobot/__main__.py`. It contains the class `Bot`, the primary foundation of Mastobot. Let's skim through its outline.

```python
class Bot:
    def __init__()
    def _check_triggers()
    def _respond()

    # decorator generators
    def on_mention()
    def on_home_update()

    # execution
    def run()
```

**Note**: By convention, everything prefixed with a single underline (`_`) is internal to its class, shouldn't be accessed by the bot developer, but is still accessible from the outside if you really want.

### Fundamental trigger mechanism

A `Bot` instance has an attribute `_triggers` (ref: `__init__`). It is a list of `Trigger` instances (ref: `trigger.py`). A `Trigger` instance, let's say `trig`, carries an action or a series thereof that will be taken when an expected event occurs. To put it the techie way, it invokes a callback when an event positively matches its expectation.

The `Bot` is set up to listen to the [user stream](https://mastodonpy.readthedocs.io/en/stable/#mastodon.Mastodon.stream_user). Whenever a new event whatsoever is received, it iterates through `_triggers`, calling each `trig.test(event, content)`. If `True` is returned, it invokes `trig.invoke(obj)` where obj is the dict object from Mastodon.py (ref: `_check_triggers`). Then, the returned value of `trig.invoke(obj)` is typically replied to the status concerned, a procedure you should have gotten familiar with in the README (ref: `_respond`). Or it might be a fav, or it might be a boost, or it might be a list of reactions to the toot. Once responded, a trigger cycle is complete.

## WIP: trigger.py and structs.py
