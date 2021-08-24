from typing import NamedTuple
from datetime import datetime
from .constants import *

"""bot-dev-constructed objects"""


class Reply:
    """Helper class to be constructed by the bot developer.
        Avoids quirky dict syntax because ``reply.key``
        is so much more succint than ``dict["key"]``.
    """

    def __init__(self, text: str, visibility=None, spoiler_text=None):
        if not text:
            raise ValueError("Argument `text` cannot be empty")
        self.text = str(text)

        if not visibility in VISIBILITY_LIST + [None]:
            raise ValueError(
                "Argument `visibility` must be one of "
                "'public', 'unlisted', 'private', or 'direct'"
            )
        self.visibility = visibility

        self.spoiler_text = spoiler_text


# return Boost or return Favourite in callbacks
Boost = object()
Favourite = object()

"""mastobot objects provided for bot dev"""

Mention = NamedTuple(
    "Account", [("id", int), ("username", str), ("acct", str), ("url", str)]
)

Account = NamedTuple(
    "Account",
    [
        ("id", int),
        ("username", str),
        ("acct", str),
        ("display_name", str),
        ("url", str),
        ("avatar", str),
        ("avatar_static", str),
        ("bot", bool),
    ],
)

Status = NamedTuple(
    "Status",
    [
        ("id", int),
        ("url", str),
        ("account", Account),
        ("in_reply_to_id", int),
        ("content", str),
        ("created_at", datetime),
        ("sensitive", bool),
        ("spoiler_text", str),
        ("visibility", str),
        ("mentions", list),
    ],
)

Notification = NamedTuple(
    "Notification",
    [
        ("id", int),
        ("type", str),
        ("created_at", datetime),
        ("account", Account),
        ("status", Status),
    ],
)


def gen_status(obj: dict) -> Status:
    """Dict to NamedTuple utility.

    :param obj: (dict) mastodon.py status dict.
    """
    return Status(
        id=obj["id"],
        url=obj["url"],
        account=Account(
            id=obj["account"]["id"],
            username=obj["account"]["username"],
            acct=obj["account"]["acct"],
            display_name=obj["account"]["display_name"],
            url=obj["account"]["url"],
            avatar=obj["account"]["avatar"],
            avatar_static=obj["account"]["avatar_static"],
            bot=obj["account"]["bot"],
        ),
        in_reply_to_id=obj["in_reply_to_id"],
        content=obj["content"],
        created_at=obj["created_at"],
        sensitive=obj[SENSITIVE],
        spoiler_text=obj[SPOILER_TEXT],
        visibility=obj[VISIBILITY],
        mentions=[
            Mention(id=m["id"], username=m["username"], acct=m["acct"], url=m["url"])
            for m in obj["mentions"]
        ],
    )


def gen_account(obj: dict) -> Account:
    """Dict to NamedTuple utility.

    :param obj: (dict) mastodon.py user dict.
    """

    return Account(
        id=obj["id"],
        username=obj["username"],
        acct=obj["acct"],
        display_name=obj["display_name"],
        url=obj["url"],
        avatar=obj["avatar"],
        avatar_static=obj["avatar_static"],
        bot=obj["bot"],
    )
