from mastodon import Mastodon, StreamListener
from .html_text import html_to_text
from .structs import *
from .trigger import Trigger
from .constants import *

# related documentation: https://mastodonpy.readthedocs.io/en/stable/#


class Bot:
    def __init__(self, instance_url: str, access_token: str):
        """Intiate a Mastodon bot.

        :param instance_url: (str) base URL for your Mastodon instance of choice,
            e.g. ``https://mastodon.technology``.
        :param access_token: (str) "Your access token" inside
            Preferences -> Development -> some application.
        """
        self._instance = instance_url
        self._token = access_token
        self._handle = ""  # will be like "bot@instance.tld"
        self._atname = ""  # will be like "@bot"
        self._triggers = []
        self._check_update_triggers = lambda o: self._check_triggers(o, UPDATE)
        self._check_notification_triggers = lambda o: self._check_triggers(
            o, NOTIFICATION
        )

    def _check_triggers(self, obj: dict, stream: str):
        """Handle events from ``mastodon.StreamListener.on_update()`` if 
            ``stream=="update"``, and ``mastodon.StreamListener.on_notification()``
            if ``stream=="notification"``.
        """
        # set up expectations
        if stream == UPDATE:
            status = obj
            event = UPDATE
        elif stream == NOTIFICATION:
            status = obj["status"]
            event = obj["type"]
        else:
            return

        # if the bot is mentioned, remove the mention text from status content
        # before testing trigger
        mentioned_accts = [m["acct"] for m in status["mentions"]]
        if self._handle in mentioned_accts:
            to_be_removed = self._atname
        else:
            to_be_removed = ""

        for trig in self._triggers:
            if not trig.event == event:
                continue
            if trig.test(
                event,
                html_to_text(status["content"]).replace(to_be_removed, "", 1).strip(),
            ):
                # pass obj to trig. trig will decide which elements
                # to pass on to bot-developer-defined callback.
                reply = trig.invoke(obj)
                if reply:
                    self._respond(status, reply)

    def _respond(self, status: dict, content):
        """Reply to a status with content, boost, or favourite it.

        :param status: (dict) the status to respond to.
        :param content: When ``content`` is a string,
            simply reply with it, keeping everything else as Mastodon.py decides.
            When it is an instance of the ``mastobot.Reply`` class, all its arguments
            will be passed on to Mastodon.py. The rest are left in their default state.
            When it is ``mastobot.Boost``, boost ``status``. Ditto for ``Favourite``.
            When it is a list/tuple, recursively call ``self._respond(status, n)``
            for each ``n`` in content.
        """
        if not content:
            raise ValueError(f"Response to {status['id']} empty; aborted")

        if type(content) in (list, tuple):
            for n in content:
                self._respond(status, n)
            return
        elif content == Boost:
            self._bot.status_reblog(status["id"])
            return
        elif content == Favourite:
            self._bot.status_favourite(status["id"])
            return
        elif type(content) == str:
            args = {
                STATUS: content,
                SENSITIVE: status[SENSITIVE],
                VISIBILITY: status[VISIBILITY],
                SPOILER_TEXT: status[SPOILER_TEXT],
            }
        elif isinstance(content, Reply):
            args = {
                STATUS: content.text,
                VISIBILITY: content.visibility or status[VISIBILITY],
                SPOILER_TEXT: content.spoiler_text or status[SPOILER_TEXT],
            }

        self._bot.status_reply(to_status=status, **args)

    # decorator generators

    def on_mention(self, expectation, validation=EQUALS, case_sensitive=False):
        """Listen to mentions and invoke a callback with a ``Status`` object
            as argument.

        :param expectation: (str or callable) string, regex string or callable
            that evaluates to True if the status content is what you want.
        :param validation: (str) may be "equals", "contains", "regex" or "evaluate".
        """

        def decorator(callback):
            self._triggers.append(
                Trigger(
                    event=MENTION,
                    validation=validation,
                    expectation=expectation,
                    callback=callback,
                    case_sensitive=case_sensitive,
                )
            )

        return decorator

    def on_home_update(self, expectation, validation=EQUALS, case_sensitive=False):
        """Listen to updates on the home timeline and invoke a callback with
            a ``Status`` object as argument.

        :param expectation: (str or callable) string, regex string or callable
            that evaluates to True if the status content is what you want.
        :param validation: (str) may be "equals", "contains", "regex" or "evaluate".
        """

        def decorator(callback):
            self._triggers.append(
                Trigger(
                    event=UPDATE,
                    validation=validation,
                    expectation=expectation,
                    callback=callback,
                    case_sensitive=case_sensitive,
                )
            )

        return decorator

    # execution

    def run(self):
        """Start bot.

        After all listeners (triggers) are set, invoke ``bot.run()``.
        """
        self._bot = Mastodon(api_base_url=self._instance, access_token=self._token)
        print("Connected to " + self._instance)

        # keep a record of what this bot is called
        # so that "@atname" can be removed when necessary.
        me = self._bot.account_verify_credentials()
        self._handle = me["acct"]
        self._atname = "@" + me["username"]

        # register stream listeners
        self._user_stream = StreamListener()
        self._user_stream.on_update = self._check_update_triggers
        self._user_stream.on_notification = self._check_notification_triggers
        self._bot.stream_user(self._user_stream)
