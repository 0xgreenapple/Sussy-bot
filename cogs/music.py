import discord
from discord.ext import commands
from discord import app_commands





class music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def join(self,ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()


async def setup(bot: commands.Bot ) -> None:
    await bot.add_cog(
        music(bot))