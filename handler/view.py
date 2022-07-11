from __future__ import annotations

import logging
import time
from datetime import datetime, timedelta

import discord

from typing import TYPE_CHECKING, Optional
from logging import getLogger

import psutil

if TYPE_CHECKING:
    from .Context import Context
    from bot import SussyBot

log = getLogger(__name__)


class error_buttons(discord.ui.View):
    def __init__(
            self,
            ctx: Context,

    ):
        super().__init__(timeout=180)
        self.ctx: Context = ctx

    @discord.ui.button(label='delete', style=discord.ButtonStyle.danger)
    async def delete(self, interaction: discord.Interaction, button):
        if interaction.user.id == self.ctx.author.id or interaction.user.id == self.ctx.guild.owner.id:
            await interaction.message.delete()
            return
        else:
            await interaction.response.send_message('this is not for you lol', ephemeral=True)


    @discord.ui.button(label='help', style=discord.ButtonStyle.green)
    async def help(self, interaction: discord.Interaction, button):
        if interaction.user.id == self.ctx.author.id or interaction.user.id == self.ctx.guild.owner.id:
            await interaction.response.send_message("no help?")
            return
        else:
            await interaction.response.send_message('this is not for you lol', ephemeral=True)


    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
            try:
                await self.message.edit(view=self)
            except discord.NotFound:
                pass

class delete_view(discord.ui.View):
    def __init__(
            self,
            ctx: Context,

    ):
        super().__init__(timeout=180)
        self.ctx: Context = ctx
        self.message: Optional[discord.Message] = None

    @discord.ui.button(label='delete', style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button):
        if interaction.user.id == self.ctx.author.id or interaction.user.id == self.ctx.guild.owner.id:
            await interaction.message.delete()
            return
        else:
            await interaction.response.send_message('this is not for you lol', ephemeral=True)

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
            try:
                await self.message.edit(view=self)
            except discord.NotFound:
                pass

class userinfo(discord.ui.View):
    def __init__(
            self,
            ctx: Context,

    ):
        super().__init__(timeout=180)
        self.ctx: Context = ctx
        self.message: Optional[discord.Message] = None
    @discord.ui.button(label='permissions', style=discord.ButtonStyle.primary)
    async def permission(self, interaction: discord.Interaction, button:discord.ui.Button):
        if interaction.user.id == self.ctx.author.id or interaction.user.id == self.ctx.guild.owner.id:
            permission = []
            log.warning('hello')
            for key,value in self.ctx.author.guild_permissions:
                if value:
                    permission.append(key.replace('_',' '))
            permission = ', '.join(permission)
            embed = discord.Embed(title='guild permissions',description=f'```yml \n{permission}```')
            self.permission1.disabled = False
            button.disabled = True
            await interaction.response.edit_message(embed=embed,view=self)
            return
        else:
            await interaction.response.send_message('this is not for you lol', ephemeral=True)

    @discord.ui.button(label='back', style=discord.ButtonStyle.primary,disabled=True)
    async def permission1(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.message.embeds[0]
        button.disabled = True
        self.permission.disabled = False
        await interaction.response.edit_message(embed=embed,view=self)


class refresh_ping(discord.ui.View):
    def __init__(
            self,
            ctx: Context,
            bot:SussyBot

    ):
        super().__init__(timeout=180)
        self.ctx: Context = ctx
        self.bot: SussyBot  = bot
        self.message: Optional[discord.Message] = None

    @discord.ui.button(label='refresh', style=discord.ButtonStyle.green)
    async def refresh_Ping(self, interaction: discord.Interaction, button):
        if interaction.user.id == self.ctx.author.id or interaction.user.id == self.ctx.guild.owner.id:

            ping = self.bot.latency * 1000

            if 100 <= ping <= 200:
                ping_status = "neutral"
            elif ping <= 100:
                ping_status = "low"
            else:
                ping_status = "high"
            timestamp1 = datetime.utcnow()
            uptime = (timedelta(seconds=int(round(time.time() - self.bot.startTime))))

            member = 0
            for guilds in self.bot.guilds:
                a = guilds.member_count
                member += a
            total_memory = round(psutil.virtual_memory().total)
            if total_memory / 1000000 < 1000:
                total_memory = f"{round(psutil.virtual_memory().total / 1000000)} MB"
            else:
                total_memory = f"{round(psutil.virtual_memory().total / 1000000000, 2)} GB"

            used_memory = round(psutil.virtual_memory().used)
            if used_memory / 1000000 < 1000:
                used_memory = f"{round(psutil.virtual_memory().used / 1000000)} MB"
            else:
                used_memory = f"{round(psutil.virtual_memory().used / 1000000000, 2)} GB"

            bedem = discord.Embed(title='``status``', colour=self.bot.bot_color, timestamp=timestamp1)
            bedem.add_field(name=f"Ping **({ping_status})**", value=f"```{round(self.bot.latency * 1000)}ms```",
                            inline=True)
            bedem.add_field(name="Servers",
                            value=f"```{len(self.bot.guilds)}```",
                            inline=True)
            bedem.add_field(name="Users", value=f"```{member}```", inline=True)
            bedem.add_field(name="Uptime", value=f"```{uptime}```", inline=True)
            bedem.add_field(name="System",
                            value=f"**memory Usage:** ``{used_memory} /{total_memory}`` \n "
                                  f"**cpu :** ``{psutil.cpu_percent()}``%"
                            , inline=False)
            bedem.add_field(name="command ran today", value=f"```18238183```")
            bedem.set_author(name=self.ctx.author.name, icon_url=self.ctx.author.avatar.url)
            bedem.set_footer(text="\u200b", icon_url=self.bot.user.avatar.url)
            await interaction.response.edit_message(embed=bedem,view=self)
            return
        else:
            await interaction.response.send_message('this is not for you lol', ephemeral=True)

    @discord.ui.button(label='delete', style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button):
        if interaction.user.id == self.ctx.author.id or interaction.user.id == self.ctx.guild.owner.id:
            await interaction.message.delete()
            await self.ctx.message.delete()
            return
        else:
            await interaction.response.send_message('this is not for you lol', ephemeral=True)

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
            try:
                await self.message.edit(view=self)
            except discord.NotFound:
                pass
