from mastobot import Bot
bot = Bot(
    instance_url="https://mastodon.instance",
    access_token="NaaVC6ZOQY1Yf1Oz06XizwtPhynbTy16BuuNEpFAGPsn",
)

@bot.on_mention("hi")
def respond_to_hi(status):
    name = status.account.username
    return f"hey, {name}!"


bot.run()