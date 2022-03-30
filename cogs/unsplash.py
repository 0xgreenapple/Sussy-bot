import logging
import os
import discord
import aiohttp
import random
from requests import get
from discord.ext import commands



class unsplash(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def image(self, ctx, *, message=None):
        unsplashID = os.environ['UNSPLASH_KEY']
        embed4 = discord.Embed(title="", description="")
        search_url = None
        final_image = None
        if message != None:
            search_url = f'https://api.unsplash.com/search/photos?client_id={unsplashID}&query={message}&per_page=25'
        else:
            search_url = f'https://api.unsplash.com/photos/random?client_id={unsplashID}&count=2'

        async with aiohttp.ClientSession() as cs:
            async with cs.get(search_url) as r:
                res = await r.json()
                if message != None:
                    final_image = res['results'][random.randint(0, 25)]['urls']['small']
                else:
                    final_image = res[0]['urls']['small']

                embed4.set_image(url=final_image)
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed4)

def setup(client):
    client.add_cog(unsplash(client))


