import sys
import os
import asyncio
import datetime
import textwrap
import collections

import requests
import discord
from discord.ext import commands

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
GIT_REPO_URL = 'https://github.com/devchat-cartel/devbot/branches'

bot = commands.Bot('. ',
                   case_insensitive=True)

def get_last_github_push():
    response = requests.get(
        'https://api.github.com/repos/devchat-cartel/devbot'
    )
    try:
        return datetime.datetime.strptime(
            response.json()['pushed_at'],
            DATE_FORMAT
        )
    except:
        return 'Unknown'

def get_last_commit():
    response = requests.get(
        'https://api.github.com/repos/devchat-cartel/devbot/git/refs/heads'
    )

    branches = [
        e['object']['url']
        for e in response.json()
    ]

    commits = [
        requests.get(e).json()
        for e in branches
    ]

    messages = {
        e['author']['date'] : e['message']
        for e in commits
    }

    return (messages[max(messages.keys())].items())

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def last_commit(ctx):
    last_push_ago = datetime.datetime.now() - get_last_github_push()
    last_push_ago -= datetime.timedelta(microseconds=last_push_ago.microseconds)
    await ctx.send(f'Last commit was {last_push_ago} ago')


@bot.command(name='private')
@commands.cooldown(1, 10, commands.BucketType.user)
async def echo(ctx, *, message):
    await ctx.send(message)


@bot.command()
async def repo(ctx):
    dmchannel = await ctx.author.create_dm()
    await dmchannel.send(GIT_REPO_URL)

bot.remove_command("help")
@bot.command()
async def help(ctx):
    dmchannel = await ctx.author.create_dm()
    await dmchannel.send(textwrap.dedent(f"""
            **COMMANDS**
            ```
            `. help`
            sends you this message

            `. position [<symbol>]`
            shows your current position size and entry price for <symbol> in a public channel (XBTUSD default)
            aliases are `. p` and `. pos`

            `. liquidation [<symbol>]`
            shows your current liquidation price for <symbol> in a public channel (XBTUSD default)
            aliases are `. l` and `. liq`

            `. api <key> <secret>`
            (DM-only) sets up your Bitmex API credentials

            `. remove`
            (DM-only) removes your Bitmex API credentials from the bot
            aliases are `. delete`
            ```
            **API KEY SETUP**

            To retrieve your current /position, you need to tell the bot your Bitmex API keys.

            In your bitmex account settings, create a READ-ONLY API key (do not select 'order'
            or 'order cancel' in the drop-down; just leave it on the default '-').

            Then, DM me (the bot) using the command:
            `. api <key> <secret>`

            for example:
            `. api nBRcCH6uE49KgLCMjJn09DEA -jNDyaMgwqoZT8V3-4Hmx5oA5UeNOYICNk3dl4H6w1-s5sxA`

            **SHOWING YOUR POSITION**

            In a public channel (like #bitmex), typing:
            `. position`
            will display your current XBTUSD position with the # of contracts, long/short, and entry price.

            `. position ETHUSD`
            will display your current ETHUSD position with the # of contracts, long/short and entry price.

            **REMOVING YOUR API KEYS**

            To erase your API keys (DM me):
            `. remove`
            """
        )[1:-1]
    )


@bot.event
async def on_ready():
    print('Ready')
    guilds = await bot.fetch_guilds(limit=5).flatten()
    for guild in guilds:
        print(guild)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if type(error) == commands.CommandOnCooldown:
        # await ctx.send(f"Chill out, {ctx.author.mention}! You have to wait 10 seconds between commands... stop spamming, retard")
        return
    await ctx.send(f"Unknown command: {ctx.message.content[2:]}")
    await commands.Bot.on_command_error(bot, ctx, error)


if __name__ == '__main__':
    bot.BACKEND_KEY = sys.argv[2]
    bot.load_extension('bitmex_caller')
    try:
        bot.run(
            sys.argv[1]
        )
    except (KeyboardInterrupt):
        sys.exit()
