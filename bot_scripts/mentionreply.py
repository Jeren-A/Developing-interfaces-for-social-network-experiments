from mastobot import Bot
bot = Bot(
    instance_url="https://mastodon.social",
    access_token="NaaVC6ZOQY1Yf1Oz06XizwtPhynbTy16BuuNEpFAGPs",
)


@bot.on_mention("hi")
def respond_to_hi(status):
    name = status.account.display_name
    return f"hey, {name}!"

bot.run()

