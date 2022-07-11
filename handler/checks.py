from __future__ import annotations

import logging

import discord
from discord.ext import commands

from typing import TYPE_CHECKING
from handler import errors

if TYPE_CHECKING:
    from handler.Context import Context


def is_role_lower(user: discord.Member):
    async def predict(ctx):
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
    return member.top_role.position < ctx.author.top_role.position or ctx.author == ctx.guild.owner
