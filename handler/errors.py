from __future__ import annotations

import discord
from discord import DiscordException
from discord.ext import commands
from discord.ext.commands.errors import CheckFailure

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import SussyBot


async def error_embed(titile: str = None, *, des: str = None, error_name: str = None, error_des: str = None,
                      colour: discord.Colour, timestamp=discord.utils.utcnow()):
    if titile is None:
        a = SussyBot.get_emoji(975326725426778184)
        titile = f"{a} ``OPERATION FAILED"

    embed = discord.Embed(title=titile, description=des, colour=colour, timestamp=timestamp)

class CannotsendEmbeds(CheckFailure):
    """check if bot can send embeds"""

    def __init__(self, message=None):
        super().__init__(message or 'this command cannot be run.')