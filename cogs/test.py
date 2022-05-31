import asyncio

import PIL.TiffImagePlugin
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
import typing
import asyncpg
import os
import bot
from typing import Literal




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
            ctx.guild.id, ctx.author.id
        )

        await ctx.send("done")

    @commands.command()
    async def pingv1(self, ctx, l=30):
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
        sorted_words = sorted(leaderboard.items(), key=lambda item: int(item[1]), reverse=True)
        index = 1
        for key, val in sorted_words:
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
            ctx.author.id, ctx.guild.id
        )
        msg_ref = ctx.message.reference
        async with ctx.typing():
            # do expensive stuff here
            await ctx.send('done!')

    """ def get_bot_uptime(self, *, brief: bool = False) -> str:
        return time.human_timedelta(self.bot.uptime, accuracy=None, brief=brief, suffix=False)"""

    @commands.hybrid_command(name="stats", description="Get bot system information")
    @cooldown(1, 3, BucketType.user)
    async def stats(self, ctx:commands.Context):
        shard = self.bot.get_shard(ctx.guild.shard_id)
        ping = shard.latency * 1000

        if ping >=100 and ping <= 200:
            ping_status = "neutral"
        elif ping <=100:
            ping_status = "low"
        else:
            ping_status = "high"
        timestamp1 = datetime.datetime.utcnow()
        uptime = (timedelta(seconds=int(round(time.time() - self.bot.startTime))))

        member = 0
        for guilds in self.bot.guilds:
            if guilds.shard_id == shard.id:
                a = guilds.member_count
                member += a
        bedem = discord.Embed(title='``status``', colour=self.bot.white_colour, timestamp=timestamp1)
        bedem.add_field(name=f"Ping **({ping_status})**", value=f"```{round(self.bot.latency * 1000)}ms```", inline=True)
        bedem.add_field(name="Servers", value=f"```{len([guild for guild in self.bot.guilds if guild.shard_id == shard.id])}```", inline=True)
        bedem.add_field(name="Users", value=f"```{member}```", inline=True)
        bedem.add_field(name="Uptime", value=f"```{uptime}```", inline=True)
        bedem.add_field(name="System",
                        value=f"**memory Usage:** ``{round(psutil.virtual_memory().used / 1000000000, 2)} GB/{round(psutil.virtual_memory().total / 1000000000, 2)} GB`` \n "
                              f"**cpu :** ``{psutil.cpu_percent()}``%"
                        , inline=False)
        bedem.add_field(name="command ran today", value=f"```18238183```")
        bedem.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        bedem.set_footer(text="\u200b", icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=bedem)

    @app_commands.command(name="hello")
    async def hello1(self, interaction=discord.Interaction):
        await interaction.response.send_message("hello")


    @commands.command(name="test1")
    async def avatar(self,ctx):
        formats = ["png","webp",]
        small_size = ctx.author.avatar.with_size(256).with_static_format("png").url
        medium_size = ctx.author.avatar.with_size(512).with_static_format("png").url
        large_size=ctx.author.avatar.with_size(1024).with_static_format("png").url
        verylarge_size = ctx.author.avatar.with_size(2048).with_static_format("png").url

        embed = discord.Embed(title=f"``avatar of {ctx.author.display_name}``",description=f"**Sizes:**:  **[SMALL]({small_size})** | **[MEDIUM]({medium_size})** | **[LARGE]({large_size})** | **[VERY LARGE]({verylarge_size})**|",timestamp=datetime.datetime.utcnow(),colour=self.bot.yellow_colour)
        embed.set_image(url=ctx.author.avatar.url)
        embed.set_footer(text="size default (512x512)")
        embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="timeout")
    async def mute(self,ctx,member:discord.Member,time:int,*,reason:str):
        imeout = (discord.utils.utcnow() + datetime.timedelta(minutes=time))
        await member.timeout(imeout,reason=reason)
        await ctx.send(f"{member} is timedout out until {time} minteus ")


    @commands.command()
    async def unmute(self, ctx, member: discord.Member,*, reason: str):
        await member.timeout(None,reason=reason)
        await ctx.send("member has been timed out")
        channel = await member.create_dm()
        await channel.send("you have been timed out")
    @commands.command()
    async def userinfo(self,ctx,memder:typing.Union[discord.Member,discord.User]=None):

        if memder is None:

            badges = await self.shop(member=ctx.author)
            a = ctx.author.roles
            a.sort(reverse=True)
            logging.warning(a)
            first_line1= " "
            second_line1= " "
            third_line1 = " "
            first_line = []
            second_line = []
            third_line = []
            b = " "
            for i in a:
                if i.name != "@everyone":
                    while len(first_line) != 4:
                        first_line.append(i.name)
                        break
                    if len(first_line) == 4:
                        if len(i.name) <= 6:
                            while len(second_line) != 4:
                                second_line.append(i.name)
                                break
                    if len(second_line) == 4:
                        if len(i.name) <= 6:
                            while len(third_line) != 4:
                                third_line.append(i.name)
                                break

            first_line = first_line1.join(first_line)
            second_line = second_line1.join(second_line)
            third_line = third_line1.join(third_line)

            emoji = self.bot.get_emoji(965978649872441364)
            embed = discord.Embed(colour=self.bot.yellow_colour,timestamp=discord.utils.utcnow())
            embed.add_field(name="__**General information**__",
                            value=f"{emoji} **Tag :** {ctx.author}\n"
                                  f"{emoji} **userid :** ``{ctx.author.id}`` \n"
                                  f"{emoji} **creation date :** <t:{round(int(time.mktime(ctx.author.created_at.timetuple())))}:D>\n"
                                  f"{emoji} **creation age :** <t:{round((int(time.mktime(ctx.author.created_at.timetuple()))))}:R>\n"
                                  f"{emoji} **discord badges :** {badges}\n"
                                  f"{emoji} **bot ? :** {ctx.author.bot}",inline=False)
            embed.add_field(name="__**Server information**__",
                            value=f"{emoji} **nickname :**{ctx.author.nick}\n"
                                  f"{emoji} **top role :** ``{ctx.author.top_role.name}``\n"
                                  f"{emoji} **global permission :** ``admin`` \n"
                                  f"{emoji} **server join date :** <t:{round(int(time.mktime(ctx.author.joined_at.timetuple())))}:D>\n"
                                  f"{emoji} **server join age :** <t:{round(int(time.mktime(ctx.author.joined_at.timetuple())))}:R>\n"
                                  f"{emoji} **role colour :** {ctx.author.top_role.colour}\n"
                                 ,inline=False)
            activity = ""
            if ctx.author.activity is None:
                activity = "none"
            else:
                activity = ctx.author.activity.name
            embed.add_field(name="__**user status**__",
                            value=f"{emoji} **activity :** {activity}\n"
                                  f"{emoji} **status :** ``{ctx.author.status}``\n"
                                  f"{emoji} **timeout? :**``{ctx.author.is_timed_out()}``",inline=False)
            embed.add_field(name=f"__**role[{len(ctx.author.roles)}] top 10**__",
                            value=f"```{first_line}\n{second_line}\n{third_line}```")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            embed.set_author(name=ctx.author,icon_url=ctx.author.avatar.url)
            embed.set_footer(text="\u200b",icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return
        elif memder is not None:
            if ctx.guild.get_member(memder.id) is not None:
                badges = await self.shop(member=memder)
                memder = ctx.guild.get_member(memder.id)
                activity = ""

                a = memder.roles
                a.sort(reverse=True)
                first_line1 = " "
                second_line1 = " "
                third_line1 = " "
                first_line = []
                second_line = []
                third_line = []
                b = " "
                for i in a:
                    if i.name != "@everyone":
                        while len(first_line) != 4:
                            first_line.append(i.name)
                            break
                        if len(first_line) == 4:
                            if len(i.name) <= 6:
                                while len(second_line) != 4:
                                    second_line.append(i.name)
                                    break
                        if len(second_line) == 4:
                            if len(i.name) <= 6:
                                while len(third_line) != 4:
                                    third_line.append(i.name)
                                    break

                first_line = first_line1.join(first_line)
                second_line = second_line1.join(second_line)
                third_line = third_line1.join(third_line)

                emoji = self.bot.get_emoji(965978649872441364)
                embed = discord.Embed(colour=self.bot.yellow_colour, timestamp=discord.utils.utcnow())
                embed.add_field(name="__**General information**__",
                                value=f"{emoji} **Tag :** {memder}\n"
                                      f"{emoji} **userid :** ``{memder.id}`` \n"
                                      f"{emoji} **creation date :** <t:{round(int(time.mktime(memder.created_at.timetuple())))}:D>\n"
                                      f"{emoji} **creation age :** <t:{round((int(time.mktime(memder.created_at.timetuple()))))}:R>\n"
                                      f"{emoji} **discord badges :** {badges}\n"
                                      f"{emoji} **bot ? :** {memder.bot}", inline=False)
                embed.add_field(name="__**Server information**__",
                                value=f"{emoji} **nickname :**{memder.nick}\n"
                                      f"{emoji} **top role :** ``{memder.top_role.name}``\n"
                                      f"{emoji} **global permission :** ``admin`` \n"
                                      f"{emoji} **server join date :** <t:{round(int(time.mktime(memder.joined_at.timetuple())))}:D>\n"
                                      f"{emoji} **server join age :** <t:{round(int(time.mktime(memder.joined_at.timetuple())))}:R>\n"
                                      f"{emoji} **role colour :** {memder.top_role.colour}\n"
                                , inline=False)
                if memder.activity is None:
                    activity = "none"
                else:
                    activity = memder.activity.name
                embed.add_field(name="__**user status**__",
                                value=f"{emoji} **activity :** {activity}\n"
                                      f"{emoji} **status :** ``{memder.status}``\n"
                                      f"{emoji} **timeout? :**``{memder.is_timed_out()}``", inline=False)
                embed.add_field(name=f"__**role[{len(memder.roles)}] top 10**__",
                                value=f"```{first_line}\n{second_line}\n{third_line}```")
                embed.set_thumbnail(url=memder.avatar.url)
                embed.set_author(name=memder, icon_url=memder.avatar.url)
                embed.set_footer(text="\u200b", icon_url=self.bot.user.avatar.url)
                await ctx.send(embed=embed)
                return
            else:
                ban = ""
                badges = await self.shop(member=memder)
                memder = await self.bot.fetch_user(memder.id)
                userbans = [ban_entry.user.id async for ban_entry in ctx.guild.bans()]
                if memder.id in userbans:
                    ban = True
                else:
                    ban=False
                activity = ""
                emoji = self.bot.get_emoji(965978649872441364)
                embed = discord.Embed(colour=self.bot.yellow_colour, timestamp=discord.utils.utcnow())
                embed.add_field(name="__**General information**__",
                                value=f"{emoji} **Tag :** {memder}\n"
                                      f"{emoji} **userid :** ``{memder.id}`` \n"
                                      f"{emoji} **creation date :** <t:{round(int(time.mktime(memder.created_at.timetuple())))}:D>\n"
                                      f"{emoji} **creation age :** <t:{round((int(time.mktime(memder.created_at.timetuple()))))}:R>\n"
                                      f"{emoji} **discord badges :** {badges}\n"
                                      f"{emoji} **bot ? :** {memder.bot}", inline=False)
                embed.add_field(name="__**user status**__",
                                value=f"{emoji} **banned? :**``{ban}``", inline=False)
                embed.set_thumbnail(url=memder.avatar.url)
                embed.set_author(name=memder, icon_url=memder.avatar.url)
                embed.set_footer(text="\u200b", icon_url=self.bot.user.avatar.url)
                await ctx.send(embed=embed)
                return
    @commands.command()
    async def testcommand(self,ctx:commands.Context,member : discord.Member):
        a = member.guild_permissions
        logging.warning(a)
        b = []
        g = ' '
        for key, value in a:
            if value == True:
                b.append(key)
        if member.guild_permissions.administrator or member.guild_permissions.manage_guild:
            g = "admin"
            await ctx.send(g)
            return

        else :
            listt = ['kick_members', 'ban_members','manage_channels','moderate_members','manage_messages','manage_permissions','manage_nicknames','manage_roles','manage_webhooks','manage_threads']
            for i in listt:
                if not i in b:
                    g = 'mod'
                    print("hello")
                    await ctx.send(g)
                    break
                elif not i in b:
                    g = "general"
                    await ctx.send("general")







        logging.warning(b)



    async def shop(self,member:typing.Union[discord.Member,discord.User]):
        emoji = []

        if member.public_flags.hypesquad_bravery:
            bravery = self.bot.get_emoji(979102473073614899)
            emoji.append(str(bravery))
        elif member.public_flags.hypesquad_brilliance:
            bril = self.bot.get_emoji(979102473136525322)
            emoji.append(str(bril))
        elif member.public_flags.hypesquad_balance:
            balance = self.bot.get_emoji(979323502270247022)
            emoji.append(str(balance))
        if member.public_flags.verified_bot_developer:
            botdev = self.bot.get_emoji(979102471500730378)
            emoji.append(str(botdev))
        if member.public_flags.early_supporter:
            early_supporter = self.bot.get_emoji(979326434101317642)
            emoji.append(str(early_supporter))
        if member.public_flags.bug_hunter:
            bug_hunter= self.bot.get_emoji(979330886023643146)
            emoji.append(str(bug_hunter))
        if member.public_flags.staff:
            staff = self.bot.get_emoji(979330886954803200)
            emoji.append(str(staff))

        finale = ''
        if emoji is not None:
            finale = ' '.join([i for i in emoji])
        else:
            finale = "none"
        return finale




async def setup(bot: SussyBot) -> None:
    await bot.add_cog(
        test(bot))
