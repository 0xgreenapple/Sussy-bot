import logging
import os
import discord
import aiohttp
import random
import asyncio
from requests import get
from discord.ext import commands



class trivia(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def trv(self,ctx):
        question = "what"
        answer = "yes"
        await ctx.send(question)

        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel

        try:
            message, author = self.client.wait_for('message', check=check, timeout=60)
            if message.content == answer:
                await ctx.send('Answer correct.')
            else:
                await ctx.send('Answer wrong')
        except asyncio.TimeoutError:
            await ctx.send('Times out')






def setup(client):
    client.add_cog(trivia(client))

