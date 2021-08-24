# List common constants used by Mastobot and Mastodon.py here
# Comes handy if you have autocomplete

# Mastobot section
# StreamListener.on_xxx()
UPDATE = "update"
NOTIFICATION = "notification"

# Trigger(validation="xxx")
EQUALS = "equals"
CONTAINS = "contains"
REGEX = "regex"
EVALUATE = "evaluate"
VALIDATION_LIST = [EQUALS, CONTAINS, REGEX, EVALUATE]

# Mastodon.py section
# toot = {"xxx": "..."}
STATUS = "status"
SENSITIVE = "sensitive"
VISIBILITY = "visibility"
SPOILER_TEXT = "spoiler_text"

# toot = {"visibility": "xxx"}
PUBLIC = "public"
UNLISTED = "unlisted"
PRIVATE = "private"
DIRECT = "direct"
VISIBILITY_LIST = [PUBLIC, UNLISTED, PRIVATE, DIRECT]

# notification= {"type": "xxx"}
MENTION = "mention"
FAVOURITE = "favourite"
REBLOG = "reblog"
FOLLOW = "follow"
UPDATE = "update"
EVENT_LIST = [MENTION, FAVOURITE, REBLOG, FOLLOW, UPDATE]

