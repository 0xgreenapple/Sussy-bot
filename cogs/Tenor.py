import logging
import os
import discord
import aiohttp
import random
from requests import get
from discord.ext import commands



class gif(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def gif(self, ctx, *, message=None):
        apikey = os.environ["GIF_KEY"]
        search_url = None
        if message != None:
            search_url = f"https://g.tenor.com/v1/search?q={message}&key={apikey}&limit=25"
        else:
            search_url = f"https://g.tenor.com/v1/random?q=%s&key={apikey}&limit=25"

        async with aiohttp.ClientSession() as cs:
            async with cs.get(search_url) as r:
                res = await r.json()

                if message == None:
                    # logging.warning(res['results'])
                    final_image = res["results"][random.randint(0, 25)]["media"][0]["tinygif"]["url"]
                else:
                    final_image = res["results"][random.randint(0, 25)]["media"][0]["tinygif"]["url"]

                await ctx.message.add_reaction("✅")
                await ctx.send(final_image)

def setup(client):
    client.add_cog(gif(client))

