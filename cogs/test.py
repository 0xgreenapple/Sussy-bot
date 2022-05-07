import discord
from discord.ext import commands
from discord.ext.commands import cooldown,BucketType
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
class test(commands.Cog ,):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    """@commands.command()
    async def roletest(self,ctx,role: discord.Role):
        members = []
        a = 0

        for member in role.members:
            a += 1
            members.append(f"**``{a} :``** {member.mention}")

        allMember = '\n'.join(members)
        embed = discord.Embed(title=role.name,description=f"this is the list of members in \n{role.name}{allMember}")
        # for i in members:
        #     allMember = allMember.join(i)
        logging.warning(allMember)
        logging.warning(members)
        await ctx.send(embed=embed)"""

    @commands.hybrid_command(name="ping",description="do ping pong")
    async def ping(self,ctx):
        await ctx.send("ping")



async def setup(bot: commands.Bot ) -> None:
    await bot.add_cog(
        test(bot))

