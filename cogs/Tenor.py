import logging
import os
import discord
import aiohttp
import random
from requests import get
from discord.ext import commands
from discord import app_commands
from discord.ui import Button , View
from bot import SussyBot
class Tenor(commands.Cog):
    def __init__(self, bot: SussyBot) -> None:
        self.bot = bot

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

    @app_commands.command(name="gif",description="search for a gif")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    async def gif_slash(self, interaction: discord.Interaction,message:str=None):
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
                    button2 = Button(label="cancle", style=discord.ButtonStyle.red, )

                    async def button2_callback(interaction):

                        await interaction.response.edit_message(view=view.clear_items())

                    button = Button(label="Next image", style=discord.ButtonStyle.primary)
                    view = View()

                    async def button_callback(interaction):
                        search_url = f"https://g.tenor.com/v1/random?q=%s&key={apikey}&limit=25"

                        async with aiohttp.ClientSession() as cs:
                            async with cs.get(search_url) as r:
                                res = await r.json()

                                final_image = res["results"][random.randint(0, 25)]["media"][0]["tinygif"]["url"]
                        await interaction.response.edit_message(final_image, view=view)

                    button.callback = button_callback
                    button2.callback = button2_callback
                    view.add_item(button)
                    view.add_item(button2)
                    await interaction.response.send_message(final_image,view=view)
                else:
                    final_image = res["results"][random.randint(0, 25)]["media"][0]["tinygif"]["url"]
                    await interaction.response.send_message(final_image)


    @gif_slash.error
    async def gifslash_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"{error}", ephemeral=True)
        else:
            await interaction.response.send_message("**something went wrong do ``$help`` for help**", ephemeral=True)



async def setup(bot: SussyBot ) -> None:
    await bot.add_cog(
        Tenor(bot))