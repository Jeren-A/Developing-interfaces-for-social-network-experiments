from mastobot import *
from os import environ

if __name__ == "__main__":
    instance = environ.get("INSTANCE")
    token = environ.get("ACCESS_TOKEN")
    bot = Bot(instance, token)

    """Test mention

    input: @bot Henlo
    output: @you hi, <your_display_name>
    """

    @bot.on_mention("henlo", validation=EQUALS, case_sensitive=False)
    def respond(status):
        return "hi, " + status.account.display_name

    """Test 'regex' validation

    input: :hacker_e: :hacker_d: :hacker_g: :hacker_y:
    outpur: nice hacker font you have
    """

    @bot.on_home_update("(:hacker_[a-z]:\s)+", validation=REGEX)
    def nice_hacker_font(status):
        return Reply("nice hacker font you have", visibility=UNLISTED)

    """Test 'evaluate' validation

    input: :cate: :cate: :cate:
    output: Woah, 3 cates - that's a lot!
    """

    has_more_than_two_cates = lambda s: s.count(":cate:") > 2

    @bot.on_home_update(has_more_than_two_cates, validation=EVALUATE)
    def so_many_cates(status):
        cate_count = status.content.count(":cate:")
        return Reply(f"Woah, {cate_count} cates - that's a lot!")

    """Test home timeline with 'contains' validation

    input: hey mastobot!
    output: yes i am online why do you ask
    """

    @bot.on_home_update("mastobot!", validation=CONTAINS)
    def online(status):
        return "yes i am online why do you ask"

    """Test 'equals' validation with list containing boost and fav as response

    input: mastobot plz favboost my post
    output: yes honey [fav] [boost]
    """

    @bot.on_home_update("mastobot plz favboost my post")
    def yes_honey(status):
        return ["yes honey", Favourite, Boost]

    """Test responding with nothing at all

    input: ksdfjdjgsakhghkalvfh
    output: [nothing at all]
    """

    @bot.on_home_update("ksdfjdjgsakhghkalvfh")
    def do_nothing(status):
        pass

    bot.run()
