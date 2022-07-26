from __future__ import annotations

import io

import asyncpg

import time

import argparse
import logging
import shlex
import typing
from discord.ui import Button
from time import mktime
from typing import Optional, TYPE_CHECKING

import discord
from discord import automod, app_commands
from discord.ext import commands, menus
from discord.ext.commands import cooldown, BucketType
from discord.ext.menus.views import ViewMenuPages

from handler.pagination import SimplePages
from handler.utils import string_to_delta
from handler.view import delete_view, userinfo, interaction_delete_view, interaction_error_button, reaction_role
from handler.checks import is_permitted, is_lower_role
from datetime import timedelta, datetime
from discord.app_commands import Choice
from enum import Enum
from handler import utils

if TYPE_CHECKING:
    from bot import SussyBot
    from handler.Context import Context

# setup logging
log = logging.getLogger(__name__)


class Warningspages(SimplePages):
    def __init__(self, entries: list, *, ctx: discord.Interaction, per_page: int = 12, title: str = None):
        converted = entries
        print(entries)
        super().__init__(converted, per_page=per_page, ctx=ctx, title=title)


class Point(typing.NamedTuple):
    x: int
    y: int


class PointTransformer(app_commands.Transformer):
    @classmethod
    async def transform(cls, interaction: discord.Interaction, value: str) -> Point:
        (x, _, y) = value.partition(',')
        return Point(x=int(x.strip()), y=int(y.strip()))


async def bulk_delete_advance(
        interaction: discord.Interaction, limit: int = 10, *, check: list = None,
        before=None, after=None, around=None, oldest_first: Optional[bool] = None,
        reason: Optional[str] = None, delete_type=None):
    message = discord.utils.utcnow() - timedelta(days=14)
    if len(check) != 0:
        log.warning('asdasd')
        print(delete_type)

        # check.append(lambda m: m.created_at >= message)
        def predicate(m):
            r = any(p(m) for p in check)
            if delete_type == 'true':
                r = all(p(m) for p in check)
            return r

        predicate: typing.Callable[[discord.Message], typing.Any] = predicate
        print(predicate)
        message = await interaction.channel.purge(
            limit=limit, check=predicate if predicate else lambda m: m.created_at >= message, before=before,
            after=after,
            around=around, oldest_first=oldest_first, bulk=True, reason=reason)
        return message
    else:
        message = await interaction.channel.purge(limit=limit, check=lambda m: m.created_at >= message)
    return message


class moderation(commands.Cog):
    """moderation commands"""

    def __init__(self, bot: SussyBot) -> None:
        self.bot = bot

    # delete the message under 14 days.

    # clear command
    @app_commands.command(name='purge', description="clear the messages of a channel in the best way possible")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.guild_only()
    @app_commands.describe(
        limit='number of messages to delete from the channel default set to 10',
        contain='delete the message that content given word. separate by comma!',
        startswith='delete the messages that starts with given word. separate by comma',
        user='only delete the message of specific user',
        embeds='delete the message that contain embeds',
        files='delete the message contains files',
        reactions='delete the message contains reactions',
        delete_type='If set true, delete only messages matching all conditions',
        hide='hide the response message if set to true'
    )
    async def clear(self, interaction: discord.Interaction, limit: app_commands.Range[int, 1, 2000] = 10,
                    delete_type: typing.Literal['true', 'false'] = None, *,
                    user: typing.Union[discord.Member, discord.User] = None,
                    contain: str = None, startswith: str = None, endswith: str = None,
                    embeds: typing.Literal['true', 'false'] = None,
                    files: typing.Literal['true', 'false'] = None, reactions: typing.Literal['true', 'false'] = None,
                    mentions: typing.Literal['true', 'false'] = None, hide: typing.Literal['true', 'false'] = None):

        """advance clear command that delete the messages
         from the channel that is under 14 days as given argument.
         delete the 100 message from the channel if amount not given

         `limit` : the number of messages to delete
         `!user` : delete the message of the user
         `!contain` : delete the message that contain given word
        """
        # emojis
        if hide == 'true':
            await interaction.response.defer(thinking=True, ephemeral=True)

        purge_embed = discord.Embed(colour=self.bot.embed_colour, timestamp=discord.utils.utcnow())
        purge_embed.set_footer(text='\u200b', icon_url=interaction.user.avatar.url)

        view = interaction_delete_view(interaction)
        message = discord.utils.utcnow() - timedelta(days=14)
        predicates = []
        await interaction.response.defer(thinking=True, ephemeral=True)
        if embeds == 'true':
            log.warning('embeds')
            predicates.append(lambda m: len(m.embeds) and m.created_at >= message)
        if files == 'true':
            log.warning('files')
            predicates.append(lambda m: len(m.attachments) and m.created_at >= message)
        if reactions == 'true':
            log.warning('reaction')
            predicates.append(lambda m: len(m.reactions) and m.created_at >= message)
        if mentions == 'true':
            log.warning('mention')
            predicates.append(lambda m: len(m.mentions) and m.created_at >= message)
        if startswith:
            log.warning('starts')
            predicates.append(lambda m: any(m.content.endswith(s) for s in endswith) and m.created_at >= message)
        if endswith:
            endswith = endswith.split(',')
            log.warning('ends')
            predicates.append(lambda m: any(m.content.endswith(s) for s in endswith) and m.created_at >= message)
        if contain:
            content = contain.split(',')
            log.warning('contain')
            predicates.append(
                lambda m: True if any(sub in m.content for sub in content) and m.created_at >= message else False)
        if user:
            predicates.append(lambda m: True if m.author.id == user.id and m.created_at >= message else False)

        try:
            message = await bulk_delete_advance(
                interaction=interaction, limit=limit, check=predicates,
                delete_type=delete_type)
        except discord.Forbidden:
            await utils.error_embed(
                bot=self.bot, Interaction=interaction,
                error_name="purge command",
                error_dis="i dont have permission to delete messages")
            return

        purge_embed.add_field(
            name="**Purge result :**",
            value=f">>> used by : {interaction.user.mention} \n"
                  f"{self.bot.channel_emoji} **channel :** {interaction.user.mention} \n"
                  f"{self.bot.right} **message requested :** ``{limit}`` \n"
                  f"{self.bot.search_emoji} **deleted :** ``{len(message)}`` \n"
                  f"{self.bot.failed_emoji} failed : ``{limit - len(message)}``")
        if interaction.response.is_done():
            await interaction.followup.send(embed=purge_embed)
            return
        else:
            await interaction.followup.send(embed=purge_embed, view=view)
            view.message = await interaction.original_message()
            return view.message

    # warn member
    @app_commands.guild_only()
    @app_commands.command(name='warn', description='warn a member, warnings are saved in the bot database')
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members=True)
    @app_commands.default_permissions(kick_members=True)
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(
        member='member to warn, |id|mention|tag|',
        reason='reason for warning'
    )
    async def warn(self, interaction: discord.Interaction, member: discord.Member, *,
                   reason: app_commands.Range[str, 1, 250] = None):

        if member.id == interaction.user.id:
            await utils.error_embed(
                error_name='warn command error', error_dis='you cant warn yourself', bot=self.bot,
                Interaction=interaction)
            return
        if member.bot:
            await utils.error_embed(
                error_name='warn command error', error_dis='the member you provided cant be banned', bot=self.bot,
                Interaction=interaction)
            return
        if not await is_lower_role(interaction, member):
            await utils.error_embed(
                error_name='warn command error', error_dis="you must have lower role than provided member",
                bot=self.bot, Interaction=interaction
            )
            return
        await interaction.response.defer(thinking=True)
        # values
        reason_msg = reason if reason else 'for no reason'
        dm_value = True
        # append the values to warning table
        warns = await self.bot.db.fetch(
            """
            SELECT * FROM test.warns
             WHERE guild_id = $1 AND user_id = $2 
            """,
            interaction.guild.id, member.id
        )
        if warns is not None:
            if len(warns) > 30:
                await self.bot.db.execute(
                    """
                    DELETE FROM test.warns 
                    WHERE id IN (
                    SELECT id FROM test.warns WHERE user_id =$1 AND guild_id = $2 
                    ORDER BY id ASC LIMIT 1)
                    """,
                    interaction.guild.id, member.id
                )

        warnid = await self.bot.db.fetchval(f"""SELECT test.warnfunc($1,$2,$3)""", member.id, interaction.guild.id,
                                            reason)

        dm_warn_embed = discord.Embed(
            title=f'You have been warned in ``{interaction.guild.name}`` server',
            description=f'{self.bot.file_emoji} **reason :** {reason_msg}',
            timestamp=discord.utils.utcnow()
        ).set_footer(text='\u200b', icon_url=interaction.user.avatar.url)

        dm_info_embed = discord.Embed(
            title=f'**``warn``**', timestamp=discord.utils.utcnow()
        ).set_footer(text='\u200b',
                     icon_url=interaction.user.display_avatar.replace(size=32).url
                     )

        try:
            channel = await member.create_dm()
            await channel.send(embed=dm_warn_embed)
        except discord.HTTPException:
            dm_value = 'failed'

        print('going')
        dm_info_embed.add_field(name=f'{self.bot.right} __{member.name}__ has been warned',
                                value=f'>>> {self.bot.file_emoji} **reason :** {reason} \n'
                                      f'dmed member: ``{dm_value}``\n'
                                      f'``warn ID``: {warnid}')

        view = interaction_delete_view(interaction)
        await interaction.followup.send(embed=dm_info_embed, view=view)
        view.message = await interaction.original_message()
        return view.message

    @app_commands.guild_only()
    @app_commands.command(name='warns', description='get the all warnings of a user')
    @app_commands.default_permissions(kick_members=True)
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members=True)
    @app_commands.describe(
        member='member | member mention |userid'
    )
    async def warns(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer(thinking=True)
        warns = await self.bot.db.fetch(
            """
            SELECT * FROM test.warns
             WHERE guild_id = $1 AND user_id = $2 
            """,
            interaction.guild.id, member.id
        )

        warninglist = []
        for warning in warns:
            warning: asyncpg.Record = warning
            time = utils.datetime_to_local_timestamp(warning.get('time'))
            if warning.get('warning') is not None:
                warninglist.append({'id': warning.get("id"), 'time': time, 'reason': warning.get('warning')})
            else:
                warninglist.append({'id': warning.get("id"), 'time': time, 'reason': 'no reason'})

        if warns:
            warnings = Warningspages(entries=warninglist, per_page=5, ctx=interaction,
                                     title=f'``{member}`` warnings [{len(warninglist)}]')
            await warnings.start()
        if warns is None:
            await interaction.followup.send('this user has no warnings', ephemeral=True)

    @app_commands.command(name='clearwarnings', description='clear the warnings of member,view warnings by running '
                                                            '/warns command')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members=True)
    @app_commands.default_permissions(kick_members=True)
    @app_commands.describe(id='warn id, check by running warns command',
                           clear_all='clear all warnings of the given user')
    async def clearwarns(self, interaction: discord.Interaction, member: discord.Member, *, id: int = None,
                         clear_all: typing.Literal['true', 'false'] = None):
        if member.id == interaction.user.id:
            await utils.error_embed(
                error_name='warn command error',
                error_dis='you cant clear yourself warning',
                bot=self.bot, Interaction=interaction)
            return

        if not await is_lower_role(interaction, member):
            await utils.error_embed(
                error_name='warn command error',
                error_dis="you cant clear warnings of the user who has above to you",
                bot=self.bot, Interaction=interaction
            )
            return
        # show the interaction message
        await interaction.response.defer()
        warnings = 0
        all_cleard = False
        value = await self.bot.db.fetch(
            """
            SELECT * FROM test.warns 
            WHERE id = $1 AND user_id=$2 
            AND guild_id= $3
            """,
            id, member.id, interaction.guild.id
        )
        if clear_all == 'true':
            await self.bot.db.execute(
                """ DELETE FROM test.warns 
                    WHERE user_id= $1 AND 
                    guild_id = $2
                """,
                member.id, interaction.guild.id
            )
            warnings = len(value)
            all_cleard = True
        else:
            if len(value) is None:
                await utils.error_embed(
                    bot=self.bot, Interaction=interaction,
                    error_name='warn command error',
                    error_dis=f'there is no warning for {member.name} with id : {id}'
                )
                return

            await self.bot.db.execute(
                """
                DELETE FROM test.warns 
                WHERE user_id= $1 
                AND guild_id = $2 AND id = $3
                """, member.id, interaction.guild.id, id
            )
            warnings = 1
        if warnings == 1:
            delete_warn_embed = discord.Embed(
                title=f'**``{warnings} warnings were deleted``**',
                description=f'{self.bot.right} **user**: {member.mention} \n'
                            f'warn id:``{id}`` \n'
                            f'all deleted? = ``false``', timestamp=discord.utils.utcnow()
            ).set_footer(text='\u200b',
                         icon_url=interaction.user.display_avatar.replace(size=32).url
                         )
        else:
            delete_warn_embed = discord.Embed(
                title=f'**``{warnings} warnings were deleted``**',
                description=f'{self.bot.right} **user**: {member.mention} \n'
                            f'all deleted? = ``true``', timestamp=discord.utils.utcnow()
            ).set_footer(text='\u200b',
                         icon_url=interaction.user.display_avatar.replace(size=32).url
                         )
        view = interaction_delete_view(interaction)
        await interaction.followup.send(embed=delete_warn_embed, view=view)
        view.message = await interaction.original_message()
        return view.message

    # kick command
    @app_commands.command(name='kick', description="kick member of server")
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members=True)
    @app_commands.describe(
        member='provide the user to kick from guild',
        reason='reason to kick the member',
        dm='direct message on kick?',
        days='number of days to delete the messages'
    )
    async def kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None,
                   dm: typing.Literal['true', 'false'] = None, days: app_commands.Range[int, 1, 14] = None):

        """
        kick member with reason if given
        `!reason` : kick a member of the server with reason if provided
        `!dm` : store value true dm member on kick
        """
        # kick embed
        ejected = self.bot.get_emoji(991340144202350663)
        kick_embed = discord.Embed(title=f'{ejected} ``Kick``')
        kick_embed.set_footer(text='\u200b', icon_url=interaction.user.avatar.url)

        if member.id == interaction.user.id:
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='kick command error',
                error_dis='you cant kick your self. are you crazy')
            return
        if not await is_lower_role(interaction, member):
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='kick command error',
                error_dis="you must have lower role than member"
            )
            return

        dm = dm
        dm_value = ''
        msg_deleted = 0
        if reason:
            kick_embed.description = f'{self.bot.file_emoji} **reason :** {reason}'
        else:
            reason = None
            kick_embed.description = f'{self.bot.file_emoji} **reason :** no reason provided'
        if dm == 'true':
            try:
                dm_view = interaction_delete_view(interaction)
                dm_kick_embed = discord.Embed(
                    title=f'You have been kicked from ``{interaction.guild.name}`` server',
                    description=f'{self.bot.file_emoji} **reason :** {reason if reason else "no reason"}',
                    timestamp=discord.utils.utcnow()
                ).set_footer(text='\u200b', icon_url=interaction.user.avatar.url)

                channel = await member.create_dm()
                message = await channel.send(embed=dm_kick_embed, view=dm_view)
                dm_view.message = message

                dm_value = True
            except discord.Forbidden or discord.HTTPException:
                dm_value = 'dm failed'
        try:

            dm_value = dm_value if dm_value else 'false'
            reason = f'[{reason}]- {interaction.user}' if reason else f'[no reason] -{interaction.user}'
            await interaction.guild.kick(user=member, reason=reason)
            if days:
                days = discord.utils.utcnow() - timedelta(days=days)
                msg_deleted = await interaction.channel.purge(limit=500, check=lambda m: m.created_at >= days)
        except discord.Forbidden or discord.HTTPException:
            await interaction.response.send_message(embed=kick_embed)

        kick_embed.add_field(name='__**kick details**__',
                             value=f'>>> {self.bot.right} **moderator :** {interaction.user.mention} \n'
                                   f'**dmed member? :** {dm_value} \n'
                                   f'**delete messages:**`{days if msg_deleted is not None else "failed"}`',
                             inline=False)
        kick_embed.add_field(name='__**member details**__',
                             value=f'>>>  {self.bot.right} **username :** ``{member}`` \n'
                                   f'``ID``:{member.id} \n'
                                   f'**server joined at :** <t:{round(int(mktime(member.joined_at.timetuple())))}:D>\n '
                                   f'**created at :** <t:{round(int(mktime(member.created_at.timetuple())))}:D>')
        view = interaction_delete_view(interaction)
        await interaction.response.send_message(embed=kick_embed, view=view)
        view.message = await interaction.original_message()

    @app_commands.guild_only()
    @app_commands.command(name='ban', description="ban a user from the server")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.describe(
        user='member or user to ban, can be id user tag or mention',
        reason='reason of ban',
        days='number of days to delete the message',
        dm='dm member or not'
    )
    async def ban(self, interaction: discord.Interaction, user: typing.Union[discord.Member, discord.User], *,
                  reason: str = None, days: app_commands.Range[int, 1, 7] = None,
                  dm: typing.Literal['true', 'false'] = None):

        """
        ban member with reason if given
        `reason` : kick a member of the server with reason if provided
        `dm` : store value true dm member on kick
        `days` : delete message days
        """
        # embed
        right_arrow = self.bot.right

        ejected = self.bot.get_emoji(991340144202350663)
        ban_embed = discord.Embed(title=f'{ejected} ``ban``')
        ban_embed.set_footer(text='\u200b', icon_url=interaction.user.avatar.url)
        member_or_not = interaction.guild.get_member(user.id)
        if user.id == interaction.user.id:
            await utils.error_embed(
                Interaction=interaction,
                bot=self.bot,
                error_name='ban command error',
                error_dis='you cant ban your self! are you crazy?')
            return

        if member_or_not:
            if not await is_lower_role(interaction, member=user):
                await utils.error_embed(
                    bot=self.bot,
                    Interaction=interaction,
                    error_name='ban command error',
                    error_dis="you must have lower role than given member!")
                return

        delete = days if days else 0
        created_at = round(int(mktime(user.created_at.timetuple())))
        joined_at = round(int(mktime(user.joined_at.timetuple()))) if member_or_not else None
        dm_value = ''

        if reason:
            ban_embed.description = f'{self.bot.file_emoji} **reason :** {reason}'
        else:
            reason = None
            ban_embed.description = f'{self.bot.file_emoji} **reason :** no reason provided'

        if dm == 'true' and not user.bot:
            try:
                dm_view = interaction_delete_view(interaction)
                dm_ban_embed = discord.Embed(
                    title=f'You have been banned from ``{interaction.guild.name}`` server',
                    description=f'{self.bot.file_emoji} **reason :** {reason if reason else "no reason"}',
                    timestamp=discord.utils.utcnow()
                ).set_footer(text='\u200b', icon_url=interaction.user.avatar.url)
                channel = await user.create_dm()
                message = await channel.send(embed=dm_ban_embed)
                dm_view.message = message
                dm_value = True
            except discord.Forbidden or discord.HTTPException:

                dm_value = 'dm failed'
        try:

            dm_value = dm_value if dm_value else 'false'
            reason = f'[{reason}]- {interaction.user}' if reason else f'[no reason] -{interaction.user}'
            await interaction.guild.ban(user=user, reason=reason, delete_message_days=0)
        except discord.Forbidden or discord.HTTPException:
            await utils.error_embed(
                bot=self.bot, Interaction=interaction,
                error_name='ban command error', error_dis='something went wrong')
            return

        ban_embed.add_field(name='__**ban details**__',
                            value=f'>>> {self.bot.file_emoji} **moderator :** {interaction.user.mention} \n'
                                  f'**dmed member? :** {dm_value} \n'
                                  f'**delete message days :** ``{delete}``', inline=False
                            )
        if member_or_not:
            ban_embed.add_field(name='__**member details**__',
                                value=f'>>>  {right_arrow} **username :** ``{user}`` \n'
                                      f'``ID``:{user.id} \n'
                                      f'**joined at :** <t:{joined_at}:D>\n '
                                      f'**created at :** <t:{created_at}:D>'
                                )
        else:
            ban_embed.add_field(name='__**member details**__',
                                value=f'>>>  {right_arrow} **username :** ``{user}`` \n'
                                      f'``ID``:{user.id} \n'
                                      f'**created at :** <t:{created_at}:D>'
                                )
        view = interaction_delete_view(interaction)
        await interaction.response.send_message(embed=ban_embed, view=view)
        view.message = await interaction.original_message()

    @app_commands.command(name='unban', description="unban a user | reason to unban")
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.describe(
        user='user to unban, must be id or user tag',
        reason='reason for unban',
        dm='dm member on unban if possible'
    )
    async def unban(self, interaction: discord.Interaction, user: discord.User, *, reason: Optional[str],
                    dm: typing.Literal['true', 'false'] = None):
        """unban a user or multiple!
        unban a user with reason if given
        `member`: user to unban
        `reason`: unban reason (optional)
        `dm`:dm member if possible
        """

        reason_msg = reason if reason else 'no reason provided'

        failed = 0
        dm_value = ''
        ban_embed = discord.Embed(title='``unban``', description=f'{self.bot.file_emoji} **reason :**{reason_msg}')

        if dm == 'true':
            try:
                dm_warn_embed = discord.Embed(title=f'You have been unbanned in ``{interaction.guild.name}`` server',
                                              description=f'{self.bot.file_emoji} **reason :** {reason_msg}',
                                              timestamp=discord.utils.utcnow())
                dm_warn_embed.set_footer(text='\u200b', icon_url=interaction.user.avatar.url)
                channel = await user.create_dm()
                await channel.send(embed=dm_warn_embed)
                dm_value = 'true'
            except discord.Forbidden or discord.HTTPException:
                dm_value = 'failed'
        try:
            reason = f'[{reason}]- {interaction.user}' if reason else f'[no reason] -{interaction.user}'
            await interaction.guild.unban(user=user, reason=reason)
        except discord.NotFound:
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='unban command error',
                error_dis=f'the user {user.name} is not banned')
            return
        except discord.HTTPException:
            await utils.error_embed(
                Interaction=interaction,
                bot=self.bot,
                error_name='unban command error',
                error_dis='something went wrong while unbanning a user')
            return

        ban_embed.add_field(name='__**ban details**__',
                            value=f'>>> {self.bot.right} **moderator :** {interaction.user.mention} \n'
                                  f'**failed :** ``{failed}`` \n'
                                  f'**dm user?:** ``{dm_value}``',
                            inline=False)

        ban_embed.add_field(
            name='__**user details**__',
            value=f'>>>  {self.bot.right} **username :** ``{user.name}`` \n'
                  f'``ID``:{user.id} \n'
                  f'**created at :** <t:{round(int(mktime(user.created_at.timetuple())))}:D>')
        view = interaction_delete_view(interaction)
        view.message = await interaction.response.send_message(embed=ban_embed, view=view)

    timeout = app_commands.Group(
        name="timeout",
        description="add, update,remove timeout",
        guild_only=True,
        default_permissions=discord.Permissions(moderate_members=True)
    )

    @app_commands.command(name='timeout', description='timeout or update timeout of a member ')
    @app_commands.guild_only()
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.checks.bot_has_permissions(moderate_members=True)
    @app_commands.describe(
        member='the member who you want to timeout',
        duration='must be in 1d|1h|1m|1s formate',
        reason='the reason to timeout the member',
    )
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, *,
                      duration: str = None, reason: str = None):

        if member.id == interaction.user.id:
            await utils.error_embed(
                Interaction=interaction,
                bot=self.bot,
                error_name='timeout command error',
                error_dis='you cant ban your self! are you crazy?')
            return

        if not await is_lower_role(interaction, member=member):
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='timeout command error',
                error_dis="you must have lower role than given member!")
            return

        if member.bot:
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='timeout command error',
                error_dis="cant timeout this user!")
            return
        await interaction.response.defer(thinking=True)

        # variables
        failed = False
        reason_Msg = reason if reason else 'no reason'
        reason = f'[{reason}] - {interaction.user}' if reason else f'[no reason] - {interaction.user}'
        time_delta = string_to_delta(duration)

        time_delta = time_delta if time_delta else timedelta(days=28)

        try:
            await member.timeout(time_delta, reason=reason)
        except discord.HTTPException:
            failed = True
        timestamp = round(int(mktime((datetime.now() - time_delta).timetuple())))
        timeout_info_embed = discord.Embed(
            title=f'**``timeout``**', timestamp=discord.utils.utcnow()
        ).set_footer(text='\u200b',
                     icon_url=interaction.user.display_avatar.replace(size=32).url
                     )

        if not failed:
            if member.is_timed_out():
                timedoutfor = round(int(mktime(member.timed_out_until.timetuple())))
                timeout_info_embed.title = f'**``timeout update``**'
                timeout_info_embed.add_field(name=f'{self.bot.right} __{member.name}__ timeout has been updated',
                                             value=f'>>> {self.bot.file_emoji} **reason :** {reason_Msg} \n'
                                                   f'before: <t:{timedoutfor}:f>\n'
                                                   f'after: <t:{timestamp}:f> \n'
                                                   f'``failed``: {self.bot.failed_emoji}')
            else:
                timeout_info_embed.add_field(name=f'{self.bot.right} __{member.name}__ has been timed out',
                                             value=f'>>> {self.bot.file_emoji} **reason :** {reason_Msg} \n'
                                                   f'**until**: <t:{timestamp}:f> \n'
                                                   f'``failed``: {self.bot.failed_emoji}')
        else:
            timeout_info_embed.title = f'**``timeout failed``**'
            timeout_info_embed.add_field(name=f'{self.bot.right} __{member.name}__ has been timed out',
                                         value=f'>>> {self.bot.file_emoji} **reason :** {reason_Msg} \n'
                                               f'``failed``: {self.bot.success_emoji}')
        view = interaction_delete_view(interaction)
        await interaction.followup.send(
            embed=timeout_info_embed, view=view
        )

        view.message = await interaction.original_message()
        return view.message

    @app_commands.command(name='removetimeout', description='remove timeout of a user')
    @app_commands.guild_only()
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.checks.bot_has_permissions(moderate_members=True)
    @app_commands.describe(
        member='the member who you want to remove timeout',
        reason='the reason to remove timeout of the member'
    )
    async def removetimeout(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):

        if not await is_lower_role(interaction, member=member):
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='timeout command error',
                error_dis="you must have lower role than given member!")
            return
        if not member.is_timed_out():
            await utils.error_embed(
                Interaction=interaction,
                bot=self.bot,
                error_name='timeout command error',
                error_dis='the member is already not timed out')
            return

        # defer the interaction
        await interaction.response.defer()
        # variables
        reason_msg = reason if reason else 'no reason'
        reason = f'[{reason}] - {interaction.user}' if reason else f'[no reason] - {interaction.user}'
        failed = False
        try:
            await member.edit(timed_out_until=None, reason=reason)
        except discord.HTTPException or discord.Forbidden:
            failed = True
        if failed:
            info_embed = discord.Embed(
                title=f'``failed to remove timeout``',
                description=
                f'{self.bot.right} **user**: {member.mention} \n'
                f'**timeout until** : <t:{round(int(mktime(member.timed_out_until.timetuple())))}:f> \n'
                f'``failed?:``{self.bot.success_emoji if failed else self.bot.failed_emoji} \n',
                colour=self.bot.embed_colour, timestamp=discord.utils.utcnow()
            ).set_footer(text='\u200b',
                         icon_url=interaction.user.display_avatar.replace(size=32).url
                         )
        else:
            info_embed = discord.Embed(
                title=f'``{member.name} timeout has been removed ``',
                description=
                f'{self.bot.file_emoji} **reason** : {reason_msg} \n'
                f'{self.bot.right} **moderator**: {member.mention} \n'
                f'**timeout was until** : <t:{round(int(mktime(member.timed_out_until.timetuple())))}:f> \n'
                f'``failed?:``{self.bot.success_emoji if failed else self.bot.failed_emoji} \n',
                colour=self.bot.embed_colour, timestamp=discord.utils.utcnow()
            ).set_footer(text='\u200b',
                         icon_url=interaction.user.display_avatar.replace(size=32).url
                         )
        view = interaction_delete_view(interaction)
        await interaction.followup.send(embed=info_embed, view=view)
        view.message = await interaction.original_message()
        return view.message

    @app_commands.command(name='removetimeout', description='remove timeout of a user')
    @app_commands.guild_only()
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.checks.bot_has_permissions(moderate_members=True)
    @app_commands.describe(
        member='the member who you want to remove timeout',
        reason='the reason to remove timeout of the member'
    )
    async def removetimeout(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):

        if not await is_lower_role(interaction, member=member):
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='timeout command error',
                error_dis="you must have lower role than given member!")
            return
        if not member.is_timed_out():
            await utils.error_embed(
                Interaction=interaction,
                bot=self.bot,
                error_name='timeout command error',
                error_dis='the member is already not timed out')
            return

        # defer the interaction
        await interaction.response.defer()
        # variables
        reason_msg = reason if reason else 'no reason'
        reason = f'[{reason}] - {interaction.user}' if reason else f'[no reason] - {interaction.user}'
        failed = False
        try:
            await member.edit(timed_out_until=None, reason=reason)
        except discord.HTTPException or discord.Forbidden:
            failed = True
        if failed:
            info_embed = discord.Embed(
                title=f'``failed to remove timeout``',
                description=
                f'{self.bot.right} **user**: {member.mention} \n'
                f'**timeout until** : <t:{round(int(mktime(member.timed_out_until.timetuple())))}:f> \n'
                f'``failed?:``{self.bot.success_emoji if failed else self.bot.failed_emoji} \n',
                colour=self.bot.embed_colour, timestamp=discord.utils.utcnow()
            ).set_footer(text='\u200b',
                         icon_url=interaction.user.display_avatar.replace(size=32).url
                         )
        else:
            info_embed = discord.Embed(
                title=f'``{member.name} timeout has been removed ``',
                description=
                f'{self.bot.file_emoji} **reason** : {reason_msg} \n'
                f'{self.bot.right} **moderator**: {member.mention} \n'
                f'**timeout was until** : <t:{round(int(mktime(member.timed_out_until.timetuple())))}:f> \n'
                f'``failed?:``{self.bot.success_emoji if failed else self.bot.failed_emoji} \n',
                colour=self.bot.embed_colour, timestamp=discord.utils.utcnow()
            ).set_footer(text='\u200b',
                         icon_url=interaction.user.display_avatar.replace(size=32).url
                         )
        view = interaction_delete_view(interaction)
        await interaction.followup.send(embed=info_embed, view=view)
        view.message = await interaction.original_message()
        return view.message

    role = app_commands.Group(name='role', description='commands related to roles', guild_only=True,
                              default_permissions=discord.Permissions(manage_roles=True))

    @role.command(name='add', description='easily add roles to a member')
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    @app_commands.describe(
        role='the role that you want to add to the user',
        member='the member that you want to add role to',
        removeadd='that will remove the all roles before adding to the member if set to true',
        hide='run the command anonymously 0-0'
    )
    async def _role_add(self, interaction: discord.Interaction, role: discord.Role, *, member: discord.Member,
                        removeadd: typing.Literal['true', 'false'] = None,
                        hide: typing.Literal['true', 'false'] = None):
        # checks
        if not role.position < interaction.guild.me.top_role.position:
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='bot error',
                error_dis='something sussy happened, i cant assign the roles that is above me')
            return
        if role.is_bot_managed() or role.is_integration() or role.is_premium_subscriber():
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='bot error',
                error_dis='cant assign this role to member, either the role is managed by some type of integration or '
                          'is '
                          'a booster role')
            return
        if not member.top_role.position < interaction.guild.me.top_role.position:
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='bot error',
                error_dis="something sussy happened, i cant assign the roles to the member who's top role is above me")
            return
        if member.id == interaction.user.id and not member.id == interaction.guild.owner.id:
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='role command error',
                error_dis='you cant add roles to your self.')
            return
        if not await is_lower_role(interaction, member):
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='role command error',
                error_dis="lmao fail, you cant add the roles to a member who's role is above you"
            )
            return

        # send the interaction message

        await interaction.response.defer(thinking=True, ephemeral=True if hide == 'true' else False)

        # variables

        failed = False
        removeadd = True if removeadd == 'true' else False
        reason = f"operation done by - {interaction.user} command: /add-role"

        try:
            if removeadd:
                await member.edit(roles=[role], reason=reason)
            else:
                await member.add_roles(role, reason=reason, atomic=False)
        except discord.HTTPException or discord.Forbidden:
            error_emed = discord.Embed(
                title=f"{self.bot.right} failed to add role to __{member.name}__",
                description='>>> reason: something went wrong'
            )
            error_emed.add_field(
                name='details',
                value=f'>>> {self.bot.moderator_emoji} **Moderator:** {interaction.user.mention} \n'
                      f'**member:** {member.mention} \n'
                      f'**role:** {role.mention}'

            )
            view = None
            if hide == 'true':
                view = interaction_error_button(interaction)
                linkbutton = Button(url="https://sussybot.xyz", label="support", style=discord.ButtonStyle.url)
                view.add_item(linkbutton)
            await interaction.followup.send(embed=error_emed, view=view)

            view.message = await interaction.original_message()
            return view.message

        role_info_embed = discord.Embed(title='``role update``')
        role_info_embed.add_field(
            name=f'{self.bot.right} added role to __{member.name}__',
            value=f'>>> {self.bot.moderator_emoji} **Moderator :** {interaction.user.mention} \n'
                  f'**member :** {member.mention} \n'
                  f'role: {role.mention}',
            inline=False
        )
        role_info_embed.add_field(
            name=f'details',
            value=f'>>> removed previous role : ``{removeadd}``',
            inline=False
        )
        if hide == 'true':
            await interaction.followup.send(embed=role_info_embed)
            return
        else:
            view = interaction_delete_view(interaction)
            await interaction.followup.send(embed=role_info_embed, view=view)
            view.message = await interaction.original_message()
            return view.message

    @role.command(name='remove', description='easily remove the roles from a user')
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    @app_commands.describe(
        role='the role you want to remove from the member',
        member='member that you want to remove the role from',
        remove_all='remove all roles from the member',
        hide=' hide interaction response message if set to true'
    )
    async def _role_remove(self, interaction: discord.Interaction,
                           role: discord.Role, member: discord.Member,
                           remove_all: typing.Literal['true', 'false'] = None,
                           hide: typing.Literal['true', 'false'] = None
                           ):
        if not role.position < interaction.guild.me.top_role.position:
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='bot error',
                error_dis='something sussy happened, i cant remove the roles that is above me')
            return
        if role.is_bot_managed() or role.is_integration() or role.is_premium_subscriber():
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='bot error',
                error_dis='cant remove this role to member, either the role is managed by some type of integration or '
                          'is '
                          'a booster role')
            return
        if not member.top_role.position < interaction.guild.me.top_role.position:
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='bot error',
                error_dis="something sussy happened, i cant remove the roles to the member whose top role is above me")
            return
        if member.id == interaction.user.id and not member.id == interaction.guild.owner.id:
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='role command error',
                error_dis='you cant remove roles to your self.')
            return
        if not await is_lower_role(interaction, member):
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='role command error',
                error_dis="lmao fail, you cant remove roles to a member who's role is above you"
            )
            return
        if not member.get_role(role.id) and not remove_all == 'true':
            await utils.error_embed(
                bot=self.bot,
                Interaction=interaction,
                error_name='role command error',
                error_dis=f"bruh this guy doesnt have {role.mention} role"
            )
            return
        # send interaction defer message
        await interaction.response.defer(thinking=False)

        # variable
        failed = False
        removeall = True if remove_all == 'true' else False
        reason = f' operation by :{interaction.user} command:/ role remove'

        if removeall:
            try:
                await member.edit(roles=[], reason=reason)
            except discord.HTTPException or discord.Forbidden:
                failed = True
        else:
            try:
                await member.remove_roles(role, reason=reason, atomic=False)
            except:
                failed = True

        if failed:
            error_emed = discord.Embed(
                title=f"{self.bot.right} failed to remove role from __{member.name}__",
                description='>>> reason: something went wrong'
            )
            error_emed.add_field(
                name='details',
                value=f'>>> {self.bot.moderator_emoji} **Moderator:** {interaction.user.mention} \n'
                      f'**member:** {member.mention} \n'
                      f'**role:** {role if removeall else "all"}'

            )

            view = interaction_error_button(interaction)
            linkbutton = Button(url="https://sussybot.xyz", label="support", style=discord.ButtonStyle.url)
            view.add_item(linkbutton)
            await interaction.followup.send(embed=error_emed, view=view)
            view.message = await interaction.original_message()
            return view.message
        else:
            role_info_embed = discord.Embed(title='``role update``')
            role_info_embed.add_field(
                name=f'{self.bot.right} remove role from __{member.name}__',
                value=f'>>> {self.bot.moderator_emoji} **Moderator :** {interaction.user.mention} \n'
                      f'**member :** {member.mention} \n'
                      f'role: {role.mention}',
                inline=False
            )
            role_info_embed.add_field(
                name=f'details',
                value=f'>>> removed all role : ``{"true" if removeall == "true" else "false"}``',
                inline=False
            )

            if hide == 'true':
                await interaction.followup.send(embed=role_info_embed)
                return
            else:
                view = interaction_delete_view(interaction)
                await interaction.followup.send(embed=role_info_embed, view=view)
                view.message = await interaction.original_message()
                return view.message

    @role.command(name='mass-add')
    async def _role_massadd(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send('hello2')

    @role.command(name='mass-remove')
    async def _role_mass_remove(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send('hello3')

    @app_commands.command(name='rs')
    @app_commands.guild_only()
    async def reactions_role(
            self, interaction: discord.Interaction, role1: discord.Role, role2: discord.Role,
            role3: discord.Role = None, role4: discord.Role = None, *, role5: discord.Role = None,
            role6: discord.Role = None, role_menu_name: str = None,text:str=None
    ):
        await interaction.response.defer()
        messahe = await interaction.original_message()
        await self.bot.db.execute(
            """SELECT * FROM test.rolefunc($1,$2,$3,$4,$5,$6,$7,$8)""",
            interaction.guild.id, messahe.id, role1.id, role2.id, role3.id, role4.id, role5.id, role6.id
        )
        view = reaction_role(self.bot)
        await interaction.followup.send(text,view=view)


async def setup(bot: SussyBot) -> None:
    await bot.add_cog(
        moderation(bot))
