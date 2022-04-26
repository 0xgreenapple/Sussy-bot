import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import json
import logging
import sqlite3
import asyncpg
from main import *
from discord import ui
from discord.enums import TextStyle
from discord.ui import modal , TextInput
from datetime import datetime
import json




class my_modal(ui.Modal, title = "example modal"):
    ans = ui.TextInput(label= "asdasdasd" ,style= discord.TextStyle.short, placeholder="yes" , default="yes/no",required=True,max_length= 8)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title= self.title, description=f"{self.ans.label} \n {self.ans}",timestamp=datetime.now(),color= discord.Color.red())
        embed.set_author(name= interaction.user , icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)



class test(commands.Cog ,):
    def __init__(self, bot: commands.Bot , ) -> None:
        self.bot = bot

    @app_commands.command(name="test",description="hello world")
    async def modal(self, interaction = discord.Interaction):
        await interaction.response.send_modal(my_modal())

async def setup(bot: commands.Bot ) -> None:
    await bot.add_cog(
        test(bot))

