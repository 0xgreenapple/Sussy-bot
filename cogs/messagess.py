import discord
from discord.ext import commands
import json
from discord import app_commands


class messagess(commands.Cog ,):
    def __init__(self, bot: commands.Bot , ) -> None:
        self.bot = bot



    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.bot:
            with open('messages.json', 'r') as f:
                messagecount = json.load(f)
            await self.update_data1(messagecount, ctx.author, ctx.guild)
            await self.add_experience1(messagecount, ctx.author, 1, ctx.guild)
            with open('messages.json', 'w') as f:
                json.dump(messagecount, f, indent=4)


    async def update_data1(self, messagecount, user, server):
        if not str(server.id) in messagecount:
            messagecount[str(server.id)] = {}
            if not str(user.id) in messagecount[str(server.id)]:
                messagecount[str(server.id)][str(user.id)] = {}
                messagecount[str(server.id)][str(user.id)]['messages'] = 1
        elif not str(user.id) in messagecount[str(server.id)]:
            messagecount[str(server.id)][str(user.id)] = {}
            messagecount[str(server.id)][str(user.id)]['messages'] = 1


    async def add_experience1(self, users, user, exp, server):
        users[str(user.guild.id)][str(user.id)]['messages'] += exp

    @commands.command()
    async def msg(self, ctx):
        user = ctx.message.author
        with open('messages.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(ctx.guild.id)][str(user.id)]['messages']

        embed = discord.Embed(title='you sent {} messages since i joined the server'.format(lvl),
                              color=discord.Color.red())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def messageslb(self, ctx, x=30):
        with open('messages.json', 'r') as f:

            users = json.load(f)

        leaderboard = {}
        total = []

        for user in list(users[str(ctx.guild.id)]):
            name = int(user)
            total_amt = users[str(ctx.guild.id)][str(user)]['messages']
            leaderboard[total_amt] = name
            total.append(total_amt)

        total = sorted(total, reverse=True)

        em = discord.Embed(title=f'Top 10 active members in {ctx.guild.name}',colour=discord.Colour.red())

        index = 1
        for amt in total:
            id_ = leaderboard[amt]
            member = self.bot.get_user(id_)
            em.add_field(name=f'``{index}:`` {member}', value=f' **messages sent :** ``{amt}``', inline=False)
            em.set_footer(text=f"{self.bot.user.name} : infromation requsted by {ctx.author.display_name}", icon_url=self.bot.user.avatar.url)

            if index == x:
                break
            else:
                index += 1

        await ctx.send(embed=em)



    @commands.command()
    async def invites(self,ctx, user : discord.Member = None):
        if user == None:
            totalInvites = 0
            for i in await ctx.guild.invites():
                if i.inviter == ctx.author:
                    totalInvites += i.uses
            embed = discord.Embed(title=ctx.author, description=f"You've invited ``{totalInvites}`` member{'' if totalInvites == 1 else 's'} to the server!" , colour=discord.Colour.red())
            embed.set_footer(text=f"{self.bot.user} : Infromation requested by {ctx.author}",
                             icon_url=self.bot.user.avatar.url)
            await ctx.send(embed = embed)
        else:
            totalInvites = 0
            for i in await ctx.guild.invites():

                if i.inviter == user:
                    totalInvites += i.uses
            embed2 = discord.Embed(title=user,
                                  description=f"{user} invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!")
            embed2.set_footer(text=f"{self.bot.user} : Infromation requested by {user}",
                             icon_url=self.bot.user.avatar.url)
            await ctx.send(embed = embed2)





    #slash command
    @app_commands.command(name="messages_leaderboard", description="show leaderboard by messages sent by user")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    async def messageslbslash(self, interaction : discord.Interaction):
        x=10
        with open('messages.json', 'r') as f:
            users = json.load(f)
        leaderboard = {}
        total = []

        for user in list(users[str(interaction.guild.id)]):
            name = int(user)
            total_amt = users[str(interaction.guild.id)][str(user)]['messages']
            leaderboard[total_amt] = name
            total.append(total_amt)

        total = sorted(total, reverse=True)

        em = discord.Embed(title=f'Top {x} active members in {interaction.guild.name}',colour=discord.Colour.red())

        index = 1
        for amt in total:
            id_ = leaderboard[amt]
            member = self.bot.get_user(id_)
            em.add_field(name=f'``{index}:`` {member}', value=f' **messages sent :** ``{amt}``', inline=False)
            em.set_footer(text=f"{self.bot.user.name} : infromation requsted by {interaction.user.display_name}", icon_url=self.bot.user.avatar.url)

            if index == x:
                break
            else:
                index += 1

        await interaction.response.send_message(embed=em)



    @messageslbslash.error
    async def messageslb_error(self,interaction: discord.Interaction , error : app_commands.AppCommandError):
        if isinstance(error , app_commands.CommandOnCooldown):
            await interaction.response.send_message(error , ephemeral=True)
        else:
            await interaction.response.send_message("something went wrong", ephemeral = True)




    @app_commands.command(name="messages", description="Display amount of messages sent by a user or yourself")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(member="User")
    async def msg2(self,interaction : discord.Interaction , member : discord.Member = None):
        if member is not None:
            user = member
            with open('messages.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(member.guild.id)][str(user.id)]['messages']

            embed = discord.Embed(title='you sent {} messages since i joined the server'.format(lvl),
                              color=discord.Color.red())
            embed.set_author(name=member, icon_url=member.avatar.url)
            await interaction.response.send_message(embed = embed)
        else:
            user = interaction.user
            with open('messages.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(interaction.user.guild.id)][str(user.id)]['messages']

            embed = discord.Embed(title='you sent {} messages since i joined the server'.format(lvl),
                                  color=discord.Color.red())
            embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @msg2.error
    async def message2_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(error, ephemeral=True)
        elif isinstance(error , app_commands.CommandInvokeError):
            await interaction.response.send_message("member name is not in the list", ephemeral = True)
        else:
            await interaction.response.send_message("something went wrong", ephemeral=True)






    @app_commands.command(name="invites",description="display the total invi")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(user = "Member")
    async def invitesslash(self, intercation : discord.Interaction, user: discord.Member = None):
        if user == None:
            totalInvites = 0
            for i in await intercation.guild.invites():
                if i.inviter == intercation.user:
                    totalInvites += i.uses
            embed = discord.Embed(
                                  description=f"You've invited ``{totalInvites}`` member{'' if totalInvites == 1 else 's'} to the server!",
                                  colour=discord.Colour.red(),)
            embed.set_footer(text=f"{self.bot.user} : Infromation requested by {intercation.user}",
                              icon_url=self.bot.user.avatar.url)
            embed.set_author(icon_url=intercation.user.avatar.url,name=intercation.user)

            await intercation.response.send_message(embed=embed)

        else:
            totalInvites = 0
            for i in await user.guild.invites():

                if i.inviter == user:
                    totalInvites += i.uses
            embed2 = discord.Embed(description=f"{user} invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!")
            embed2.set_footer(text=f"{self.bot.user} : Infromation requested by {intercation.user}", icon_url=self.bot.user.avatar.url)
            embed2.set_author(icon_url=user.avatar.url, name=user)
            await intercation.response.send_message(embed=embed2)

    @invitesslash.error
    async def inviteslashe_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(error, ephemeral=True)
        else:
            await interaction.response.send_message("something went wrong", ephemeral=True)
            raise error







async def setup(bot: commands.Bot ) -> None:
    await bot.add_cog(
        messagess(bot))