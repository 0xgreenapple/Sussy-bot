from __future__ import annotations

import discord

from typing import TYPE_CHECKING
from discord.ext import commands
from handler.view import error_buttons
from discord.ui import Button

if TYPE_CHECKING:
    from bot import SussyBot


class Context(commands.Context):
    bot: SussyBot

    async def error_embed(
            self, title: str = None, *, description: str = None, error_name=None,
            error_dis: str = None, colour: discord.Colour = None, timestamp=discord.utils.utcnow()):

        error_emoji = self.bot.get_emoji(975326725426778184)
        right_emoji = self.bot.get_emoji(975326725158346774)

        if title is None:
            title = f"{error_emoji} ``OPERATION FAILED``"

        if not colour:
            colour = self.bot.embed_colour

        embed = discord.Embed(title=title, description=description, timestamp=timestamp, colour=colour)

        if error_name and error_dis:
            error_name = f"__**{error_name}**__"
            error_dis = f"{right_emoji} {error_dis}"
            embed.add_field(name=error_name, value=error_dis)

        embed.set_footer(text='\u200b', icon_url=self.author.avatar.url)
        view = error_buttons(self)
        linkbutton = Button(url="https://sussybot.xyz", label="support", style=discord.ButtonStyle.url)
        view.add_item(linkbutton)
        view.message = await self.send(embed=embed, view=view)
        return view.message

    async def hello(self):
        return await self.send("hello")

    async def send_dm(
            self, member=discord.Member, *, message: str = None, embed: discord.Embed = None,
            view: discord.ui.View = None):
        channel = await member.create_dm()

        return await channel.send(content=message, embed=embed, view=view)


async def heloo(ctx:discord.Interaction):
    await ctx.response.send_message("hello world")
