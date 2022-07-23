from enum import Enum

import discord
import subprocess

import ssl

import os
from discord.app_commands import checks, Choice
from discord.ext import commands

from pympler.tracker import SummaryTracker
import contextlib

class True_Or_False(Enum):
    true = 'true'
    false = 'false'
tracker = SummaryTracker()
if __name__ == "__main__":
    import logging
    import typing
    import sys
    from bot import SussyBot
    from handler import errors
    from discord import app_commands
    from handler.checks import owner_only
    from handler.Context import heloo
    from handler import utils
    import asyncio

    client = SussyBot()


    @client.check
    async def is_permitted(ctx):
        me = ctx.guild.me if ctx.guild is not None else ctx.bot.user
        permission = ctx.channel.permissions_for(me)
        if permission.embed_links \
                and permission.external_emojis:
            return True
        logging.warning('no')
        raise errors.CannotsendEmbeds


    @client.command()
    async def pre(ctx):
        prefixes = await client.db.fetchval(
            """
            SELECT prefix
            FROM test.guilds
            WHERE id = $1
            """,
            ctx.guild.id
        )
        logging.warning(prefixes)
        if prefixes is None:
            await client.db.execute(
                """
                INSERT INTO test.guilds (id, prefix)
                VALUES($1,$2)
                ON CONFLICT DO NOTHING
                """,
                ctx.guild.id, "$"
            )
            await ctx.send("prefix set to $")
            return
        else:
            await ctx.send(prefixes)


    @client.command()
    async def setpre(ctx, prefix):
        await client.db.execute(
            """
            UPDATE guilds.prefixes 
            SET prefixes = $2
            WHERE guild_id = $1
            """,
            ctx.guild.id, prefix
        )
        await ctx.send("done")


    @client.command()
    async def delpre(ctx):
        await client.db.execute(
            """
            DELETE FROM guilds.prefixes 
            WHERE guild_id = $1
            """,
            ctx.guild.id
        )
        prefixes = await client.db.fetchval(
            """
            SELECT prefixes
            FROM guilds.prefixes
            WHERE guild_id = $1
            """,
            ctx.guild.id
        )
        logging.warning(prefixes)
        if prefixes is None:
            await ctx.send("hello")
        elif prefixes != None:
            await ctx.send("yes")

    bot = app_commands.Group(name='bot', description='the configuration commands for the bot'
                             , guild_ids=[client.support_guild])


    @bot.command(name='reload')
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.choices(
        colour=[  # param name
            Choice(name="Red", value='True'),
            Choice(name="Green", value='True'),
            Choice(name="Blue", value="blue")
        ],
        embeds=[  # param name
            Choice(name="Red", value='a'),
            Choice(name="Green", value='True'),
            Choice(name="Blue", value="blue")
        ]

    )
    async def reload(interaction: discord.Interaction, colour:Choice[str] , embeds:Choice[str], lol:str):
        await interaction.response.send_message(colour)


    @bot.command()
    async def fruits(interaction: discord.Interaction, fruits: typing.Literal['lolol','false']):
        print(fruits)
        if fruits == True_Or_False.true:
            interaction.response.send_message('bruh')
        if fruits == 'true':
            interaction.response.send_message('lo')




    @bot.command(name='load-cog', description='hello world')
    @owner_only()
    async def load_cog(interaction: discord.Interaction, cog: str):
        '''Load cog'''
        try:
            await client.load_extension("cogs." + cog)
        except commands.ExtensionAlreadyLoaded:
            print(f"Cog already loaded")
        except commands.ExtensionFailed as e:
            print(
                f"Error loading cog: {e.original.__class__.__name__}: {e.original}")
        except commands.ExtensionNotFound:
            print(f"Error: Cog not found")
        except commands.NoEntryPointError:
            print(f" Error: Setup function not found")
        except commands.ExtensionError as e:
            print(f" Error: {e}")
        except Exception as e:
            print(
                f"\N{THUMBS DOWN SIGN} Failed to load `{cog}` cog\n{type(e).__name__}: {e}")
        else:
            print(f"\N{THUMBS UP SIGN} Loaded `{cog}` cog \N{GEAR}")


    @bot.command(name="unload-cog")
    @owner_only()
    async def unload(ctx, cog: str):
        '''Unload cog'''
        try:
            await client.unload_extension("cogs." + cog)
        except commands.ExtensionNotLoaded:
            print(f"Error: Cog not found/loaded")
        except commands.ExtensionError as e:
            print(f" Error: {e}")
        except Exception as e:
            print(
                f"\N{THUMBS UP SIGN} Failed to unload `{cog}` cog\n{type(e).__name__}: {e}")
        else:
            print(f"\N{OK HAND SIGN} Unloaded `{cog}` cog \N{GEAR}")


    @bot.command(name='reload-cog')
    @owner_only()
    async def reload(ctx, cog: str):
        '''Reload cog'''
        try:
            await client.reload_extension("cogs." + cog)
        except commands.ExtensionFailed as e:
            print(
                f" Error loading cog: {e.original.__class__.__name__}: {e.original}")
        except commands.ExtensionNotFound:
            print(f"Error: Cog not found")
        except commands.ExtensionNotLoaded:
            print(f" Error: Cog not found/loaded")
        except commands.NoEntryPointError:
            print(f" Error: Setup function not found")
        except commands.ExtensionError as e:
            print(f" Error: {e}")
        except Exception as e:
            print(
                f"\N{THUMBS DOWN SIGN} Failed to reload `{cog}` cog\n{type(e).__name__}: {e}")
        else:
            print(f"\N{THUMBS UP SIGN} Reloaded `{cog}` cog \N{GEAR}")


    @bot.command(name='disconnect')
    @owner_only()
    async def disconnect(ctx):
        '''this is for emergency'''
        await client.close()

    client.tree.add_command(bot)


    @contextlib.contextmanager
    def setup_logging():
        log = logging.getLogger()

        try:
            # __enter__
            max_bytes = 32 * 1024 * 1024  # 32 MiB
            logging.getLogger('discord').setLevel(logging.INFO)
            logging.getLogger('asyncio').setLevel(logging.INFO)

            logging.getLogger('asyncpg').setLevel(logging.DEBUG)
            logging.getLogger('asyncpg').setLevel(logging.INFO)
            logging.getLogger('discord.http').setLevel(logging.INFO)
            logging.getLogger('aiohttp.client').setLevel(logging.WARNING)
            logging.getLogger('aiohttp.server').setLevel(logging.WARNING)
            logging.getLogger('aiohttp').setLevel(logging.INFO)
            logging.getLogger('aiohttp.access').setLevel(logging.INFO)
            logging.getLogger("asyncio").setLevel(logging.INFO)

            log.setLevel(logging.INFO)
            handler = logging.StreamHandler(sys.stderr)
            # (filename='sussybot.log', encoding='utf-8', mode='w', maxBytes=max_bytes,
            # backupCount=5)
            dt_fmt = '%Y-%m-%d %H:%M:%S'
            fmt = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')
            handler.setFormatter(fmt)
            log.addHandler(handler)

            yield
        finally:
            # __exit__
            handlers = log.handlers[:]
            for hdlr in handlers:
                hdlr.close()
                log.removeHandler(hdlr)


    async def main():
        async with client:
            try:
                client.console_log("starting up the bot")
                await client.start()
                await client.change_status.start()
            finally:
                client.console_log("shutting down the bot tasks")
                await client.shutdown_tasks()
                client.console_log("closing down the bot")
                await client.close()
                print(" done ")


    @client.command()
    async def automessage(ctx, value: typing.Literal["true", "false"]):
        logging.warning(value)

        a = True
        if value == "true":
            a = True
        elif value == "false":
            a = False
        logging.warning(a)
        await client.db.execute(
            """
            UPDATE guilds.checks 
            SET settings = $3
            WHERE guild_id = $1 AND name = $2
            """,
            ctx.guild.id, "automessage", a
        )

        check = await client.db.fetchval(
            """
            SELECT settings FROM guilds.checks
            WHERE name = $1 AND guild_id = $2
            """,
            "automessage", ctx.guild.id
        )
        logging.warning(check)
        await ctx.send(f"automessage is updated to {check}")


    try:
        with setup_logging():
            asyncio.run(main())
            tracker.print_diff()
    except KeyboardInterrupt:
        print(f"task shutdown with ")
