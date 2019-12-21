from discord.ext import commands
from cryptowrapper import BitMEX
from configparser import ConfigParser


class BitmexCaller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.keylist = ConfigParser()

    def get_key_by_userid(self, userid: str):
        self.keylist.read('keys.txt')
        if self.keylist.has_section(userid):
            key = self.keylist.get(userid, 'key')
            # print(key)
            secret = self.keylist.get(userid, 'sec')
            # print(secret)
            return key, secret
        return False, None  # could be None, False or either or... doesn't matter

    @commands.command()
    async def position(self, ctx):
        user = ctx.author
        key, secret = self.get_key_by_userid(str(user.id))  # cast to string so configparser can read it in .txt file
        if not key:
            await ctx.send(f"Sorry, API access isn't set up for {user}. Please send me a DM using the '. api' command:"
                           f"\n`. api <key> <secret>`"
                           f"\n With your (read-only!) api key info filled in.")
            return

        client = BitMEX(asynchronous=True, api_key=key, api_secret=secret)
        resp = await client.position_GET()

        currentQty = resp[0]['currentQty']
        direction = 'LONG:green_circle:'
        if currentQty < 0:
            direction = 'SHORT:red_circle:'
        avgEntryPrice = resp[0]['avgEntryPrice']
        await ctx.send(f"{str(user)} Position:"
                       f"\n**{currentQty}** contracts {direction} from entry **{avgEntryPrice}**")


def setup(bot):
    bot.add_cog(BitmexCaller(bot))