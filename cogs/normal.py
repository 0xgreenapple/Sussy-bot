import discord
import datetime
from discord.ext import commands



class general(commands.Cog):

    def __init__(self, client):
        self.client = client




    @commands.command(description="get a user basic info")
    async def whois(self, ctx, member: discord.Member, ):
        embed10 = discord.Embed(title=member.name, description=member.mention, url=member.avatar_url,
                                 colour=discord.Colour.red())
        embed10.add_field(name="ID", value=member.id, inline=False)
        embed10.add_field(name="status", value=member.status, inline=False)
        embed10.add_field(name="__**join server at**__ ", value=member.joined_at)
        embed10.add_field(name="__**created at**__ ", value=member.created_at)
        embed10.set_thumbnail(url=member.avatar_url)
        await ctx.message.add_reaction("✅")
        await ctx.send(embed=embed10)

    @commands.command(description="do ping to get bot infromation")
    async def ping(self,ctx):
        embed11 = discord.Embed(title="pong! 🏓 latency is "f"{round(self.client.latency * 1000)}ms",description="",url="", colour=discord.Colour.red())
        await ctx.message.add_reaction("🏓")
        await ctx.send(embed=embed11)

        #await ctx.send_message("pong! latency is "f"{round(self.client.latency * 1000)} ms")

    '''@nextcord.slash_command()
    async def info(self, interactions : interactions):
        await ctx.send("owner = green apple#6495")
        await ctx.send("command prefix is " + f"('{self.client.command_prefixs}')")'''

    '''@nextcord.slash_command()
    async def commandlist(self, interactions : interactions):
        await ctx.send("$info| bot info")
        await ctx.send("$kick| kick a member")
        await ctx.send("$ban| ban a member ")
        await ctx.send("$ping| bot latency")
        await ctx.send("$avatar| for user avatar")'''

    @commands.command(description="get a user avatar")
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            embed10 = discord.Embed(title=ctx.message.author.display_name, description="", url=ctx.message.author.avatar_url,
                                   colour=discord.Colour.blue())
            embed10.set_image(url=ctx.message.author.avatar_url)
            await ctx.message.add_reaction("✅")
            await ctx.send(embed=embed10)
            return
        else:
            embed9 = discord.Embed(title=member.display_name, description="", url=member.avatar_url, colour=discord.Colour.blue())
            embed9.set_image(url=member.avatar_url)
            await ctx.message.add_reaction("✅")
            await ctx.send(embed=embed9)


    @commands.command(description= "get list of all commands")
    async def list(self,ctx):
        embed = discord.Embed(title=" commands list :", url="", description="this is the list of all command in the bot"
                                                                           "\n"
                                                                           "__**general commands**__ "
                                                                           "\n"
                                                                           "━━━━━━━━━━━━━━━━━━━━━━━━"
                                                                           , color=0xFF5733)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/917479518040645712/951103745817731132/sussy_server_3.gif")
        embed.add_field(name="__**help**__", value="do ($help) to view command list")
        embed.add_field(name="__**avatar**__", value="do ($avatar <user>) to view user avatars")
        embed.add_field(name="__**ping**__", value="do ($ping) to view user client ping")
        embed.add_field(name="__**info**__ ", value="do ($info) to view bot infromation")

        embed2 = discord.Embed(title="", url="", description="this is the list of all mod commands in the bot"
                                                                           "\n"
                                                                           "__**general mod commands**__ "
                                                                           "\n"
                                                                           "━━━━━━━━━━━━━━━━━━━━━━━━"
                              , color=0xFF5733)
        embed.set_thumbnail(
            url="")
        embed2.add_field(name="__**kick**__", value="do ($kick <user> <reason>) to kick a user")
        embed2.add_field(name="__**ban**__", value="do ($ban <user> <reason>) to ban a user")
        embed2.add_field(name="__**unban**__", value="do ($unban <user> ) to unban a user")
        embed2.add_field(name="__**clear**__ ", value="do ($clear <amount>) to clear the specific amount of messages in the channel")
        await ctx.send(embed=embed)
        await ctx.send(embed=embed2)


def setup(client):
    client.add_cog(general(client))