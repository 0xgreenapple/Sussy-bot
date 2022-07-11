import logging

import discord
from discord.ext import commands
from bot import SussyBot
from discord.ext.commands import cooldown, BucketType
from handler.topics import topic1
import random
from itertools import cycle


class member(commands.Cog):
    def __init__(self, bot: SussyBot) -> None:
        self.bot = bot
        self.topicss = topic1
    @commands.command()
    @commands.guild_only()
    @cooldown(1,3600,BucketType.guild)
    async def deadchat(self, ctx:commands.Context):

        a = ctx.guild.get_role(983346963024060426)
        logging.warning("yes")
        logging.warning(a)
        await ctx.reply(f'{a.mention} make this sussy chat active,**{random.choice(topic1)}**')

    @commands.command()
    @commands.guild_only()
    @cooldown(1, 5, BucketType.user)
    async def topic(self, ctx: commands.Context):
        await ctx.reply(f"**{random.choice(topic1)}**")

    @deadchat.error
    async def deadchaterror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply("command on cooldown")




async def setup(bot: SussyBot) -> None:
    await bot.add_cog(
        member(bot))
