import logging
import discord
from discord import app_commands, role
from discord.ext import commands , tasks
import os
from discord.utils import get
import aiohttp
import random
from glob import glob
from itertools import cycle
import json
import sqlite3
from cogs.normal import PersistentView
import asyncpg
from asyncpg.pool import create_pool
import asyncio

COGS = [path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")]



"""this is the mai n file that run the bot"""

print(
" eeeee e   e eeeee eeeee e    e    eeeee  eeeee eeeeeee \n "
"8     8   8 8     8     8    8    8    8 8   8   88  \n " 
"8eeee 8   8 8eeee 8eeee 8eeee8    8eee8e 8   8   88  \n"
'     8 8   8     8     8   88      8    8 8   8   88  \n'
" 8ee88 88ee8 8ee88 8ee88   88      88eee8 8eee8   88  \n")


input("are you a robot ?")


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
        with open('prefixes.json', 'r') as f: #we open and read the prefixes.json, assuming it's in the same file
            prefixes = json.load(f) #load the json as prefixes
            return prefixes[str(message.guild.id)]
    except KeyError:

        with open('prefixes.json', 'r') as f:  # read the prefix.json file
            prefixes = json.load(f)            # load the json file

        prefixes[str(message.guild.id)] = '$'  # default prefix

        with open('prefixes.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
            json.dump(prefixes, f, indent=4)   # the indent is to make everything look a bit neater
        with open('prefixes.json', 'r') as t:  ##we open and read the prefixes.json, assuming it's in the same file
            prefixes = json.load(t)

            return prefixes[str(message.guild.id)]
    except :
        return


# async def create_db_pool():


    # self.bot.db = await asyncpg.create_pool(database= "discord", user="postgress", password="galax0")
    # bot.db = await asyncpg.create_pool(dsn='postgres://postgres:galax0@localhost:5432/discord')
    # conn = await asyncpg.connect(user='postgres', password='galax0',
    #                              database='discord', host='127.0.0.1')





class mybot(commands.Bot):
    """the code that run the bot and load prefix"""
    def __init__(self):
        super().__init__(
            command_prefix =(get_prefix),
            case_insensitive= True,
            intents=discord.Intents.all(),
            application_id = 953274927027458148)
        #we use this so the bot doesn't sync commands more than once




    #setup cogs
    async def setup_hook(self):
        print("setting everything up.....")
        """this code load the cogs and commands files"""
        self.add_view(PersistentView())
        COGS = ["normal","messagess","randomapi","calc command","example","error handler"]
        print("loading cogs ....")

        for cog in COGS:
            await self.load_extension(f"cogs.{cog}")
            await bot.tree.sync()


            print(f"{cog} loaded    >>>>>>>>")
        print("setup comelete ...")





    #inform that bot is ready, online
    async def on_ready(self):
        """print client is ready on ready"""
        """conn = psycopg2.connect()
        cur = conn.cursor()
        cur.execute("CREATE TABLE student ();")
        conn.commit()
        cur.close()
        conn.close()"""
        self.change_status.start()
        print("status loop complete")
        print(f"bot is logged as {bot.user}")







    @tasks.loop(seconds=3600)
    async def change_status(self):
        status = cycle(["do not disturb me :)",'$help', 'Green apple', 'amongus', 'SUS', 'bruh', 'ur mom', '0101000101', 'game of life','what do you know about about rolling down in the deep'])
        await bot.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.watching,name=next(status)))



    #load the prefix on guild join
    async def on_guild_join(self,guild):  # when the bot joins the guild

        with open('prefixes.json', 'r') as f:  # read the prefix.json file
            prefixes = json.load(f)  # load the json file
        prefixes[str(guild.id)] = '$'  # default prefix
        with open('prefixes.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
            json.dump(prefixes, f, indent=4)  # the indent is to make everything look a bit neater
        print(f"{guild.name} prefix loaded")
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

        a = ["keep your mouth close",
             " dont disturb me :)",
             "stfu",
             "shut your mouth",
             "you smell",
             "nuts?",
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
            "ummmm u suck",
             "joe mama",
             "retard"
        ]
        message_in = message.content

        print(f"{message.guild} {message.channel} : {message.author}: {message.author.display_name}: {message.content}")

        if message.author.bot:
            return
        elif message_in.lower().find('sus') != -1:
            await message.channel.send("amongus", delete_after=10)

        elif (bot.user in message.mentions) and message_in.lower().find('prefix') != -1:
            v =await self.get_prefix(message)
            embed = discord.Embed(title=f"YO :wave:  my prefix is {v}", )

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


            elif message_in.lower().find('hi') != -1 or message_in.lower().find('helo') != -1 or message_in.lower().find('sup') != -1  or message_in.lower().find(
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
bot.remove_command("help")
bot.run(token)




