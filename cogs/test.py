import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import json
import logging
import sqlite3
import asyncpg
from main import *

import json
class test(commands.Cog ,):
    def __init__(self, bot: commands.Bot , ) -> None:
        self.bot = bot


    """@app_commands.command(name="send", description="send message to a channel")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.checks.has_permissions(manage_channels = True)
    @app_commands.describe(channel="the channel where you want to send message to",
                           message="message that you want to send")
    async def send_ch(self, interaction: discord.Interaction, channel: discord.TextChannel, message: str):
        self.channel = channel

        await channel.send(message)
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(f"succesfuly sent! , message: ||{message}|| to {channel} channel")

    @commands.command()
    async def roast(self, ctx):
        async with aiohttp.ClientSession() as cs:

            link = "https://insult.mattbas.org/api/"
            async with cs.get(link) as r:
                res = await r.json()
                logging.warning(res)

    @commands.command()
    async def set_r(self,ctx, channel: discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, channel_id) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Channel has been set to {channel.mention}")
            elif result is not None:
                sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
                val = ( channel.id,ctx.guild.id)
                await ctx.send(f"Channel has been updated to {channel.mention}")
            cursor.execute(sql , val)
            db.commit()
            cursor.close()
            db.close()

    @commands.command()
    async def rule_set(self, ctx,*,text):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, msg) VALUES(?,?)")
                val = (ctx.guild.id, text)
                await ctx.send(f"rule has been set to \n{text}")
            elif result is not None:
                sql = ("UPDATE main SET msg = ? WHERE guild_id = ?")
                val = (text, ctx.guild.id)
                await ctx.send(f"Channel has been updated to \n {text}")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
    @commands.command()
    async def rule1(self,ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        else:
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {ctx.guild.id}")
            result1 = cursor.fetchone()
            await ctx.send(str(result1[0]))
    @commands.command()
    async def set_rule(self, ctx, *,text:str):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT rule FROM role WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO role(guild_id, rule) VALUES(?,?)")
            val = (ctx.guild.id, text)
            await ctx.send(f"rule has been set to \n{text}")
        elif result is not None:
            sql = ("UPDATE role SET rule = ? WHERE guild_id = ?")
            val = (text, ctx.guild.id)
            await ctx.send(f"Channel has been updated to \n {text}")
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()"""

    """@commands.command()
    async def rule(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT rule FROM role WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            await ctx.send("``this server does not have a rule| what a fool``")
        else:
            await ctx.send(str(result[0]))"""
    """@tasks.loop(seconds=3600)
        async def change_status(self):
            status = cycle(['$help', 'Green apple', 'amongus', 'SUS', 'bruh', 'ur mom', '0101000101', 'game of life'])
            await bot.change_presence(activity=discord.Game(next(status)))"""


    """@commands.command()
    async def hello1(self, ctx):
        logging.warning('hello')

    @commands.command()
    async def bal(self,ctx , roles):"""
    @commands.Cog.listener()
    async def on_ready(self):
        """print client is ready on ready"""
        await self.pg_con.execute("CREATE TABLE IF NOT EXISTS economy (user_id BIGINT NOT NULL, money BIGINT)")
        await self.pg_con.execute("ALTER TABLE economy ADD COLUMN IF NOT EXISTS user_id BIGINT NOT NULL")
        await self.pg_con.execute("ALTER TABLE economy ADD COLUMN IF NOT EXISTS money BIGiNT")

    async def add(self, id , amount=2000):
        bal = await self.pg_con.fetchrow("SELECT money FROM economy WHERE user_id = $1",id)
        await self.pg_con.execute('UPDATE economy SET money = $! WHERE user_id =$2',amount+bal[0],id)

    async def cheak(self, id):
        user = await self.pg_con.fetchrow("SELECT * FROM economy WHERE user_id = $1",id)
        if not user:
            await self.pg_con.execute("INSERT INTO economy (user_id, money) VALUES ($1, $2)",id,2000)

    async def balance(self, id):
        bal = await self.pg_con.fetchrow("SELECT money FROM economy WHERE user_id = $1", id)
        return bal[0]

    async def top(self):
        tops = await self.pg_con.fetchrow("SELECT * FROM economy ORDER BY money DESC NULLS LAST")
        return tops

    @commands.command()
    async def trials(self, ctx):
        id= ctx.author.id
        await self.cheak(id)
        await self.add(id,1000)
        tops = await self.top()
        await ctx.send("done")



async def setup(bot: commands.Bot ) -> None:
    await bot.add_cog(
        test(bot))

