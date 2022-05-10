import asyncio

import discord
from discord.ext import commands
from bot import SussyBot
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
from datetime import datetime
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
        logging.warning(a)
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
            leaderboard[x] = name
            total.append(x)
            logging.warning(total)
            logging.warning(leaderboard)


        print("second")
        em = discord.Embed(title=f'Top 10 active members in {ctx.guild.name}', colour=self.bot.violet_color)

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
        await ctx.send(embed=em)

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
        await ctx.send(a)














async def setup(bot: SussyBot) -> None:
    await bot.add_cog(
        test(bot))
