import discord
import datetime
import warnings
from discord.ext import commands, tasks



class help(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.group(invoke_without_command=True)
    async def help(self,ctx):
        em = discord.Embed(title="__**commands**__",description="this is the list of all category ",colour=discord.Colour.red())
        em.set_author(name="Sussy Server plugins commands ",icon_url="https://cdn.discordapp.com/avatars/953274927027458148/0acc66836632c839426a39fd97e240a3.webp?size=1024",
                      )
        em.set_thumbnail(url="https://cdn.discordapp.com/avatars/953274927027458148/0acc66836632c839426a39fd97e240a3.webp?size=1024")
        em.add_field(name="Modrator", value="``$help mod``")
        em.add_field(name="Fun",value="``$help fun``")
        em.add_field(name="General",value="``$help general``")
        em.add_field(name="Rules",value="``$help rules``")
        em.set_footer(text=f"infromation requested by {ctx.message.author.display_name}",icon_url=ctx.message.author.avatar_url)


        await ctx.send(embed=em)

    @help.command()
    async def mod(self,ctx):
        em = discord.Embed(title="__**mod plugins**__",description="**``$kick <user> <reason optional>``**"
                                                                   "\n"
                                                                   "kick a user for guild"
                                                                   "\n"
                                                                   "\n"
                                                                   "**``$ban <user> <reason optional>``**"
                                                                   "\n"
                                                                   "ban a user from the guild"
                                                                   "\n"
                                                                   "\n"
                                                                   "**``$unban <user> <reason optional>``**"
                                                                   "\n"
                                                                   "unban a banned user in the guild"
                                                                   "\n"
                                                                   "\n"
                                                                   "**``$mute <user>``**"
                                                                   "\n"
                                                                   "mute a random user from the guild"
                                                                   "\n")
        '''em.add_field(name="``$kick <user> <reason optional>``",value="kick a user for guild",)
        em.add_field(name="",value="")
        em.add_field(name="``$ban <user> <reason optional>``",value="ban a user from the guild",inline=False)
        em.add_field(name="``$unban <user> <optional>``",value="unban a banned user",inline=False)
        em.add_field(name="``$mute <user> <reason optional>``",value="mute a random user from the guild",inline=False)'''
        await ctx.send(embed=em)





def setup(client):
    client.add_cog(help(client))