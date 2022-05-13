import logging
import os
import discord
from discord.ext.commands import cooldown, BucketType
import aiohttp
import random

from requests import get
from discord.ext import commands
from discord import app_commands
from bot import SussyBot
class unsplash(commands.Cog):
    def __init__(self, bot: SussyBot) -> None:
        self.bot = bot

    @commands.command(pass_context=True)
    @cooldown(1 , 10 , BucketType.user)



    async def image(self, ctx, *, message=None):
        try:
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
        except IndexError:
            embed1 = discord.Embed(title=f"there is no image called {message}")
            await ctx.send(embed1)
        except:
            await ctx.send("**i m dying**")

    @app_commands.command(name="image")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    async def image_slash(self, interaction: discord.Interaction,*,message:str=None):
        try:
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
                    await interaction.response.send_message(embed=embed4)
        except IndexError:
            embed1 = discord.Embed(title=f"there is no image called {message}")
            await interaction.response.send_message(embed=embed1)
        except:
            await interaction.response.send_message("**i m dying**")





async def setup(bot: SussyBot ) -> None:
    await bot.add_cog(
        unsplash(bot))

