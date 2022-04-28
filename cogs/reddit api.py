import logging
import os
import discord
import aiohttp
import random
from discord.ext import commands



class reddit_api(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


#reddit=====================================================================
    @commands.command(pass_context=True)
    async def memes(self, ctx):
        try:
            embed = discord.Embed(title="yo boi", description="")

            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                    res = await r.json()
                    embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                    await ctx.message.add_reaction("✅")
                    await ctx.send(embed=embed)
        except IndexError:
            await ctx.send("api is down try again")



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




async def setup(bot: commands.Bot ) -> None:
    await bot.add_cog(
        reddit_api(bot))