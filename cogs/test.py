import discord
from discord.ext import commands
from discord import app_commands


import json
class test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='tester',
                  description='testing')  # guild specific slash command
    async def slash2(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"I am working! I was made with Discord.py!", ephemeral=True)

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("hello")
    @commands.command()
    async def changeprefix(self,ctx, prefix):  # command: bl!changeprefix ...
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:  # writes the new prefix into the .json
            json.dump(prefixes, f, indent=4)
        await ctx.message.add_reaction("✅")
        embed = discord.Embed(title=f"prefix changed to {prefix}")
        await ctx.send(embed=embed)





async def setup(bot: commands.Bot ) -> None:
    await bot.add_cog(
        test(bot))

