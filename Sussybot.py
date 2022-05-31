from pympler.tracker import SummaryTracker
tracker = SummaryTracker()
if __name__ == "__main__":
    import logging
    import sys
    from bot import SussyBot
    import asyncio

    client = SussyBot()


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


    async def main():
        """Launches the bot."""
        async with client:
            try:
                client.print("starting up the bot")
                await client.start()
                await client.change_status.start()
            finally:
                client.print("shutting down the bot tasks")
                await client.shutdown_tasks()
                client.print("closing down the bot")
                await client.close()
                print(" done ")


    try:
        asyncio.run(main())
        tracker.print_diff()
    except KeyboardInterrupt:
        print("bot has successfully stopped")



