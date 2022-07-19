from __future__ import annotations

import logging

import discord
from discord import Interaction, app_commands
from discord.ext import commands

from typing import TYPE_CHECKING

import Sussybot
from handler import errors

if TYPE_CHECKING:
    from handler.Context import Context
    from bot import SussyBot


def is_role_lower(user: discord.Member):
    async def predict(ctx):
        if isinstance(ctx,discord.Interaction):
            return user.top_role.position < ctx.user.top_role.position
        else:
            return user.top_role.position < ctx.author.top_role.position
    return predict


def is_permitted():
    async def predict(ctx: Context):
        me = ctx.guild.me if ctx.guild is not None else ctx.bot.user
        permission = ctx.channel.permissions_for(me)
        if permission.embed_links \
                and ctx.message.guild.me.guild_permissions.external_emojis:
            return True
        logging.warning('no')
        raise errors.CannotsendEmbeds

    return commands.check(predict)


async def is_lower_role(ctx, member: discord.Member):
    if isinstance(ctx, discord.Interaction):
        return member.top_role.position < ctx.user.top_role.position or ctx.user == ctx.guild.owner
    else:
        return member.top_role.position < ctx.author.top_role.position or ctx.author.id == ctx.guild.owner.id



# in a class (cog)
# @staticmethod
# ^ required if this function is in a cog
# the decorator

def owner_only():
    async def predict(interaction: Interaction):
        return interaction.user.id == 888058231094665266
    return app_commands.check(predict)
