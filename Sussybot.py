import subprocess

import ssl

import os

from pympler.tracker import SummaryTracker
import contextlib

tracker = SummaryTracker()
if __name__ == "__main__":
    import logging
    import typing
    import sys
    from bot import SussyBot
    from handler import errors
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
            SELECT prefixes
            FROM guilds.prefixes
            WHERE guild_id = $1
            """,
            ctx.guild.id
        )
        if prefixes is None:
            await client.db.execute(
                """
                INSERT INTO guilds.prefixes (guild_id, prefixes)
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


    @contextlib.contextmanager
    def setup_logging():
        log = logging.getLogger()

        try:
            # __enter__
            max_bytes = 32 * 1024 * 1024  # 32 MiB
            logging.getLogger('discord').setLevel(logging.INFO)
            logging.getLogger('asyncio').setLevel(logging.DEBUG)

            logging.getLogger('asyncpg').setLevel(logging.DEBUG)
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
