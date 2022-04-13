import logging

import discord
from discord import app_commands, role
from discord.ext import commands , tasks
import os
import aiohttp
import random
from glob import glob
from itertools import cycle
import json

from cogs.normal import PersistentView

COGS = [path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")]



"""this is the mai n file that run the bot"""
class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self,cog,False)
    def ready_up(self,cog):
        setattr(self,cog,True)
        print(f"{cog} is ready")


    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


def get_prefix(client, message): ##first we define get_prefix
    """load prefix function"""
    try:

        with open('prefixes.json', 'r') as f: ##we open and read the prefixes.json, assuming it's in the same file
            prefixes = json.load(f) #load the json as prefixes
            return prefixes[str(message.guild.id)]

    except KeyError:

        with open('prefixes.json', 'r') as f:  # read the prefix.json file
            prefixes = json.load(f)  # load the json file

        prefixes[str(message.guild.id)] = '$'  # default prefix

        with open('prefixes.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
            json.dump(prefixes, f, indent=4)  # the indent is to make everything look a bit neater
        with open('prefixes.json', 'r') as t: ##we open and read the prefixes.json, assuming it's in the same file
            prefixes = json.load(t)

            return prefixes[str(message.guild.id)]
    except :
        return



class mybot(commands.Bot):
    """the code that run the bit and load prefix"""
    def __init__(self):
        super().__init__(
            command_prefix = (get_prefix),
            intents=discord.Intents.all(),
            application_id = 953274927027458148)
        #we use this so the bot doesn't sync commands more than once

    #setup cogs
    async def setup_hook(self):
        """this code load the cogs and commands files"""
        self.add_view(PersistentView())
        COGS = ["normal","randomapi"]
        for cog in COGS:
            await self.load_extension(f"cogs.{cog}")
            await bot.tree.sync()
            print(f"{cog} loaded.")
    #inform that bot is ready, online
    async def on_ready(self):
        """print client is ready on ready"""
        await bot.change_presence(activity=discord.Game(name="green apple"))
        self.change_status.start()
        print(f"We have logged in as {self.user}.")

    #change the status as time pass
    @tasks.loop(seconds=3600)
    async def change_status(self):
        status = cycle(['$help', 'Green apple', 'amongus', 'SUS', 'bruh', 'ur mom', '0101000101', 'game of life'])
        await bot.change_presence(activity=discord.Game(next(status)))

        #load the prefix on guild join
    async def on_guild_join(self,guild):  # when the bot joins the guild
        with open('prefixes.json', 'r') as f:  # read the prefix.json file
            prefixes = json.load(f)  # load the json file

        prefixes[str(guild.id)] = '$'  # default prefix

        with open('prefixes.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
            json.dump(prefixes, f, indent=4)  # the indent is to make everything look a bit neater

        """send to support server that bot is joined the guild"""
        channel = await bot.fetch_channel(960863076821905478)
        embed = discord.Embed(title=f"i joind the {guild.name} server")
        await channel.send(embed=embed)

    async def on_guild_remove(self,guild):  # when the bot is removed from the guild
        with open('prefixes.json', 'r') as f:  # read the file
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))  # find the guild.id that bot was removed from

        with open('prefixes.json', 'w') as f:  # deletes the guild.id as well as its prefix
            json.dump(prefixes, f, indent=4)
        channel = await bot.fetch_channel(960863137706442812)
        embed = discord.Embed(title=f"i left the {guild.name} server")
        await channel.send(embed=embed)

    async def on_message(self,message):
        a = [
            "why you pinged me ",
            "among us",
            "go outside touch some grass",
            "ur mom",
            "imposter was ejected",
            "you are sus",
            "SUS",
            "Wtf you want to me",
            "red was the imposter",
            "f you kid",
            "what the fuck! you looking nice today :)",
            "hmm tell me who is baka",
            "ummmm u suck"
        ]
        message_in = message.content

        channel = bot.get_channel('952460342313758760')
        print(f"{message.guild} {message.channel} : {message.author}: {message.author.display_name}: {message.content}")
        sussyserver_guild = bot.get_guild(917471209329946695)

        if message.author.bot:
            return
        elif message_in.lower().find('sus') != -1:
            await message.channel.send("amongus", delete_after=10)

        elif (bot.user in message.mentions) and message_in.lower().find('prefix') != -1:
            embed = discord.Embed(title=f"YO :wave:  my prefix is ", )

            await message.channel.send(embed=embed)
        elif bot.user in message.mentions:
            if message_in.lower().find('amongus') != -1 or message_in.lower().find(
                    'cool') != -1 or message_in.lower().find('good') != -1 or message_in.lower().find('nice') != -1:
                await message.channel.send(f'amongus')


            elif message_in.lower().find('bad') != -1 or message_in.lower().find(
                    'horrible') != -1 or message_in.lower().find('suck') != -1 or message_in.lower().find(
                'terrible') != -1 or message_in.lower().find('waste') != -1 or message_in.lower().find(
                'fk') != -1 or message_in.lower().find('fuck') != -1:
                await message.channel.send(f'ur mom', delete_after=11)


            elif message_in.lower().find('hi') != -1 or message_in.lower().find(
                    'hello') != -1 or message_in.lower().find('sup') != -1 or message_in.lower().find(
                'yo') != -1 or message_in.lower().find('hola') != -1 or message_in.lower().find(
                'ello') != -1 or message_in.lower().find('yes') != -1:
                await message.channel.send(f'**hello there how are you?**')


            elif message_in.lower().find('how are you') != -1:
                await message.channel.send(f'I can smell sus,btw how about you {message.author.display_name} ?')


            elif message_in.lower().find('ur mom') != -1:
                await message.channel.send(f'ur mom in my basement, {message.author.display_name}')


            elif message_in.lower().find('ur dad') != -1:
                await message.channel.send(f'shut up YOU, {message.author.display_name}')


            elif message_in.lower().find('fuck you') != -1:
                await message.channel.send(f'f you too, {message.author.display_name}')


            elif message_in.lower().find('what do you do for living') != -1:
                await message.channel.send(f'i eat bananas , {message.author.display_name}')


            else:
                await message.channel.send(f'{random.choice(a)}, **{message.author.display_name}**!')

        await bot.process_commands(message)

"""===================================================================================================="""
token = os.environ['TOKEN']
bot = mybot()
bot.run(token)



