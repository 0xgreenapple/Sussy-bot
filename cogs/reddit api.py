import logging
import os
import discord
import aiohttp
import random
from requests import get
from discord.ext import commands



class fun(commands.Cog):

    def __init__(self, client):
        self.client = client


#reddit=====================================================================
    @commands.command(pass_context=True)
    async def memes(self, ctx):
        embed = discord.Embed(title="yo boi", description="")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def meirl(self, ctx):
        embed4 = discord.Embed(title="", description="")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/me_irl/new.json?sort=hot') as r:
                res = await r.json()
                embed4.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed4)


    @commands.command(pass_context=True)
    async def space(self, ctx):
        embed10 = discord.Embed(title="", description="")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/astrophotography/new.json?sort=hot') as r:
                res = await r.json()
                embed10.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed10)


def setup(client):
    client.add_cog(fun(client))