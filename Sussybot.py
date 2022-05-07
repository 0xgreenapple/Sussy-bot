from bot import SussyBot
import os
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp


async def run_bot():
    client = SussyBot()
    await client.start()
def main():
    """Launches the bot."""
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()




