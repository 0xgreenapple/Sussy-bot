"""
Sussy-bot main runner
~~~~~~~~~~~~~~~~~~~
starter of the sussy bot for discord py
that start the bot and connect to discord.
:copyright: (c) xgreenapple
:license: MIT.
"""
__title__ = 'Sussy-bot'
__author__ = 'xgreenapple'
__copyright__ = 'Copyright xgreenapple'
__version__ = '0.0.1a'

import logging
import os
import time
import json
import asyncio
import datetime
from collections import Counter

import aiohttp
import discord
import certifi
import ssl
import dotenv
import random
import contextlib

from glob import glob
from itertools import cycle

from handler.Context import Context
from handler.database import create_database_pool
from platform import python_version
from discord.ext import commands, tasks
from datetime import timedelta
from discord import http, gateway, client
from discord.client import Client
from pympler.tracker import SummaryTracker

"""this is the main file that run the bot"""
log = logging.getLogger(__name__)
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


# class bot the main code
class SussyBot(commands.Bot):
    """Sussy-bot v0.1.9 Interface
    """

    user: discord.ClientUser
    bot_app_info: discord.AppInfo
    owner: 888058231094665266

    """the code that run the bot and load prefix"""

    def __init__(self):

        allowed_mentions = discord.AllowedMentions(roles=True, everyone=False, users=True)
        self.ready = False
        self.statues = cycle(
            ["Technoblade never dies", "so long, blood god", 'long live the blood god', 'rest in peace king'])
        super().__init__(
            command_prefix=self.get_command_prefix,
            case_insensitive=True,
            intents=discord.Intents(
                messages=True,
                bans=True,
                members=True,
                emojis=True,
                guilds=True,
                message_content=True,

            ),

            application_id=976086412313120798,
            help_command=None,
        )
        # variables

        self.online_time = datetime.datetime.now(datetime.timezone.utc)
        self.spam_cooldown = commands.CooldownMapping.from_cooldown(5.0, 6.0, commands.BucketType.user)
        self.spam_count = Counter()
        self.version = "0.0.1a"
        self.owner_id = 888058231094665266
        self.support_guild = 939208771929014372
        self.message_prefix_s = "Sussy bot"
        self.changelog = "https://discord.gg/wC37kY3qwH"
        self.dashboard = "https://sussybot.xyz"
        self.bot_user_agent = "Sussybot (Discord Bot)"
        self.user_agent = (
            "Sussybot "
            f"Python/{python_version()} "
            f"aiohttp/{aiohttp.__version__}"
            f"discord.py/{discord.__version__}"
        )

        # colours
        self.bot_color = 0xa68ee3
        self.pink_color = 0xff0f8c
        self.blue_color = 0x356eff
        self.embed_colour = 0x2E3136
        self.cyan_color = 0x00ffad
        self.white_color = 0xffffff
        self.black_color = 0x000000
        self.youtube_color = 0xcd201f
        self.violet_color = 0xba9aeb
        self.green_color = 0x00ff85
        self.yellow_color = 0xffe000
        self.embed_default_colour = 0x00ffad
        self.dark_theme_colour = 0x36393e

        # Emojis
        self.channel_emoji = '<:channel:990574854027743282>'
        self.search_emoji = '<:icons8search100:975326725472944168>'
        self.failed_emoji = '<:icons8closewindow100:975326725426778184>'
        self.success_emoji = '<:icons8ok100:975326724747304992>'
        self.right = '<:icons8chevronright100:975326725158346774>'
        self.file_emoji = '<:icons8document100:975326725229641781>'

        # DATABASE variables
        self.db = self.database = self.database_connection_pool = None
        self.connected_to_database = asyncio.Event()
        self.connected_to_database.set()

    # load cogs from other files

    async def setup_hook(self) -> None:

        self.aiohttp_session = aiohttp.ClientSession(loop=self.loop)
        self.console_log("client session start")
        self.bot_app_info = await self.application_info()
        self.owner_id = self.bot_app_info.owner.id
        self.console_log("setting up database")
        await self.initialize_database()
        self.console_log("database setup done")
        self.loop.create_task(
            self.startup_tasks(), name="Bot startup tasks"
        )
        COGS = ["error handler", 'moderation', 'test','member']
        self.console_log("loading cogs..")
        for cog in COGS:
            await self.load_extension(f"cogs.{cog}")
            self.console_log(f"{cog} loaded ")
        # await self.tree.sync()
        # self.tree.copy_global_to(guild=discord.Object(self.support_guild))
        self.console_log("setup hook complete")

    # connect to database execute on setup hook, inspired by harmon bot
    async def connect_to_database(self):
        print('connecto to database')
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
        print('dataase intialzie')
        await self.connect_to_database()
        await self.db.execute("CREATE SCHEMA IF NOT EXISTS test")
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS test.messagecount(
               guild_id         BIGINT,
               user_id          BIGINT,
               message          INT,
               PRIMARY KEY		(guild_id, user_id)

            )
            """
        )

        # await self.db.execute("CREATE SCHEMA IF NOT EXISTS chat")
        # await self.db.execute("CREATE SCHEMA IF NOT EXISTS commands")
        await self.db.execute("CREATE SCHEMA IF NOT EXISTS guilds")
        # await self.db.execute("CREATE SCHEMA IF NOT EXISTS direct_messages")
        # await self.db.execute("CREATE SCHEMA IF NOT EXISTS test")
        # await self.db.execute("CREATE SCHEMA IF NOT EXISTS moderation")
        # await self.db.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS chat.messagecount(
        #        guild_id         BIGINT,
        #        user_id          BIGINT,
        #        message          INT,
        #        PRIMARY KEY		(guild_id, user_id)
        #
        #     )
        #     """
        # )
        # await self.db.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS guilds.welcome_message (
        #         guild_id		BIGINT PRIMARY KEY,
        #         channel_id      BIGINT,
        #         message		    Text
        #     )
        #     """
        # )
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS guilds.prefixes (
                guild_id		BIGINT,
                prefixes		TEXT,
                PRIMARY KEY     (guild_id)
                
            )
            """
        )
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS test.users (
                id              BIGINT,
                blacklisted     boolean DEFAULT FALSE,
                PRIMARY KEY (id)
            )
            """
        )
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS test.guilds (
                id       		BIGINT,
                blacklisted     boolean DEFAULT FALSE,
                prefix          TEXT,
                PRIMARY KEY (id)
            )
            """
        )
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS test.warns (
                id              serial,
                time            TIMESTAMP DEFAULT NOW() NOT NULL,
                warning         TEXT,
                user_id         BIGINT,
                guild_id        BIGINT,
                FOREIGN KEY (user_id) REFERENCES test.users(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (guild_id) REFERENCES test.guilds(id) ON DELETE CASCADE ON UPDATE CASCADE
            )
            """
        )
        await self.db.execute("""DROP FUNCTION IF EXISTS test.warnfunc""")
        await self.db.execute(
            f"""
                    CREATE OR REPLACE FUNCTION test.warnfunc(BIGINT,BIGINT,TEXT) RETURNS integer
                    AS $$
                        DECLARE user_id1 BIGINT = $1;
                        DECLARE guild_id1 BIGINT = $2;
                        DECLARE warning1 TEXT = $3;
                        DECLARE warnid BIGINT;
                    BEGIN
                        IF EXISTS(SELECT * FROM test.users WHERE id = user_id1)
                        AND EXISTS(SELECT * FROM test.guilds WHERE id = guild_id1) THEN
                            INSERT INTO test.warns(user_id,guild_id,warning)
                            VALUES(user_id1,guild_id1,warning1) RETURNING id INTO warnid;
                        ELSE
                            INSERT INTO test.users(id)
                            VALUES(user_id1) ON CONFLICT DO NOTHING;
                            INSERT INTO test.guilds(id)
                            VALUES(guild_id1) ON CONFLICT DO NOTHING;
                            INSERT INTO test.warns(user_id,guild_id,warning)
                            VALUES(user_id1,guild_id1,warning1) RETURNING id INTO warnid;
                    END IF;
                    RETURN warnid;
                    END $$ LANGUAGE plpgsql;

                    """)
        # await self.db.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS guilds.blacklist (
        #         guild_id        BIGINT PRIMARY KEY
        #     )
        #     """
        # )
        # await self.db.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS moderation.warns (
        #         guild_id         BIGINT,
        #         user_id          BIGINT,
        #         datetime       TIMESTAMP,
        #         warn             TEXT[],
        #         totalwarn        BIGINT,
        #         PRIMARY KEY		 (guild_id, user_id)
        #     )
        #     """
        # )
        # await self.db.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS guilds.checks (
        #         guild_id        BIGINT PRIMARY KEY,
        #         name            TEXT,
        #         settings        BOOL
        #     )
        #     """
        # )
        # await self.db.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS test.datetime (
        #         user_id        BIGINT PRIMARY KEY,
        #         datetime       TIMESTAMP
        #     )
        #     """
        # )

    def console_log(self, message):
        print(f"[{datetime.datetime.now().strftime(r'%D %I:%M %p')}] > {self.user} > {message}")

    # do ready tasks
    @property
    async def app_info(self):
        if not hasattr(self, "_app_info"):
            self._app_info = await self.application_info()
        return self._app_info

    @property
    def owner(self) -> discord.User:
        return self.bot_app_info.owner

    async def dm_member(self, user: discord.Member, *args, message=None, embed=None, file=None, view=None, **kwargs):
        channel = await user.create_dm()
        await channel.send(content=message, embed=embed, file=file, view=view)

    @staticmethod
    async def get_command_prefix(bot, message: discord.Message):
        prefixes = "$"
        if message.channel.type is not discord.ChannelType.private:
            prefixes = await bot.db.fetchval(
                """
                    SELECT prefix
                    FROM test.guilds
                       WHERE id = $1
                    """,
                message.guild.id
            )

        return prefixes if prefixes else "$"

    # the code that change bot status in every hour.
    async def on_ready(self):
        self.console_log(f"is shard is rate limited :{self.is_ws_ratelimited()}")

        if not hasattr(self, 'uptime'):
            self.startTime = time.time()
        if not self.ready:
            self.ready = True
            self.console_log(f"bot is logged as {self.user}")
        else:
            self.console_log(f'{self.user}bot reconnected.')

    @tasks.loop(minutes=15)
    async def change_status(self):
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Activity(
                                       type=discord.ActivityType.listening,
                                       name=next(self.statues)), )

    # load the prefix on guild join
    async def on_guild_join(self, guild):  # when the bot joins the guild
        await self.db.execute(
            """
            INSERT INTO test.guilds (id, prefixe)
            VALUES ($1, $2)
            ON CONFLICT (guild_id) DO NOTHING
            """,
            guild.id, "$"
        )

        """send to support server that bot is joined the guild"""

    # pop the guild prefix on leaving from the guild
    async def on_guild_remove(self, guild):
        await self.db.execute(
            """
            DELETE FROM test.guild 
            WHERE guild_id = $1
            """,
            guild.id
        )

    async def startup_tasks(self):
        await self.wait_until_ready()
        await self.change_status.start()

    async def start(self) -> None:
        await super().start(token, reconnect=True, )

    async def close(self) -> None:
        try:
            self.console_log(f"closing bot session")
            await self.aiohttp_session.close()
        except Exception as e:
            print(e)
        try:
            self.console_log(f"closing the bot")
            await super().close()
        except Exception as e:
            print(e)

    async def process_commands(self, message: discord.Message):
        ctx = await self.get_context(message)

        if ctx.command is None:
            return

        if ctx.author.bot:
            return

        # bucket = self.spam_cooldown.get_bucket(message)
        # current = message.created_at.timestamp()
        # retry_after = bucket.update_rate_limit(current)
        # author_id = message.author.id
        # if retry_after:
        #     self.spam_count[author_id] += 1
        # logging.warning(self.spam_count)
        await self.invoke(ctx)

    # bot monitor
    async def on_resumed(self):
        """print when client resumed"""
        self.console_log(f"{self.user} [resumed]")

    async def on_connect(self):
        """print when client connected to discord"""
        self.console_log(f"{self.user} is connected successfully")

    async def on_disconnect(self):
        """print when client disconnected to discord"""
        self.console_log(f"{self.user} is disconnected")

    # shutdown task
    async def shutdown_tasks(self):
        """shutdown the database connection"""
        # Close database connection
        await self.database_connection_pool.close()

    async def get_context(self, message, /, *, cls=Context) -> Context:
        ctx = await super().get_context(message, cls=cls)
        return ctx

    # this is the code that make the bot automatically response on ping
    async def on_message(self, message):

        if message.channel.type is not discord.ChannelType.private:
            check = True
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
            if check == True or check == None:
                message_in = message.content
                # logging
                """self.print(f"{message.guild} {message.channel} : {message.author}: {message.author.display_name}: 
                {message.content}") """

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
                            'cool') != -1 or message_in.lower().find('good') != -1 or message_in.lower().find(
                        'nice') != -1:
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
