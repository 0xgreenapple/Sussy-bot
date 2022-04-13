import discord
import datetime
import warnings
from discord.ext import commands, tasks
from discord import app_commands



class example(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot








    @app_commands.command(name="clean", description="clear messages")
    @app_commands.checks.has_permissions(manage_messages = True)
    @app_commands.checks.cooldown(1,5, key=lambda j:(j.guild_id,j.user.id))
    async def clearcommand(self, interaction: discord.Interaction,amount : int = 5):
        await interaction.channel.purge(limit=amount)
        await interaction.response.defer( ephemeral= True)
        await interaction.followup.send(f"{amount} message deleted from channel succesfully",)



    @clearcommand.error
    async def clearcommand_error(self, interaction : discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error ,app_commands.MissingPermissions):
            await interaction.response.send_message("your mom, go and get some permissions first", ephemeral= True)
        elif isinstance(error ,app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"{error}", ephemeral= True)
        else:
            await interaction.response.send_message(f"something wen wrong do $help for help $bugs for reporting a bug", ephemeral=True)



    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def clear(self,ctx, amount=5):
        await ctx.channel.purge(limit = amount)






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




    @commands.command(description="unban a random user")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send(f'Unbanned {user.mention}')
                return

    @commands.command(aliases = ["gl"])
    @commands.is_owner()
    async def guild_leave(self, ctx ,guildid):
        guild = await self.client.fetch_guild(int(guildid))
        await guild.leave()
        embed = discord.Embed(title=f"i left the guild {guild.name} ")
        await ctx.send(embed = embed)


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



    '''@commands.command(description="unban a random user")
    @commands.has_permissions(administrator=True)
    async def unban(self,ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send(f'Unbanned {user.mention}')
                return'''




async def setup(bot: commands.Bot ) -> None:
    await bot.add_cog(
        example(bot))
