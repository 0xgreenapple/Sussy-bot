import asyncio

import discord
import psutil
from discord.ext import commands
from bot import SussyBot
import datetime
import time
from datetime import timedelta
from discord.ext.commands import cooldown, BucketType
from discord import app_commands
import aiohttp
import json
import logging
import sqlite3
import asyncpg
from discord import ui
from discord.enums import TextStyle
from discord.ui import modal, TextInput
import json
import os
import bot


class test(commands.Cog):
    def __init__(self, bot: SussyBot):
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

    @commands.hybrid_command(name="ping", description="do ping pong")
    async def ping(self, ctx):
        await self.bot.db.execute(
            """
            INSERT INTO chat.messagecount (guild_id, user_id, message)
            VALUES ($1,$2, 1)
            ON CONFLICT (guild_id,user_id) DO 
            UPDATE SET message = COALESCE(messagecount.message, 0) + 1 
            """,
            ctx.guild.id,ctx.author.id
        )

        await ctx.send("done")
    @commands.command()
    async def pingv1(self,ctx,l=30):
        a = await self.bot.db.fetch(
            """
            SELECT user_id
            FROM chat.messagecount
             WHERE guild_id = $1
            """,
            ctx.guild.id
        )
        print("first")

        leaderboard = {}
        total = []
        for i in a:
            b = str(i).replace("<", "").replace(">", "").replace("=", " ").replace("Record", "").replace("user_id", "")
            name = int(b)
            x = await self.bot.db.fetchval(
                """
                SELECT message
                FROM chat.messagecount
                 WHERE user_id = $1 AND guild_id = $2
                """,
                int(b), ctx.guild.id
            )
            leaderboard[name] = x
            total.append(x)
            logging.warning(total)
            logging.warning(leaderboard)
        em = discord.Embed(title=f'Top 10 active members in {ctx.guild.name}', colour=self.bot.violet_color)
        sorted_words=sorted(leaderboard.items(),key=lambda item: int(item[1]),reverse = True)
        index = 1
        for key,val in sorted_words:
            id_ = key
            member = self.bot.get_user(id_)
            em.add_field(name=f'``{index}:`` {member}', value=f' **messages sent :** ``{val}``', inline=False)
            em.set_footer(text=f"{self.bot.user.name} : information requested by {ctx.author.display_name}",
                          icon_url=self.bot.user.avatar.url)

            if index == l:
                break
            else:
                index += 1
        await ctx.send(embed=em)

        """print(sorted_words)
        logging.warning(sorted_words)"""
        """em = discord.Embed(title=f'Top 10 active members in {ctx.guild.name}', colour=self.bot.violet_color)

        index = 1

        for amt in total:
            id_ = leaderboard[amt]
            member = self.bot.get_user(id_)
            em.add_field(name=f'``{index}:`` {member}', value=f' **messages sent :** ``{amt}``', inline=False)
            em.set_footer(text=f"{self.bot.user.name} : information requested by {ctx.author.display_name}",
                          icon_url=self.bot.user.avatar.url)

            if index == l:
                break
            else:
                index += 1
        await ctx.send(embed=em)"""

    @commands.command()
    async def pingv(self, ctx, l=30):
        a = await self.bot.db.fetch(
            """
            SELECT message
            FROM chat.messagecount
             WHERE user_id = $1 AND guild_id= $2
            """,
            ctx.author.id,ctx.guild.id
        )
        msg_ref = ctx.message.reference
        async with ctx.typing():
            # do expensive stuff here
            await ctx.send('done!')

    """ def get_bot_uptime(self, *, brief: bool = False) -> str:
        return time.human_timedelta(self.bot.uptime, accuracy=None, brief=brief, suffix=False)"""
    @commands.hybrid_command(name="stats", description="Get bot system information")
    @cooldown(1, 3, BucketType.user)
    async def stats(self, ctx):
        timestamp1 = datetime.datetime.utcnow()
        uptime = (timedelta(seconds=int(round(time.time() - self.bot.startTime))))

        member = 0
        for guilds in self.bot.guilds:
            a = guilds.member_count
            member += a
        bedem = discord.Embed(title='``status``',colour=self.bot.white_colour,timestamp=timestamp1)
        bedem.add_field(name="Ping",value=f"```{round(self.bot.latency*1000)}ms```",inline=True)
        bedem.add_field(name="Servers",value=f"```{len(self.bot.guilds)}```",inline=True)
        bedem.add_field(name="Users",value=f"```{member}```",inline=True)
        bedem.add_field(name="Uptime",value=f"```{uptime}```",inline=True)
        bedem.add_field(name="Memory",value=f"**total :** ``{round(psutil.virtual_memory().total/1000000000,2)} GB``\n"
                                            f"**used :** ``{round(psutil.virtual_memory().used/1000000000,2)} GB`` \n"
                                            f"**available :** ``{round(psutil.virtual_memory().available/1000000000,2)} GB``",inline=False)
        bedem.set_author(name=self.bot.user.name,icon_url=self.bot.user.avatar.url)
        bedem.set_footer(text="\u200b",icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=bedem)















async def setup(bot: SussyBot) -> None:
    await bot.add_cog(
        test(bot))
