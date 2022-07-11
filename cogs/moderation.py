from __future__ import annotations

import datetime

import time

import argparse
import logging
import shlex
import typing
from datetime import timedelta
from time import mktime
from typing import Optional, TYPE_CHECKING

import discord
from discord import automod, app_commands
from discord.ext import commands, menus
from discord.ext.commands import cooldown, BucketType
from discord.ext.menus.views import ViewMenuPages

from handler.pagination import SimplePages
from handler.view import delete_view, userinfo
from handler.checks import is_permitted, is_lower_role

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
    def __init__(self, entries: list, *, ctx: Context, per_page: int = 12):
        converted = entries
        log.warning(converted)
        super().__init__(converted, per_page=per_page, ctx=ctx)


async def formate_page(list: list, per_page: int):
    count = 1
    for i in list:
        count += 1
        print(i)


class moderation(commands.Cog):
    """moderation commands"""

    def __init__(self, bot: SussyBot) -> None:
        self.bot = bot

    # delete the message under 14 days.
    async def bulk_delete_advance(
            self, ctx: commands.Context, limit: int = 10, *, check: list = None,
            before=None, after=None, around=None, oldest_first: Optional[bool] = None,
            reason: Optional[str] = None):

        message = discord.utils.utcnow() - timedelta(days=14)

        if len(check) != 0 or check is not None:
            check.append(lambda m: m.created_at >= message)

            def predicate(m):
                r = all(p(m) for p in check)
                return r

            predicate: typing.Callable[[discord.Message], typing.Any] = predicate
            message = await ctx.channel.purge(
                limit=limit, check=predicate, before=before, after=after, around=around,
                oldest_first=oldest_first, bulk=True, reason=reason)
        else:
            message = await ctx.channel.purge(limit=limit, check=lambda m: m.created_at >= message)
        return message

    # clear command
    @commands.guild_only()
    @cooldown(1, 10, BucketType.channel)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.hybrid_command(name='purge', aliases=["clear", "clean"],
                             description="clear the messages of a channel or custom argument "
                                         "provided")
    async def clear(self, ctx: Context, limit: Optional[int] = 10, *, arguments: str = None):

        """advance clear command that delete the messages
         from the channel that is under 14 days as given argument.
         delete the 100 message from the channel if amount not given

         `limit` : the number of messages to delete
         `!user` : delete the message of the user
         `!contain` : delete the message that contain given word
        """
        # emojis

        purge_embed = discord.Embed(colour=self.bot.embed_colour, timestamp=discord.utils.utcnow())
        purge_embed.set_footer(text='\u200b', icon_url=ctx.author.avatar.url)

        view = delete_view(ctx)
        predicates = []
        if arguments:
            parser = Arguments(add_help=False, allow_abbrev=False, prefix_chars="-!")
            parser.add_argument('!user', nargs='+', )
            parser.add_argument('!contain', nargs='+')
            parser.add_argument('!starts', nargs='+')
            parser.add_argument('!embeds', action='store_const', const=lambda m: len(m.embeds))
            parser.add_argument('!files', action='store_const', const=lambda m: len(m.attachments))
            parser.add_argument('!reactions', action='store_const', const=lambda m: len(m.reactions))
            parser.add_argument('!mentions', action='store_const', const=lambda m: len(m.mentions))

            try:
                args = parser.parse_args(shlex.split(arguments))
            except Exception as e:
                await ctx.send(str(e))  # invoke help command here
                return

            if args.embeds:
                predicates.append(args.embeds)
            if args.files:
                predicates.append(args.files)
            if args.reactions:
                predicates.append(args.reactions)
            if args.mentions:
                predicates.append(args.mentions)
            if args.starts:
                predicates.append(lambda m: any(m.content.startswith(s) for s in args.starts))
            if args.contain:
                predicates.append(lambda m: any(sub in m.content for sub in args.contain))
            if args.user:
                users = []
                converter = commands.MemberConverter()
                for u in args.user:

                    try:
                        user = await converter.convert(ctx, u)
                        users.append(user)
                    except Exception as e:
                        embed = discord.Embed(description=f'**{e}**')  # add help command here
                        await ctx.send(embed=embed)
                        return
                predicates.append(lambda m: m.author in users)

        try:
            message = await self.bulk_delete_advance(ctx, limit=limit, check=predicates)
        except discord.Forbidden:
            await ctx.error_embed(error_name="purge command", error_dis="i dont have permission to delete messages")
            return
        purge_embed.add_field(
            name="**Purge result :**",
            value=f">>> used by : {ctx.author.mention} \n"
                  f"{self.bot.channel_emoji} **chanel :** {ctx.channel.mention} \n"
                  f"{self.bot.right} **message requested :** ``{limit}`` \n"
                  f"{self.bot.search_emoji} **deleted :** ``{len(message)}`` \n"
                  f"{self.bot.failed_emoji} failed : ``{limit - len(message)}``")

        view.message = await ctx.send(embed=purge_embed, view=view)

    # warn member
    @commands.group(name='warn', invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx: Context, member: discord.Member, *, reason: Optional[str]):

        if member.id == ctx.author.id:
            await ctx.error_embed(error_name='warn command error', error_dis='you cant warn yourself')
            return
        if member.bot:
            await ctx.error_embed(error_name='warn command error', error_dis='the member you provided cant be banned')
            return
        if not await is_lower_role(ctx, member):
            await ctx.error_embed(error_name='warn command error',
                                  error_dis="you must have lower role than provided member")
            return
        if reason:
            if len(reason) > 250:
                await ctx.error_embed(error_name='warn command error', error_dis='reason length must be '
                                                                                 'under 250 characters')
                return

            # values
        reason_msg = reason if reason else 'for no reason'
        dm_value = True
        warns = await self.bot.db.fetchval(
            """
            SELECT warn FROM moderation.warns
             WHERE guild_id = $1 AND user_id = $2 
            """,
            ctx.guild.id, member.id
        )
        print(warns)
        if warns is not None:
            if len(warns) > 30:
                await self.bot.db.execute(
                    """
                    DELETE warn FROM moderation.warns 
                    WHERE guild_id = $1 AND user_id = $2
                    """,
                    ctx.guild.id, member.id
                )

        warntime = time.mktime(datetime.datetime.now().timetuple())
        await self.bot.db.execute(
            """
                INSERT INTO moderation.warns (guild_id, user_id, warn,datetime,totalwarn)
                VALUES ($1, $2, $3,$4,$5)
                ON CONFLICT (guild_id, user_id) DO
                UPDATE SET warn = array_append(warns.warn,$4) 
                AND 
                """,
            ctx.guild.id, member.id, [reason], warntime, 0, reason
        )
        dm_warn_embed = discord.Embed(title=f'You have been warned in ``{ctx.guild.name}`` server',
                                      description=f'{self.bot.file_emoji} **reason :** {reason_msg}',
                                      timestamp=discord.utils.utcnow())
        dm_warn_embed.set_footer(text='\u200b', icon_url=ctx.author.avatar.url)

        dm_info_embed = discord.Embed(title=f'**``warn``**', timestamp=discord.utils.utcnow())

        try:
            await ctx.send_dm(member=member, embed=dm_warn_embed)
        except discord.HTTPException:
            dm_value = 'failed'
        dm_info_embed.add_field(name=f'{self.bot.right} __{member.name}__ has been warned',
                                value=f'>>> {self.bot.file_emoji} **reason :** {reason} \n'
                                      f'dmed member: ``{dm_value}``')

        dm_info_embed.set_footer(text='\u200b', icon_url=ctx.author.display_avatar.replace(size=32).url)
        view = delete_view(ctx)

        view.message = await ctx.send(embed=dm_info_embed, view=view)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def warns(self, ctx: Context, member: discord.Member):
        warns = await self.bot.db.fetchval(
            """
            SELECT warn FROM moderation.warns
             WHERE guild_id = $1 AND user_id = $2 
            """,
            ctx.guild.id, member.id
        )
        if warns:
            warnings = Warningspages(entries=warns, per_page=5, ctx=ctx)
            await warnings.start()
        if warns is None:
            await ctx.send('this user has no warnings')

    @commands.command(name='clearwarns')
    async def clearwarns(self, ctx: Context):
        """if member.id == ctx.author.id or not member.id == ctx.guild.owner:
            await ctx.error_embed(error_name='warn command error', error_dis='you cant clear yourself warnings')
            return
        if not await is_lower_role(ctx, member):
            await ctx.error_embed(error_name='warn command error',
                                  error_dis="you must have lower role than provided member")
            return"""
        a = datetime.datetime.now()

        await ctx.send(f'<t:{round(int(a))}:R>')

    # kick command
    @app_commands.command(name='kick', description="kick a user")
    @app_commands.guild_only()
    @cooldown(1, 5, BucketType.user)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx: Context, member: discord.Member, *, arguments: str = None):

        """
        kick member with reason if given
        `!reason` : kick a member of the server with reason if provided
        `!dm` : store value true dm member on kick
        """
        # kick embed
        right_arrow = self.bot.get_emoji(975326725158346774)
        reason_emoji = self.bot.get_emoji(975326725229641781)
        ejected = self.bot.get_emoji(991340144202350663)
        kick_embed = discord.Embed(title=f'{ejected} ``Kick``')
        kick_embed.set_footer(text='\u200b', icon_url=ctx.author.avatar.url)

        if member == ctx.author:
            await ctx.error_embed(
                error_name='kick command error',
                error_dis='you cant kick your self. are you crazy')
            return

        if not await is_lower_role(ctx, member):
            await ctx.error_embed(error_name='kick command error',
                                  error_dis="you must have lower role than member")
            return

        reason = ' '
        dm = None
        dm_value = ''
        if arguments:
            parser = Arguments(add_help=False, allow_abbrev=False, prefix_chars="-!")
            parser.add_argument('!reason', nargs='+', )
            parser.add_argument('!dm', action='store_true')

            try:
                args = parser.parse_args(shlex.split(arguments))
            except Exception as e:
                await ctx.send(str(e))  # add help command here
                return

            if args.dm:
                dm = args.dm

            if args.reason:
                reason = reason.join(args.reason)
                kick_embed.description = f'{reason_emoji} **reason :** {reason}'
            else:
                reason = None
                kick_embed.description = f'{reason_emoji} **reason :** no reason provided'

        if dm:
            try:
                await ctx.send_dm(member=member, message=f"you have been kicked from the server for {reason} ")
                dm_value = True
            except discord.Forbidden or discord.HTTPException:
                dm_value = 'dm failed'

        try:
            dm_value = dm_value if dm_value else 'false'
            reason = reason if reason else None

            await ctx.guild.kick(user=member, reason=reason)
        except discord.Forbidden or discord.HTTPException:
            await ctx.send(embed=kick_embed)

        kick_embed.add_field(name='__**kick details**__',
                             value=f'>>> {right_arrow} **moderator :** {ctx.author.mention} \n'
                                   f'**dmed member? :** {dm_value} ', inline=False)
        kick_embed.add_field(name='__**member details**__',
                             value=f'>>>  {right_arrow} **username :** ``{member}`` \n'
                                   f'``ID``:{member.id} \n'
                                   f'**server joined at :** <t:{round(int(mktime(member.joined_at.timetuple())))}:D>\n '
                                   f'**created at :** <t:{round(int(mktime(member.created_at.timetuple())))}:D>')
        view = delete_view(ctx)
        view.message = await ctx.send(embed=kick_embed, view=view)

    # masskick
    @commands.guild_only()
    @commands.command(name='masskick', aliases=['multikick'], description="kick multiple users")
    @cooldown(1, 30, BucketType.guild)
    @commands.has_permissions(kick_members=True)
    @commands.has_permissions(manage_guild=True)
    async def masskick(self, ctx: Context, members: commands.Greedy[discord.Member], *, reason: str = None):

        """
        mass kick command that can kick multiple members.
        in order to execute this command the user must have manage_guild
        permission and bot must have kick members permission
        """
        msg_reason = reason if reason else "for no reason"

        if len(members) == 0:
            await ctx.error_embed(error_name='kick command error', error_dis="members argument is missing")
            return

        failed = 0
        a = 0
        member_kicked = []
        member_list = ' '
        for member in members:
            if ctx.author != member or await is_lower_role(ctx, member=member):
                logging.warning(member.name)
                try:
                    await ctx.guild.kick(user=member, reason=reason)
                    member_kicked.append(member.name)
                except discord.HTTPException:
                    failed += 1

        mass_kick_embed = discord.Embed(title='`` mass kick``', description=f'**reason :** {msg_reason}',
                                        timestamp=discord.utils.utcnow())
        member_list = ', '.join(member_kicked)
        mass_kick_embed.add_field(
            name='__**details**__',
            value=f'>>> **moderator :** {ctx.author.mention} \n'
                  f'**users requested :** ``{len(members)}`` \n'
                  f'**failed :** ``{failed}``',
            inline=False)

        mass_kick_embed.add_field(
            name='__**users kicked**__',
            value=f'>>> ``{member_list}``')

        mass_kick_embed.set_footer(text='\u200b', icon_url=ctx.author.avatar.url)

        view = delete_view(ctx)

        view.message = await ctx.send(embed=mass_kick_embed, view=view)

        # kick command

    @commands.guild_only()
    @cooldown(1, 5, BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(name='ban', description="ban a user from the server")
    async def ban(self, ctx: Context, member: typing.Union[discord.Member, discord.User], *, arguments: str = None):

        """
        ban member with reason if given
        `!reason` : kick a member of the server with reason if provided
        `!dm` : store value true dm member on kick
        `!days` : delete message days
        """
        # kick embed
        right_arrow = self.bot.get_emoji(975326725158346774)
        reason_emoji = self.bot.get_emoji(975326725229641781)
        ejected = self.bot.get_emoji(991340144202350663)
        ban_embed = discord.Embed(title=f'{ejected} ``ban``')
        ban_embed.set_footer(text='\u200b', icon_url=ctx.author.avatar.url)
        member_or_not = ctx.guild.get_member(member.id)
        if member == ctx.author:
            await ctx.error_embed(
                error_name='ban command error',
                error_dis='you cant ban your self! are you crazy?')
            return

        if member_or_not:
            if not await is_lower_role(ctx, member):
                await ctx.error_embed(error_name='ban command error',
                                      error_dis="you must have lower role than given member!")
                return

        reason = ' '
        dm = None
        dm_value = ''
        delete = 1
        if arguments:
            parser = Arguments(add_help=False, allow_abbrev=False, prefix_chars="-!")
            parser.add_argument('!reason', '!r', nargs='+', )
            parser.add_argument('!days', type=int)
            parser.add_argument('!dm', action='store_true')

            try:
                args = parser.parse_args(shlex.split(arguments))
            except Exception as e:
                await ctx.send(str(e))  # add help command here
                return

            if args.dm:
                dm = args.dm

            if args.days:
                if args.days < 7:
                    delete = args.days
                elif args.days > 7:
                    delete = 7

            if args.reason:
                reason = reason.join(args.reason)
                ban_embed.description = f'{reason_emoji} **reason :** {reason}'
            else:
                reason = None
                ban_embed.description = f'{reason_emoji} **reason :** no reason provided'

        if dm:
            try:
                await ctx.send_dm(member=member, message=f"you have been banned from the server for {reason} ")
                dm_value = True
            except discord.Forbidden or discord.HTTPException:
                dm_value = 'dm failed'
        try:
            dm_value = dm_value if dm_value else 'false'
            reason = reason if reason else None
            await ctx.guild.ban(user=member, reason=reason, delete_message_days=delete)
        except discord.Forbidden or discord.HTTPException:
            await ctx.error_embed(error_name='ban command error', error_dis='something went wrong')
            return
        if reason is None:
            ban_embed.description = f'{reason_emoji} **reason :** no reason provided'
        ban_embed.add_field(name='__**ban details**__',
                            value=f'>>> {right_arrow} **moderator :** {ctx.author.mention} \n'
                                  f'**dmed member? :** {dm_value} \n'
                                  f'**delete message days :** ``{delete}``', inline=False)
        if member_or_not:
            ban_embed.add_field(name='__**member details**__',
                                value=f'>>>  {right_arrow} **username :** ``{member}`` \n'
                                      f'``ID``:{member.id} \n'
                                      f'**joined at :** <t:{round(int(mktime(member.joined_at.timetuple())))}:D>\n '
                                      f'**created at :** <t:{round(int(mktime(member.created_at.timetuple())))}:D>')
        else:
            ban_embed.add_field(name='__**member details**__',
                                value=f'>>>  {right_arrow} **username :** ``{member}`` \n'
                                      f'``ID``:{member.id} \n'
                                      f'**created at :** <t:{round(int(mktime(member.created_at.timetuple())))}:D>')
        view = delete_view(ctx)
        view.message = await ctx.send(embed=ban_embed, view=view)

    @commands.command(name='unban', description="unban a user or multiple user in best way possible")
    @commands.guild_only()
    @cooldown(1, 5, BucketType.guild)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx: Context, member: commands.Greedy[discord.User], *, reason: Optional[str]):
        """unban a user or multiple!
        unban a user with reason if given
        `member`: user to unban
        `reason`: unban reason (optional)
        """

        reason_msg = reason if reason else 'no reason provided'
        Users = member
        failed = 0
        ban_embed = discord.Embed(title='``unban``',
                                  description=f'**reason :** {reason_msg}')
        if len(Users) == 0:
            await ctx.error_embed(error_name='unban command error', error_dis='the member argument is missing')
            return
        elif len(Users) > 5:
            await ctx.error_embed(error_name='unban command error', error_dis='You can only ban maximum 5 users at one '
                                                                              'time')
            return
        for user in Users:
            try:
                await ctx.guild.unban(user=user, reason=reason)
            except discord.NotFound:
                if len(Users) == 1:
                    await ctx.error_embed(error_name='unban command error',
                                          error_dis='user is not banned')
                    return
                else:
                    failed += 1
            except discord.HTTPException:
                if len(Users) == 1:
                    await ctx.error_embed(error_name='unban command error',
                                          error_dis='something went wrong while unbanning a user')
                    return
                else:
                    failed += 1
        ban_embed.add_field(name='__**ban details**__',
                            value=f'>>> {self.bot.right} **moderator :** {ctx.author.mention} \n'
                                  f'**failed :** ``{failed}``', inline=False)
        if len(Users) == 1:
            user = ' '
            for user in Users:
                user = user
            ban_embed.add_field(name='__**user details**__',
                                value=f'>>>  {self.bot.right} **username :** ``{user.name}`` \n'
                                      f'``ID``:{user.id} \n'
                                      f'**created at :** <t:{round(int(mktime(user.created_at.timetuple())))}:D>')
        else:
            users = ' '
            for user in Users:
                users = ', '.join(user.name)
            ban_embed.add_field(name='__**users**__',
                                value=f'>>> ``{users}``')
        view = delete_view(ctx)
        view.message = await ctx.send(embed=ban_embed, view=view)

    @commands.command(name='leave')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx: Context):
        guild = ctx.guild
        await guild.leave()


async def setup(bot: SussyBot) -> None:
    await bot.add_cog(
        moderation(bot))
