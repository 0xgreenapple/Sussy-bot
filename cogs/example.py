import discord
import datetime
import warnings
from discord.ext import commands, tasks



class Modcommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    def is_it_me(self, ctx):
        return ctx.guild.id == 946345220625277030

    '''@commands.cog.listener()
    async def on_ready(self):
        print("bot is online")
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='imhrs'))'''

    '''@commands.command()
    async def timeout_user(self,*, user_id: int, guild_id: int, until):
        headers = {"Authorization": f"Bot {self.client.http.token}"}
        url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
        timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=until)).isoformat()
        json = {'communication_disabled_until': timeout}
        async with self.client.session.patch(url, json=json, headers=headers) as session:
            if session.status in range(200, 299):
                return True
            return False'''


    @commands.command(description="clear messages")
    @commands.has_permissions(kick_members=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)


    @commands.command(description="kick a random user")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if reason == None:
            reason = " no reason provided"
        await ctx.guild.kick(member)
        await ctx.channel.send(f'User {member.mention} has been kicked for {reason}')

    @commands.command(description="ban a random user")
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, member: discord.Member, *, reason=None):
        if reason == None:
            reason = " no reason provided"
        await ctx.guild.ban(member)
        await ctx.channel.send(f'User {member.mention} has been banned for {reason}')



#==========================================================================
    '''@commands.command(description="ban a random user")
    @commands.has_permissions(ban_members=True)
    async def timeout(self, ctx, member: discord.Member, *, reason=None):
        if reason == None:
            reason = " no reason provided"
        await ctx.guild.time(member)
        await ctx.channel.send(f'User {member.mention} has been banned for {reason}')'''

    '''@commands.command(description="kick any random user")
    @commands.has_permissions(kick_members=True)
    async def mute(self,ctx, member: discord.Member):
        if ctx.guild.id == 946345220625277030:
            muted_role = 957305814996107294
            await ctx.member.add_roles(muted_role)
            await ctx.channel.send(member.mention + "has been muted")'''

    '''@commands.command(pass_context=True)
    async def mute(self, ctx, member: discord.Member):
        if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '194151340090327041':
            role = discord.utils.get(member.server.roles, name='Muted')
            await ctx.add_roles(member, role)
            embed = discord.Embed(title="User Muted!",
                                  description="**{0}** was muted by **{1}**!".format(member, ctx.message.author),
                                  color=0xff00f6)
            await ctx.say(embed=embed)
        else:
            embed = discord.Embed(title="Permission Denied.",
                                  description="You don't have permission to use this command.", color=0xff00f6)
            await ctx.say(embed=embed)'''

    '''@commands.command(description="mutes the specified user.")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.member, *, reason=None):
        guild = ctx.guild
        muterole = discord.utils.get(guild.roles, name="Muted")

        if not muterole:
            muterole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permission(muterole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        await member.add_roles(muterole, reason=reason)
        await ctx.send(f"Muted {member.mention} for reason {reason}")
        await member.send(f'you were muted server {guild.name} for {reason}')'''
# ==========================================================================



    @commands.command(description="unban a random user")
    @commands.has_permissions(administrator=True)
    async def unban(self,ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send(f'Unbanned {user.mention}')
                return




def setup(client):
    client.add_cog(Modcommands(client))
