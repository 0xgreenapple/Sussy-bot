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

def setup(client):
    client.add_cog(bad(client))
