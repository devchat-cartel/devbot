import os
import asyncio
import datetime

import requests
import discord
from discord.ext import commands

GITHUB_CHECK_INTERVAL = 60
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

client = discord.Client()
# bot = commands.Bot('. ')

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

# @bot.command(name='')
# async def _message(ctx):
#     print(ctx.message.content)

# @bot.command(name='private')
# async def _priv8(ctx):
#     await ctx.send('Found me !')

# @bot.command()
# async def last_commit(ctx):
#     await ctx.send(
#         'Last commit was at {last_push}'.format(
#             last_push=get_last_github_push()
#         )
#     )

# @bot.command()
# async def echo(ctx, message):
#     await ctx.send(message)

async def background_task_github_push():
    await client.wait_until_ready()
    general = client.get_channel(518770364042444850)
    latest_push = None
    while not client.is_closed():
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


@client.event
async def on_ready():
    print('Ready')


@client.event
async def on_message(message):
    # if message.author == client.user:
    #     return
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

if __name__ == '__main__':
    client.loop.create_task(
        background_task_github_push()
    )
    client.run(
        os.getenv(
            'TOKEN',
            ''
        )
    )
    # bot.run(
    #     os.getenv(
    #         'TOKEN',
    #         ''
    #     )
    # )
