import sys
import os
import asyncio
import datetime
import textwrap

import requests
import discord
from discord.ext import commands

GITHUB_CHECK_INTERVAL = 60
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

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


@bot.command(name='private')
@commands.cooldown(1, 10, commands.BucketType.user)
async def _priv8(ctx):
    await ctx.send('Found me !')


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def last_commit(ctx):
    last_push_ago = datetime.datetime.now() - get_last_github_push()
    last_push_ago -= datetime.timedelta(microseconds=last_push_ago.microseconds)
    await ctx.send(f'Last commit was {last_push_ago} ago')


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def echo(ctx, *, message):
    await ctx.send(message)


async def background_task_github_push():
    await bot.wait_until_ready()
    general = bot.get_channel(551913608804827178)
    latest_push = None
    while not bot.is_closed():
        try:
            last_push = get_last_github_push()
            if latest_push and last_push > latest_push:
                latest_push = last_push
                await general.send(f'New commit found at {latest_push} !')
            else:
                await asyncio.sleep(GITHUB_CHECK_INTERVAL)
        except Exception as e:
            print(str(e))
            await asyncio.sleep(GITHUB_CHECK_INTERVAL)


bot.remove_command("help")
@bot.command()
async def help(ctx):
    dmchannel = await ctx.author.create_dm()
    await dmchannel.send(textwrap.dedent(f"""
            **COMMANDS**
            ```
            . help
            displays positiontracker's help menu

            . position
            shows your current /position in a public channel

            . echo <message>
            echoes back your message in the channel

            . api <key> <secret>
            (DM-only) sets up your Bitmex API credentials

            . remove
            (DM-only) removes your Bitmex API credentials from the bot
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
            will display your current position with the # of contracts, long/short, and entry price.

            **REMOVING YOUR API KEYS**

            To erase your API keys (DM me):
            `. remove`
            """
        )[1:-1] # remove leading and trailing newlines
    )


@bot.event
async def on_ready():
    print('Ready')
    guilds = await bot.fetch_guilds(limit=5).flatten()     # guilds is now a list of Guild...
    for guild in guilds:
        print(guild)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(
        ' | '.join(
            str(e)
            for e in (
                message.guild,
                message.channel,
                message.author,
                message.content
            )
        )
    )
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if type(error) == commands.CommandOnCooldown:
        # await ctx.send(f"Chill out, {ctx.author.mention}! You have to wait 10 seconds between commands... stop spamming, retard")
        return
    await ctx.send(f"Unknown command: {ctx.message.content[2:]}")
    await commands.Bot.on_command_error(bot, ctx, error)    # pretty much just for printing to console


if __name__ == '__main__':
    bot.loop.create_task(
        background_task_github_push()
    )
    bot.BACKEND_KEY = sys.argv[2]
    bot.load_extension('bitmex_caller')
    try:
        bot.run(
            # os.getenv(
            #     'TOKEN',
            #     ''
            # )
            sys.argv[1]
        )
    except (KeyboardInterrupt):
        sys.exit()
