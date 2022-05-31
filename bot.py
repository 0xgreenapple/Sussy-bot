import os
import time
import json
import asyncio
import datetime
import aiohttp
import discord
import dotenv
import random

from glob import glob
from itertools import cycle
from handler.database import create_database_pool
from platform import python_version
from discord.ext import commands, tasks
from discord.app_commands import CommandTree
from datetime import timedelta
from pympler.tracker import SummaryTracker

dotenv.load_dotenv()

"""this is the main file that run the bot"""

tracker = SummaryTracker()
print(
    " .d8888b.  888     888  .d8888b.   .d8888b. Y88b   d88P      888888b.    .d88888b. 88888888888\n"
    "d88P  Y88b 888     888 d88P  Y88b d88P  Y88b Y88b d88P       888  88b   d88P   Y88b    888    \n"
    "Y88b.      888     888 Y88b.      Y88b.       Y88o88P        888  .88P  888     888    888    \n"
    "  Y888b.   888     888   Y888b.    Y888b.      Y888P         8888888K.  888     888    888    \n"
    "     Y88b. 888     888      Y88b.     Y88b.     888          888   Y88b 888     888    888    \n"
    "       888 888     888        888       888     888          888    888 888     888    888    \n"
    "Y88b  d88P Y88b. .d88P Y88b  d88P Y88b  d88P    888          888  d88P  Y88b. .d88P    888    \n"
    "  Y8888P     Y88888P     Y8888P     Y8888P      888          8888888P     Y88888P      888    \n"

)


def get_prefix(client, message):  ##first we define get_prefix
    """load prefix function"""
    try:
        with open('data/prefixes.json',
                  'r') as f:  # we open and read the prefixes.json, assuming it's in the same file
            prefixes = json.load(f)  # load the json as prefixes
            return prefixes[str(message.guild.id)]
    except KeyError:

        with open('data/prefixes.json', 'r') as f:  # read the prefix.json file
            prefixes = json.load(f)  # load the json file

        prefixes[str(message.guild.id)] = '$'  # default prefix

        with open('data/prefixes.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
            json.dump(prefixes, f, indent=4)  # the indent is to make everything look a bit neater
        with open('data/prefixes.json',
                  'r') as t:  ##we open and read the prefixes.json, assuming it's in the same file
            prefixes = json.load(t)

            return prefixes[str(message.guild.id)]
    except:
        return


# class bot the main code
class SussyBot(commands.AutoShardedBot):
    user: discord.ClientUser
    bot_app_info: discord.AppInfo
    """the code that run the bot and load prefix"""

    def __init__(self):
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        self.ready = False
        self.statues = cycle(
            ["do not disturb me :)", '$help', 'Green apple', 'amongus', 'SUS', 'bruh', 'ur mom', '0101000101',
             'game of life', 'what do you know about about rolling down in the deep'])
        super().__init__(
            command_prefix=(get_prefix),
            case_insensitive=True,
            intents=discord.Intents.all(),
            application_id=976086412313120798,
            help_command=None
        )
        # CUSTOM

        self.online_time = datetime.datetime.now(datetime.timezone.utc)
        self.version = "0.0.11"
        self.owner_id = 888058231094665266
        self.console_message_prefix = "Sussy bot"
        self.changelog = "https://discord.gg/wC37kY3qwH"
        self.dashboard = "https://sussybot.xyz"
        self.fake_ip = "ur mother"
        self.fake_location = "new-york"
        self.simple_user_ageent = "Sussybot (Discord Bot)"
        self.user_agent = (
            "Sussybot (Discord Bot) "
            f"Python/{python_version()} "
            f"aiohttp/{aiohttp.__version__}"
            f"discord.py/{discord.__version__}"
        )
        # colours
        self.bot_color = self.bot_colour = 0xff0047
        self.embed_default_colour = self.embed_default_colour = 0x00ffad
        self.pink_color = self.pink_colour = 0xff0f8c
        self.blue_color = self.blue_colour = 0x356eff
        self.red_color = self.red_colour = 0xff0047
        self.cyan_color = self.cyan_colour = 0x00ffad
        self.dark_theme_background_colour = self.dark_theme_background_colour = 0x36393e
        self.white_color = self.white_colour = 0xffffff
        self.black_color = self.white_colour = 0x000000
        self.youtube_color = self.youtube_colour = 0xcd201f
        self.violet_color = self.violet_colour = 0xba9aeb
        self.green_color = self.green_colour = 0x00ff85
        self.yellow_color = self.yellow_colour = 0xffe000

        # global permissions
        self.regular_permission = [""]
        """self.bug_hunter_emoji = self.get_emoji()
        self.bravery_emoji = self.get_emoji()
        discord.Member.public_flags.hypesquad_bravery"""

        # database
        self.db = self.database = self.database_connection_pool = None
        self.connected_to_database = asyncio.Event()
        self.connected_to_database.set()

    # load cogs from other files
    async def setup_hook(self) -> None:
        self.aiohttp_session = aiohttp.ClientSession(loop=self.loop)
        self.print("client session start")
        self.bot_app_info = await self.application_info()
        self.owner_id = self.bot_app_info.owner.id
        self.print("setting up database")
        await self.initialize_database()
        self.print("database setup done")
        self.loop.create_task(self.startup_tasks(), name="Bot startup tasks")

        COGS = ["calc command","error handler","messagess","normal","randomapi","Tenor","unsplash"]
        self.print("loading cogs..")
        for cog in COGS:
            await self.load_extension(f"cogs.{cog}")
            self.print(f"{cog} loaded ")
        self.print("setup hook complete")

    # connect to database execute on setup hook
    async def connect_to_database(self):
        if self.database_connection_pool:
            return
        if self.connected_to_database.is_set():
            self.connected_to_database.clear()
            self.db = self.database = self.database_connection_pool = await create_database_pool()
            self.connected_to_database.set()
        else:
            await self.connected_to_database.wait()

    # setup database and create tables
    async def initialize_database(self):
        await self.connect_to_database()
        await self.db.execute("CREATE SCHEMA IF NOT EXISTS chat")
        await self.db.execute("CREATE SCHEMA IF NOT EXISTS guilds")
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS chat.messagecount(
               guild_id         BIGINT,
               user_id          BIGINT,
               message          INT,
               PRIMARY KEY		(guild_id, user_id)
                                
            )
            """
        )
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS guilds.welcome_message (
                guild_id		BIGINT PRIMARY KEY,
                channel_id      BIGINT,
                message		    Text
            )
            """
        )
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS guilds.prefixes (
                guild_id		BIGINT PRIMARY KEY,
                prefixes		    TEXT
            )
            """
        )
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS guilds.blacklist (
                guild_id        BIGINT PRIMARY KEY
            )
            """
        )

    def print(self, message):
        print(f"[{datetime.datetime.now().isoformat()}] > {self.console_message_prefix} > {message}")

    # do ready tasks
    @property
    async def app_info(self):
        if not hasattr(self, "_app_info"):
            self._app_info = await self.application_info()
        return self._app_info

    @property
    def owner(self) -> discord.User:
        return self.bot_app_info.owner

    # the code that change bot status in every hour.
    async def on_ready(self):
        self.print(f"is shard is rate limited :{self.is_ws_ratelimited()}")

        if not hasattr(self, 'uptime'):
            self.startTime = time.time()
        if not self.ready:
            self.ready = True
            self.print(f"bot is logged as {self.user}")
        else:
            self.print(f'{self.user}bot reconnected.')

    def reply(self, content, *args, **kwargs):
        return self.send(f"{self.author.display_name}:\n{content}", **kwargs)

    @tasks.loop(hours=1)
    async def change_status(self):
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Activity(type=discord.ActivityType.playing,
                                                             name=next(self.statues)))

    async def on_shard_ready(self, shard_id):
        self.print(f"{shard_id} ready the latency {self.latency}")

    # load the prefix on guild join
    async def on_guild_join(self, guild):  # when the bot joins the guild
        await self.db.execute(
            """
            INSERT INTO guilds.prefixes (guild_id, prefixes)
            VALUES ($1, $2)
            ON CONFLICT (guild_id) DO NOTHING
            """,
            guild.id, "$"
        )
        with open('data/prefixes.json', 'r') as f:  # read the prefix.json file
            prefixes = json.load(f)  # load the json file
        prefixes[str(guild.id)] = '$'  # default prefix
        with open('data/prefixes.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
            json.dump(prefixes, f, indent=4)  # the indent is to make everything look a bit neater
        print(f"{guild.name} prefix loaded")
        """send to support server that bot is joined the guild"""

    # pop the guild prefix on leaving from the guild
    async def on_guild_remove(self, guild):
        await self.db.execute(
            """
            DELETE FROM guilds.prefixes 
            WHERE guild_id = $1
            """,
            guild.id
        )
        with open('data/prefixes.json', 'r') as f:  # read the file
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))
        with open('data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    async def startup_tasks(self):
        await self.wait_until_ready()
        await self.change_status.start()

    async def start(self) -> None:
        await super().start(token, reconnect=True)

    async def close(self) -> None:
        try:
            self.print(f"closing bot session")
            await self.aiohttp_session.close()
        except Exception as e:
            print(e)
        try:
            self.print(f"closing the bot")
            await super().close()
        except Exception as e:
            print(e)

    # bot monitor
    async def on_resumed(self):
        """print when client resumed"""
        self.print(f"{self.user} [resumed]")

    async def on_connect(self):
        """print when client connected to discord"""
        self.print(f"{self.user} is connected successfully")

    async def on_disconnect(self):
        """print when client disconnected to discord"""
        self.print(f"{self.user} is disconnected")

    # bot events monitor shards
    async def on_shard_resumed(self, shard_id: int):
        """print when shard resumed"""
        self.print(f" {self.user} shard :{shard_id} resumed with latency {self.latency}")

    async def on_shard_disconnect(self, shard_id: int):
        """print when shard disconnect"""
        self.print(f"{shard_id} has been disconnected")

    # shutdown task
    async def shutdown_tasks(self):
        """shutdown the database connection"""
        # Close database connection
        await self.database_connection_pool.close()

    # this is the code that make the bot automaticly respose on ping
    async def on_message(self, message):

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
             "What you want to me",
             "red was the imposter",
             "yo! you looking nice today :)",
             "hmm tell me who is baka",
             "joe mama",
             "retard"
             ]
        message_in = message.content
        # logging
        """self.print(f"{message.guild} {message.channel} : {message.author}: {message.author.display_name}: {message.content}")"""

        if message.author.bot:
            return
        elif message_in.lower().find('sus') != -1:
            await message.channel.send("amongus", delete_after=10)

        elif (self.user in message.mentions) and message_in.lower().find('prefix') != -1:
            v = await self.get_prefix(message)
            embed = discord.Embed(title=f"YO :wave:  my prefix is {v}", )

            await message.channel.send(embed=embed)
        elif self.user in message.mentions:
            if message_in.lower().find('amongus') != -1 or message_in.lower().find(
                    'cool') != -1 or message_in.lower().find('good') != -1 or message_in.lower().find('nice') != -1:
                await message.channel.send(f'amongus')

            elif message_in.lower().find('bad') != -1 or message_in.lower().find(
                    'horrible') != -1 or message_in.lower().find('suck') != -1 or message_in.lower().find(
                'terrible') != -1 or message_in.lower().find('waste') != -1 or message_in.lower().find(
                'fk') != -1 or message_in.lower().find('fuck') != -1:
                await message.channel.send(f'ur mom', delete_after=11)

            elif message_in.lower().find('hi') != -1 or message_in.lower().find(

                    'helo') != -1 or message_in.lower().find('sup') != -1 or message_in.lower().find(
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
        await self.process_commands(message)


token = os.environ.get('BETATOKEN')
application_id = os.environ.get('BETA_APPLICATION_ID')
tracker.print_diff()
print("")
