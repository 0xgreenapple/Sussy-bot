import discord
import os
from discord.ext import commands
from discord import app_commands
from itertools import cycle


class error_handler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


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




async def setup(bot: commands.Bot ) -> None:
    await bot.add_cog(
        error_handler(bot))
