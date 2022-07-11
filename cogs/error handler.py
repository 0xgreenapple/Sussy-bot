import logging
import sys
import traceback

import discord
from discord.ext import commands, menus
from discord import app_commands
from bot import SussyBot
from handler.Context import Context
from handler import errors

log = logging.getLogger(__name__)


class error_handler(commands.Cog):
    def __init__(self, bot: SussyBot) -> None:
        self.bot = bot

        bot.tree.on_error = self.on_app_command_error

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):

        """A global error handler cog."""
        error_emoji = self.bot.get_emoji(975326725426778184)

        if isinstance(error, commands.NotOwner):
            return

        elif isinstance(error, (commands.CommandNotFound, commands.DisabledCommand)):
            return

        # handel the command cooldown
        elif isinstance(error, commands.CommandOnCooldown):
            error_name = "command on cooldown"
            error_dis = f"{ctx.command.name} command is currently on cooldown try again after {round(error.retry_after)} seconds".title()
            return await ctx.error_embed(error_name=error_name, error_dis=error_dis)

        elif isinstance(error, commands.MissingRequiredArgument):
            name = "missing argument"
            des = f"{error}"
            return await ctx.error_embed(error_name=name, error_dis=des)
        elif isinstance(error, errors.CannotsendEmbeds):
            return await ctx.send(
                f'``{ctx.command.qualified_name}`` command cant be executed. to run the command give me following '
                f'permissions!\n '
                f'**```yml\n'
                f'= embed links \n'
                f'= external emojis```**')

        elif isinstance(error, (commands.BadArgument, commands.BadUnionArgument)):
            name = f"invalided input_"
            des = f"{error}"
            return await ctx.error_embed(error_name=name, error_dis=des)

        elif isinstance(error, commands.UserInputError):
            name = f"wrong input"
            des = "there is something wrong about your input for more info type on help"
            return await ctx.error_embed(error_name=name, error_dis=des)

        elif isinstance(error, commands.UserNotFound):
            name = f"user not found",
            des = f"the user that you entered not found"
            return await ctx.error_embed(error_name=name, error_dis=des)

        # handel the missing permission
        elif isinstance(error, commands.MissingPermissions):
            if ctx.channel.type is discord.ChannelType.private:
                return
            permissions = ' '.join(error.missing_permissions)
            name = "Missing permissions",
            value = f'you are missing permissions to run the command \n``{permissions}``'
            return await ctx.error_embed(error_name=name, error_dis=value)

        # handel the bot missing permission error
        elif isinstance(error, commands.BotMissingPermissions):
            if ctx.channel.type is discord.ChannelType.private:
                return
            missing = ', '.join(error.missing_permissions)
            name = "bot missing permissions"
            des = f"i am missing some permission to run the command \n ``{missing}``"
            return await ctx.error_embed(error_name=name, error_dis=des)

        # handel the guild only error
        elif isinstance(error, commands.NoPrivateMessage):
            embed = discord.Embed(
                title=f"{error_emoji} ``OPERATION FAILED``",
                colour=self.bot.embed_colour,
                timestamp=discord.utils.utcnow())
            embed.add_field(
                name="__**Guild only command**__",
                value=">>> this command can be only execute in the servers")
            embed.set_footer(text='\u200b', icon_url=ctx.author.avatar.url)
            return await ctx.reply(embed=embed)

        elif isinstance(error, commands.CommandInvokeError):

            if isinstance(error.original, discord.HTTPException) and error.original.code == 50001:
                logging.warning(f"bot missing access in {ctx.guild}")

            if isinstance(error.original, discord.HTTPException) and error.original.code == 50006:
                name = f"user not found",
                des = f"give me something to send i cannot send empty message> if you think this is a error report it by clicking on support "
                return await ctx.error_embed(error_name=name, error_dis=des)

            elif isinstance(error.original, menus.CannotEmbedLinks):
                return await ctx.reply("i m missing permission cannot send embeds "
                                       "please give me permission to send embed links")

            elif isinstance(error.original, menus.CannotAddReactions):
                name = f"cannot add reaction",
                des = f"i am not able to add reaction to messages. this is kinda sus please give me permission to add " \
                      f"reaction to messages "
                return await ctx.error_embed(error_name=name, error_dis=des)

            # handel cannot read message error while adding menus
            elif isinstance(error.original, menus.CannotReadMessageHistory):
                embed = discord.Embed(
                    title=f"{error_emoji} ``OPERATION FAILED``",
                    colour=self.bot.embed_colour,
                    timestamp=discord.utils.utcnow())
                embed.add_field(
                    name=f"__**cannot read messages**__",
                    value=f">>> i m missing permission cannot read messages "
                          "please give me permission read messages")
                return await ctx.reply(embed=embed)

            # Bot missing permissions (Unhandled)
            elif isinstance(error.original, (discord.Forbidden, menus.CannotSendMessages)):
                log.info(
                    f"Missing Permissions for {ctx.command.qualified_name} in #{ctx.channel.name} in {ctx.guild.name} code : {error.original.code}")
                return await ctx.send('hello'
                )

            # Discord Server Error
            elif isinstance(error.original, discord.DiscordServerError):
                return log.info(f"Discord Server Error for {ctx.command.qualified_name}: {error.original}")
            else:
                # All other Errors not returned come here. And we can just print the default TraceBack.
                print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
                traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    async def on_app_command_error(self, ctx, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(title="Command On cooldown",
                                  description=f"Woah stop command is Currently on Cool down try again in {round(error.retry_after, 1)}",
                                  colour=discord.Colour.gold())
        elif isinstance(error, app_commands.BotMissingPermissions):
            embed = discord.Embed(title="Missing permission",
                                  description=f"i have not permission to do that pls do **``help <command>``** to view required permission to run this command",
                                  colour=discord.Colour.gold())

        elif isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(title="permission denied",
                                  description=f"The command cannot be run because you do not have the required permissions, ``$help_command to view required permission to run this command",
                                  colour=discord.Colour.gold())
        elif isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Command invoke error",
                                  description=f"Something went wrong pls report the error in our support server \n"
                                              f"**website** : https: sussybot.xyz \n"
                                              f"**support server** : https://discord.gg/wC37kY3qwH",
                                  colour=discord.Colour.gold())
        elif isinstance(error, app_commands.NoPrivateMessage):
            embed = discord.Embed(title="No privet channel;",
                                  description=f"this command cant run in privet channel",
                                  colour=discord.Colour.gold())
        elif isinstance(discord.errors, discord.errors.Forbidden):
            embed = discord.Embed(title="bot missing permission;",
                                  colour=discord.Colour.gold())
        else:
            embed = discord.Embed(title="Command invoke error",
                                  description=f"Something went wrong pls report the error in our support server \n"
                                              f"**website** : https: sussybot.xyz \n"
                                              f"**support server** : https://discord.gg/wC37kY3qwH",
                                  colour=discord.Colour.gold())
        await ctx.send(embed=embed, ephemeral=True)


async def setup(bot: SussyBot) -> None:
    await bot.add_cog(
        error_handler(bot))
