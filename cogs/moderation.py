from __future__ import annotations

import asyncpg
import datetime

import time

import argparse
import logging
import shlex
import typing
from time import mktime
from typing import Optional, TYPE_CHECKING

import discord
from discord import automod, app_commands
from discord.ext import commands, menus
from discord.ext.commands import cooldown, BucketType
from discord.ext.menus.views import ViewMenuPages

from handler.pagination import SimplePages
from handler.view import delete_view, userinfo, interaction_delete_view
from handler.checks import is_permitted, is_lower_role
from datetime import timedelta
from discord.app_commands import Choice
from enum import Enum
from handler import utils

if TYPE_CHECKING:
    from bot import SussyBot
    from handler.Context import Context

# setup logging
log = logging.getLogger(__name__)


class Arguments(argparse.ArgumentParser):
    def error(self, message: str):
        raise RuntimeError(message)


class MySource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=4)

    async def format_page(self, menu, entries):
        print(entries)
        offset = menu.current_page * self.per_page

        return '\n'.join(f'{i}. {v}' for i, v in enumerate(entries, start=offset))


class EmbedPageSource(menus.ListPageSource):
    async def format_page(self, menu, item):
        embed = discord.Embed(title=item)
        # you can format the embed however you'd like
        return embed


class Warningspages(SimplePages):
    def __init__(self, entries: list, *, ctx: discord.Interaction, per_page: int = 12, title: str = None):
        converted = entries
        print(entries)
        super().__init__(converted, per_page=per_page, ctx=ctx, title=title)


class True_Or_False(Enum):
    true = True
    false = False


async def formate_page(list: list, per_page: int):
    count = 1
    for i in list:
        count += 1
        print(i)


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
    @app_commands.command(name='purge', description="clear the messages of a channel in best way possible")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.guild_only()
    @app_commands.describe(
        contain='delete the message that content given word. separate by comma',
        startswith='delete the messages that starts with given word. separate by comma',
        user='only delete the message of specific user',
        embeds='delete the message that contain embeds',
        files='delete the message contains files',
        reactions='delete the message contains reactions',
        delete_type='If set true, delete only messages matching all conditions'
    )
    async def clear(self, interaction: discord.Interaction, limit: app_commands.Range[int, 1, 100] = 10,
                    delete_type: typing.Literal['true', 'false'] = None, *,
                    user: typing.Union[discord.Member, discord.User] = None,
                    contain: str = None, startswith: str = None, endswith: str = None,
                    embeds: typing.Literal['true', 'false'] = None,
                    files: typing.Literal['true', 'false'] = None, reactions: typing.Literal['true', 'false'] = None,
                    mentions: typing.Literal['true', 'false'] = None):

        """advance clear command that delete the messages
         from the channel that is under 14 days as given argument.
         delete the 100 message from the channel if amount not given

         `limit` : the number of messages to delete
         `!user` : delete the message of the user
         `!contain` : delete the message that contain given word
        """
        # emojis

        purge_embed = discord.Embed(colour=self.bot.embed_colour, timestamp=discord.utils.utcnow())
        purge_embed.set_footer(text='\u200b', icon_url=interaction.user.avatar.url)

        view = interaction_delete_view(interaction)
        message = discord.utils.utcnow() - timedelta(days=14)
        predicates = []

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

        await interaction.response.send_message(embed=purge_embed, view=view)
        view.message = await interaction.original_message()

    # warn member
    @app_commands.guild_only()
    @app_commands.command(name='warn', description='warn a user with reason')
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members=True)
    @app_commands.default_permissions(kick_members=True)
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(
        member='member to warn, |id|mention|tag|',
        reason='reason for warn'
    )
    async def warn(self, interaction: discord.Interaction, member: discord.Member, *,
                   reason: app_commands.Range[str, 1, 250] = None):

        if member.id == interaction.user.id:
            print('cant war yourself')
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
    @app_commands.command(name='warns')
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

    @app_commands.command(name='clearwarnings', description='clear the warnings of a user')
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
        allcleard = False
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
            allcleard = True
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
    @app_commands.command(name='kick', description="kick a user")
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
                channel = await member.create_dm()
                await channel.send(f"you have been kicked from the server for "
                                   f"{reason} ")
                dm_value = True
            except discord.Forbidden or discord.HTTPException:
                dm_value = 'dm failed'
        try:

            dm_value = dm_value if dm_value else 'false'
            reason = reason if reason else None
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
        log.warning('started')
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
        log.warning('middile')
        delete = days if days else 0
        created_at = round(int(mktime(user.created_at.timetuple())))
        joined_at = round(int(mktime(user.joined_at.timetuple()))) if member_or_not else None
        dm_value = ''
        log.warning('reason')
        if reason:
            log.warning('setting up reason')
            ban_embed.description = f'{self.bot.file_emoji} **reason :** {reason}'
        else:
            reason = None
            ban_embed.description = f'{self.bot.file_emoji} **reason :** no reason provided'

        log.warning('dm')
        if dm == 'true' and not user.bot:
            log.warning('trying to send dm')
            try:
                log.warning('createdm')
                channel = await user.create_dm()
                log.warning('senddm')
                await channel.send(f"you have been banned from the server for {reason} ")
                log.warning('succes')
                dm_value = True
                log.warning('succes')
            except discord.Forbidden or discord.HTTPException:
                log.warning('failed')
                dm_value = 'dm failed'
        try:
            log.warning('ban reached')
            dm_value = dm_value if dm_value else 'false'
            reason = reason if reason else None
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
        log.warning('tring to send the message')
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

    @commands.command(name='leave')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx: Context):
        guild = ctx.guild
        await guild.leave()


async def setup(bot: SussyBot) -> None:
    await bot.add_cog(
        moderation(bot))
