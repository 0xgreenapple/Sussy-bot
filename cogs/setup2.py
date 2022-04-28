import asyncio

import discord
from discord.ext import commands
import random
import json


import logging

class setup2(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot




    """def get_welcome(self,member):  ##first we define get_prefix
        with open('welcome.json', 'r') as f:  ##we open and read the prefixes.json, assuming it's in the same file
            msg = json.load(f)  # load the json as prefixes
        return msg[str(member.guild.id)]"""






    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def setup(self, ctx):
        embed = discord.Embed(title="setup",description="setting everything up.....")
        embed.add_field(name="setting logs channel",value="creating.....")
        embed.add_field(name="setting mute role",value="creating.....",inline=False)

        embed2 = discord.Embed(title="setup",description="setting everything Ip..")
        embed2.add_field(name="setting logs channel",value="done")
        embed2.add_field(name="setting mute role", value="creating.....",inline=False)

        embed3 = discord.Embed(title="setup", description="setup complete")
        embed3.add_field(name="setting logs channel", value="done")
        embed3.add_field(name="setting mute role", value="done", inline=False)
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.author: discord.PermissionOverwrite(view_channel=True),
        }
        message = await ctx.send(embed=embed)
        channel = await ctx.guild.create_text_channel('sussy-bot-logs', overwrites=overwrites)
        edit1 = await message.edit(embed=embed2)
        muterole = await ctx.guild.create_role(name="Imposter", permissions=discord.Permissions(send_messages=False,add_reactions=False,connect=False))
        await edit1.edit(embed=embed3)


    @setup.command()
    async def welcome(self, ctx, channel:discord.TextChannel, *, message:str):
        embed = discord.Embed(title="welcome message",description=message)
        with open('welcome.json', 'r') as f:  # read the prefix.json file
            msg = json.load(f)
        msg[str(ctx.guild.id)] = {}
        msg[str(ctx.guild.id)]["channel"]=int(channel.id)
        msg[str(ctx.guild.id)]["message"]=str(message)
        with open('welcome.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
            json.dump(msg, f, indent=4)
        await ctx.send("rule done")

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self,member):
        with open("welcome.json", 'r') as f:
            users = json.load(f)
        channelid = users[str(member.guild.id)]["channel"]
        message = users[str(member.guild.id)]["message"]
        embed= discord.Embed(title=member.name,description=f"**{message}**")
        channel = await self.bot.fetch_channel(channelid)

        await channel.send(embed=embed)

async def setup(bot: commands.Bot ) -> None:
    await bot.add_cog(
        setup2(bot))
