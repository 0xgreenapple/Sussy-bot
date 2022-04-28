import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import json
import logging
import sqlite3
import asyncpg
from discord import ui
from discord.enums import TextStyle
from discord.ui import modal , TextInput
from datetime import datetime
import json




class Questionnaire(ui.Modal, title='Embed'):
    author= ui.TextInput(label='author')
    title = ui.TextInput(label='title')
    thumbnail = ui.TextInput(label='thumbnail url')
    image = ui.TextInput(label='image url')
    description = ui.TextInput(label='description', style=discord.TextStyle.paragraph)

    embed = discord.Embed(title=title,description=description)
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.title,description=self.description)
        embed.set_author(name=self.author)
        embed.set_image(url=self.image)
        embed.set_thumbnail(url=self.thumbnail)
        await interaction.response.send_message(embed=embed)
class test(commands.Cog ,):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(description="Submit feedback")
    async def creatembed(self,interaction: discord.Interaction):
        # Send the modal with an instance of our `Feedback` class
        await interaction.response.send_modal(Questionnaire())
async def setup(bot: commands.Bot ) -> None:
    await bot.add_cog(
        test(bot))

