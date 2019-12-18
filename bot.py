import os
import asyncio
import datetime

import requests
import discord

GITHUB_CHECK_INTERVAL = 60
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

client = discord.Client()
bot = discord.ext.commands.Bot()

# the #general channel
general = bot.get_channel(518770364042444850)


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


async def background_task_github_push():
    await bot.wait_until_ready()
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


@client.event
async def on_ready():
    print('Ready')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # if message.author != client.user:
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

    if message.content.startswith('. '):
        if message.content[2:].startswith('last'):
            await general.send(
                'Last commit was at {last_push}'.format(
                    last_push=get_last_github_push()
                )
            )
        else:
            await general.send(
                'Unknown command: {message}'.format(
                    message=message.content[2:]
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
