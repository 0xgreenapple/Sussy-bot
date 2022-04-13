import logging
import os
import discord
import aiohttp
import random
from requests import get
from discord.ext import commands



class bad(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        badwords = ["anal", "anus", "arse," "bitch", "ballsack", "bastard", "boob", "boobs", "buttplug",
                    "cock", "cum", "cunt", "dick", "dildo", "nigga", "nigger", "pussy", "pube", "sex", "tit", "vagina",
                    "tits", "asshat", "penis", "asshole", "slurs", "piss"]

        if message.content.lower() in badwords:
            embed = discord.Embed(title="warning",description=f"**pls dont use bad words in {message.guild.name}**"
                                                              f"\n"
                                                              f"you used ||{message.content}||")
            await message.channel.send("watch your mouth")
            await message.delete()
            channel = await message.author.create_dm()

            await channel.send(embed=embed)


















async def setup(bot):
    await bot.add_cog(bad(bot))