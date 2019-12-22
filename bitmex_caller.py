import sys
import os
import requests_async
from discord.ext import commands


class BitmexCaller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = 'https://d6oaq62km8.execute-api.us-east-1.amazonaws.com/Prod/cartelbot'
        # self.backend_headers = {'X-API-KEY': os.getenv('BACKEND_KEY')}
        self.backend_headers = {'X-API-KEY': bot.BACKEND_KEY}

    @commands.command()
    async def position(self, ctx):
        user = ctx.author
        print(f'Getting /position for user: {str(user)}')
        # action = '/position'
        # data = f'name={user.id}'
        # full_url = self.base_url + action + '?' + data
        resp = await requests_async.get(self.base_url + '/position',
                                        headers=self.backend_headers,
                                        params={'name': user.id})
        print('resp', resp.content)
        if 'error' in resp.json():
            await ctx.send(f'There was an error ({resp.json()["error"]["name"]}):'
                           f'\n{resp.json()["error"]["message"]}')
            return
        try:
            resp_dict = resp.json()[0]
        except KeyError as e:
            await ctx.send(f'No position for {user.mention} right now!'
                           # f'\n(or there was an error connecting to the server).'
                           f'')
            return
        currentQty = resp_dict['currentQty']
        direction = 'LONG:green_circle:'
        if currentQty < 0:
            direction = 'SHORT:red_circle:'
        avgEntryPrice = resp_dict['avgEntryPrice']
        await ctx.send(f"{user.mention}'s Position:"
                       f"\n**{currentQty}** contracts {direction} from entry **{avgEntryPrice}**")

    @commands.command()
    @commands.dm_only()
    async def api(self, ctx, key, secret):
        user = ctx.author
        print(f'Adding API keys for user: {str(user)}')

        # check parameter lengths
        if len(key) != 24 or len(secret) != 48:
            await ctx.send('There was a problem...'
                           '\nYour key should be exactly 24 characters, and your secret 48 characters.'
                           '\nDid you maybe mix them up?')
            return
        resp = await requests_async.get(self.base_url + '/add',
                                        headers=self.backend_headers,
                                        params={'name': user.id,
                                                'key': key,
                                                'secret': secret})
        print('resp', resp.content)
        if resp.status_code == requests_async.codes.ok:
            await ctx.send('Added your API key info successfully! Try the `. position` command in the server.')
        else:
            await ctx.send(f'Add action failed: status code {resp.status_code}. Please try again later.')
            return

    @commands.command()
    @commands.dm_only()
    async def remove(self, ctx):
        user = ctx.author
        print(f'Removing API keys for user: {str(user)}')
        resp = await requests_async.get(self.base_url + '/remove',
                                        headers=self.backend_headers,
                                        params={'name': user.id})
        print('resp', resp.content)
        if resp.status_code == requests_async.codes.ok:
            await ctx.send('Removed your API keys successfully.')
        else:
            await ctx.send(f'Remove action failed: status code {resp.status_code}. Please try again later.')


def setup(bot):
    bot.add_cog(BitmexCaller(bot))