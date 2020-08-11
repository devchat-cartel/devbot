import sys
import os

import requests_async
from discord.ext import commands


class BitmexCaller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_symbols = [
            'XBT',
            'ETH',
            'BCH',
            'EOS',
            'LTC',
            'TRX',
            'XRP',
            'ADA'
        ]
        self.base_url = 'https://d6oaq62km8.execute-api.us-east-1.amazonaws.com/Prod/cartelbot'
        self.backend_headers = {'X-API-KEY': bot.BACKEND_KEY}
        self.pau = '275366370403811329'
        self.bort = '396960313687408661'
    @commands.command(name='n', aliases=['nigger'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def nicecar(self, ctx):
        ctx.send(f"i")

    @commands.command(name='pau')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def show_pau(self, ctx, symbol='XBTUSD'):
        user = ctx.author
        symbol = str(symbol).upper()

        if not symbol[:3] in self.allowed_symbols:
            await ctx.send(f"I don't know that symbol, can you try again ?")
            return

        resp = await requests_async.get(self.base_url + '/position',
                                        headers=self.backend_headers,
                                        params={'name': self.pau})

        if resp.status_code == 204:
            await ctx.send(f'PAU is busy right now, check later {user.mention} right now!')
            return
        
        resp_json = resp.json()

        if type(resp_json) == list:
            data = [e for e in resp_json if e['symbol'] == symbol]

            if data == [] or data[0]['currentQty'] == 0:
                currentQty = 0
                entry = '--'
                pnl = 0
            else:
                currentQty = data[0]['currentQty']
                pnl = data[0]['unrealisedPnl'] / (10 ** 8)
                if pnl < 0.1 ** 4:
                    pnl = f'{pnl:.8f}'
                if data[0]['avgEntryPrice'] > 0.1 ** 4:
                    entry = data[0]['avgEntryPrice']
                else:
                    entry = f"{data[0]['avgEntryPrice']:.8f}"

            if currentQty > 0:
                direction = 'LONG :green_circle:'
            elif currentQty < 0:
                direction = 'SHORT :red_circle:'
            else:
                direction = 'FLAT :zero:'

            message_text = f"PAU is {direction}"
            if entry != '--':
                message_text += f" **{currentQty} {symbol}** from entry **{entry}** with PNL {pnl} XBT"

            await ctx.send(message_text)
        elif 'error' in resp_json:
            await ctx.send(f"Error: {resp_json['error']['message']}")
        else:
            channel = await self.bot.fetch_channel('704468233872211988')
            await channel.send(f"{user.name}\n{resp_json}")

    @commands.command(name='liquidation', aliases=['l', 'liq'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def show_liquidation_price(self, ctx, symbol='XBTUSD'):
        user = ctx.author
        symbol = str(symbol).upper()

        if not symbol[:3] in self.allowed_symbols:
            await ctx.send(f"I don't know that symbol, can you try again ?")
            return

        resp = await requests_async.get(self.base_url + '/position',
                                        headers=self.backend_headers,
                                        params={'name': user.id})

        if resp.status_code == 204:
            await ctx.send(f'No position for {user.mention} right now!'
                           f'\nHave you DMed me your (read-only) API key yet?'
                           f'\n(command is: . api <key> <secret>)')
            return

        resp_json = resp.json()

        if type(resp_json) == list:
            data = [e for e in resp_json if e['symbol'] == symbol]

            if data == [] or data[0]['currentQty'] == 0:
                liq = 0
            else:
                liq = data[0]['liquidationPrice']
                if liq < 0.1 ** 4:
                    liq = f'{liq:.8f}'

            message_text = f"No {symbol} position found for {user.mention} !"
            if liq != 0:
                message_text = f"Liquidation price for {user.mention} is {liq}"
            await ctx.send(message_text)
        elif 'error' in resp_json:
            await ctx.send(f"Error: {resp_json['error']['message']}")
        else:
            channel = await self.bot.fetch_channel('704468233872211988')
            await channel.send(f"{user.name}\n{resp_json}")

    @commands.command(name='pnl', aliases=['rnpl'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def show_profits_and_losses(self, ctx, symbol='XBTUSD'):
        user = ctx.author
        symbol = str(symbol).upper()

        if not symbol[:3] in self.allowed_symbols:
            await ctx.send(f"I don't know that symbol, can you try again ?")
            return

        resp = await requests_async.get(self.base_url + '/position',
                                        headers=self.backend_headers,
                                        params={'name': user.id})

        if resp.status_code == 204:
            await ctx.send(f'No position for {user.mention} right now!'
                           f'\nHave you DMed me your (read-only) API key yet?'
                           f'\n(command is: . api <key> <secret>)')
            return

        resp_json = resp.json()

        if type(resp_json) == list:
            data = [e for e in resp_json if e['symbol'] == symbol]

            if data == [] or data[0]['currentQty'] == 0:
                pnl = 0
            else:
                pnl = data[0]['realisedPnl'] / (10 ** 8)
                upnl = data[0]['unrealisedPnl'] / (10 ** 8)
                if abs(pnl) < 0.1 ** 4:
                    pnl = f'{pnl:.8f}'

                if abs(upnl) < 0.1 ** 4:
                    upnl = f'{upnl:.8f}'

            message_text = f"No {symbol} Pnl found for {user.mention} !"
            if float(pnl) > 0:
                message_text = f"Profit for {user.mention}   RPnl: {pnl}:green_circle:   UPnl: {upnl}:green_circle:"
            elif float(pnl) < 0:
                message_text = f"Losses for {user.mention}   RPnl: -{pnl}:red_circle:   UPnl: -{upnl}:red_circle:"
            await ctx.send(message_text)
        elif 'error' in resp_json:
            await ctx.send(f"Error: {resp_json['error']['message']}")
        else:
            channel = await self.bot.fetch_channel('704468233872211988')
            await channel.send(f"{user.name}\n{resp_json}")

    @commands.command(name='position', aliases=['p', 'pos'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def show_current_position(self, ctx, symbol='XBTUSD'):
        user = ctx.author
        symbol = str(symbol).upper()

        if not symbol[:3] in self.allowed_symbols:
            await ctx.send(f"I don't know that symbol, can you try again ?")
            return

        print(f'Getting /position for user: {str(user)}')
        resp = await requests_async.get(self.base_url + '/position',
                                        headers=self.backend_headers,
                                        params={'name': user.id})

        if resp.status_code == 204:
            await ctx.send(f'No position for {user.mention} right now!'
                           f'\nHave you DMed me your (read-only) API key yet?'
                           f'\n(command is: . api <key> <secret>)')
            return

        resp_json = resp.json()

        if type(resp_json) == list:
            data = [e for e in resp_json if e['symbol'] == symbol]

            if data == [] or data[0]['currentQty'] == 0:
                currentQty = 0
                entry = '--'
                pnl = 0
            else:
                currentQty = data[0]['currentQty']
                pnl = data[0]['unrealisedPnl'] / (10 ** 8)
                if pnl < 0.1 ** 4:
                    pnl = f'{pnl:.8f}'
                if data[0]['avgEntryPrice'] > 0.1 ** 4:
                    entry = data[0]['avgEntryPrice']
                else:
                    entry = f"{data[0]['avgEntryPrice']:.8f}"

            if currentQty > 0:
                direction = 'LONG :green_circle:'
            elif currentQty < 0:
                direction = 'SHORT :red_circle:'
            else:
                direction = 'FLAT :zero:'

            message_text = f"{user.mention} is {direction}"
            if entry != '--':
                message_text += f" **{currentQty} {symbol}** from entry **{entry}** with PNL {pnl} XBT"

            await ctx.send(message_text)
        elif 'error' in resp_json:
            await ctx.send(f"Error: {resp_json['error']['message']}")
        else:
            channel = await self.bot.fetch_channel('704468233872211988')
            await channel.send(f"{user.name}\n{resp_json}")

    @commands.command()
    @commands.dm_only()
    async def api(self, ctx, key, secret):
        user = ctx.author
        print(f'Adding API keys for user: {str(user)}')

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
        if resp.status_code == requests_async.codes.ok:
            await ctx.send('Added your API key info successfully! Try the `. position` command in the server.')
        else:
            await ctx.send(f'Add action failed: status code {resp.status_code}. Please try again later.')
            return

    @commands.command(aliases=['delete'])
    @commands.dm_only()
    async def remove(self, ctx):
        user = ctx.author
        print(f'Removing API keys for user: {str(user)}')
        resp = await requests_async.get(self.base_url + '/remove',
                                        headers=self.backend_headers,
                                        params={'name': user.id})
        if resp.status_code == requests_async.codes.ok:
            await ctx.send('Removed your API keys successfully.')
        else:
            await ctx.send(f'Remove action failed: status code {resp.status_code}. Please try again later.')


def setup(bot):
    bot.add_cog(BitmexCaller(bot))
