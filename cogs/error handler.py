import discord
import os

from discord.app_commands import tree
from discord.ext import commands
from discord import app_commands
from discord.errors import Forbidden
from itertools import cycle



class error_handler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error



    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """A global error handler cog."""

        if isinstance(error, commands.CommandNotFound):
            await ctx.send("https://tenor.com/view/pixelplace-gif-24586548")
            return
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds.")
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="You are missing the required permissions to run this command!")
        elif isinstance(error, commands.UserInputError):
            embed = discord.Embed(title="Something about your input was wrong, please check your input and try again!")
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(title="you dont own me but your mom")
        elif isinstance(error,  commands.BotMissingPermissions):
            embed = discord.Embed(title="i m missing some permissions")
        elif isinstance(error,  commands.UserNotFound):
            embed = discord.Embed(title="try to put your mom username its should be work !")
        else:
            embed = discord.Embed(title="something went wrong report the bug by doing ``$bug <bug>``| ")

        await ctx.message.add_reaction("🚫")
        await ctx.send(embed=embed, delete_after=10)
        await ctx.message.delete(delay=15)

    async def on_app_command_error(self,interaction: discord.Interaction,error: app_commands.AppCommandError):
        if isinstance(error,app_commands.CommandOnCooldown):
            embed = discord.Embed(title="Command On cooldown",description=f"Woah stop command is Currently on Cool down try again in {round(error.retry_after,1)}",
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
            embed = discord.Embed(title="No privet channe;",
                                  description=f"this command cant run in privet channel",
                                  colour=discord.Colour.gold())
        elif isinstance(discord.errors, discord.errors.Forbidden):
            embed = discord.Embed(title="bot missing permmision;",
                                  colour=discord.Colour.gold())
        else:
            embed = discord.Embed(title="Command invoke error",
                                  description=f"Something went wrong pls report the error in our support server \n"
                                              f"**website** : https: sussybot.xyz \n"
                                              f"**support server** : https://discord.gg/wC37kY3qwH",
                                  colour=discord.Colour.gold())
        await interaction.response.send_message(embed = embed, ephemeral=True)





async def setup(bot: commands.Bot ) -> None:
    await bot.add_cog(
        error_handler(bot))
