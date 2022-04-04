import discord
import os
from discord.ext import commands
from itertools import cycle


class error(commands.Cog):
    def __init__(self, client):
        self.client = client


    '''@commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """A global error handler cog."""

        if isinstance(error, commands.CommandNotFound):
            message = "https://tenor.com/view/pixelplace-gif-24586548"
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissions to run this command!"
        elif isinstance(error, commands.UserInputError):
            message = "Something about your input was wrong, please check your input and try again!"
        elif isinstance(error, commands.NotOwner):
            message = "you dont own me but your mom"
        elif isinstance(error,  commands.BotMissingPermissions):
            message = "i m missing some permissions"
        elif isinstance(error,  commands.UserNotFound):
            message = "try pinging your mom !"
        else:
            message = "fucking what just happend"

        await ctx.message.add_reaction("🚫")
        await ctx.send(message, delete_after=5)
        await ctx.message.delete(delay=10)'''




def setup(client):
    client.add_cog(error(client))