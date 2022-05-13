import discord
from discord.ext import commands
import json
from discord import app_commands
from bot import SussyBot


class messagess(commands.Cog):
    def __init__(self, bot: SussyBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.bot:
            await self.bot.db.execute(
                """
                INSERT INTO chat.messagecount (guild_id, user_id, message)
                VALUES ($1,$2, 1)
                ON CONFLICT (guild_id,user_id) DO 
                UPDATE SET message = COALESCE(messagecount.message, 0) + 1 
                """,
                ctx.guild.id, ctx.author.id
            )

    @commands.command()
    async def msg(self, ctx):
        user = ctx.message.author
        lvl = await self.bot.db.fetchval(
            """
            SELECT message
            FROM chat.messagecount
             WHERE user_id=$1 AND guild_id = $2
            """,
            ctx.author.id, ctx.guild.id
        )

        embed = discord.Embed(title='you sent {} messages since i joined the server'.format(lvl),
                              color=self.bot.yellow_colour)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def messageslb(self, ctx, l=30):
        a = await self.bot.db.fetch(
            """
            SELECT user_id
            FROM chat.messagecount
             WHERE guild_id = $1
            """,
            ctx.guild.id
        )
        print("first")
        leaderboard = {}
        total = []
        for i in a:
            b = str(i).replace("<", "").replace(">", "").replace("=", " ").replace("Record", "").replace("user_id", "")
            name = int(b)
            x = await self.bot.db.fetchval(
                """
                SELECT message
                FROM chat.messagecount
                 WHERE user_id = $1 AND guild_id = $2
                """,
                int(b), ctx.guild.id
            )
            leaderboard[name] = x

        em = discord.Embed(title=f'Top 10 active members in {ctx.guild.name}', colour=self.bot.violet_color)
        sorted_words = sorted(leaderboard.items(), key=lambda item: int(item[1]), reverse=True)
        index = 1
        for key, val in sorted_words:
            id_ = key
            member = self.bot.get_user(id_)
            em.add_field(name=f'``{index}:`` {member}', value=f' **messages sent :** ``{val}``', inline=False)
            em.set_footer(text=f"{self.bot.user.name} : information requested by {ctx.author.display_name}",
                          icon_url=self.bot.user.avatar.url)

            if index == l:
                break
            else:
                index += 1
        await ctx.send(embed=em)


    @commands.command()
    async def invites(self, ctx, user: discord.Member = None):
        if user == None:
            totalInvites = 0
            for i in await ctx.guild.invites():
                if i.inviter == ctx.author:
                    totalInvites += i.uses
            embed = discord.Embed(title=ctx.author,
                                  description=f"You've invited ``{totalInvites}`` member{'' if totalInvites == 1 else 's'} to the server!",
                                  colour=discord.Colour.red())
            embed.set_footer(text=f"{self.bot.user} : Information requested by {ctx.author}",
                             icon_url=self.bot.user.avatar.url)
            await ctx.author.send(embed=embed)
        else:
            totalInvites = 0
            for i in await ctx.guild.invites():

                if i.inviter == user:
                    totalInvites += i.uses
            embed2 = discord.Embed(title=user,
                                   description=f"{user} invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!")
            embed2.set_footer(text=f"{self.bot.user} : Infromation requested by {user}",
                              icon_url=self.bot.user.avatar.url)
            await ctx.author.send(embed=embed2)

    # slash command
    @app_commands.command(name="messages_leaderboard", description="show leaderboard by messages sent by user")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    async def messageslbslash(self, interaction:discord.Interaction):
        l = 10
        a = await self.bot.db.fetch(
            """
            SELECT user_id
            FROM chat.messagecount
             WHERE guild_id = $1
            """,
            interaction.guild.id
        )
        print("first")
        leaderboard = {}

        for i in a:
            b = str(i).replace("<", "").replace(">", "").replace("=", " ").replace("Record", "").replace("user_id", "")
            name = int(b)
            x = await self.bot.db.fetchval(
                """
                SELECT message
                FROM chat.messagecount
                 WHERE user_id = $1 AND guild_id = $2
                """,
                int(b), interaction.guild.id
            )
            leaderboard[name] = x

        print("second")

        em = discord.Embed(title=f'Top 10 active members in {interaction.user.guild.name}', colour=self.bot.violet_color)
        sorted_words = sorted(leaderboard.items(), key=lambda item: int(item[1]), reverse=True)
        index = 1
        for key, val in sorted_words:
            id_ = key
            member = self.bot.get_user(id_)
            em.add_field(name=f'``{index}:`` {member}', value=f' **messages sent :** ``{val}``', inline=False)
            em.set_footer(text=f"{self.bot.user.name} : information requested by {interaction.user.display_name}",
                          icon_url=self.bot.user.avatar.url)
            if index == l:
                break
            else:
                index += 1
        await interaction.response.send_message(embed=em)



    """@messageslbslash.error
    async def messageslb_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(error, ephemeral=True)
        else:
            await interaction.response.send_message("something went wrong", ephemeral=True)"""


    @app_commands.command(name="messages", description="Display amount of messages sent by a user or yourself")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(member="User")
    async def msg2(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is not None:
            user = member
            a = await self.bot.db.fetchval(
                """
                SELECT message
                FROM chat.messagecount
                 WHERE user_id = $1 AND guild_id= $2
                """,
                user.id, user.guild.id
            )
            if a is None:
                a = 0
            embed = discord.Embed(title='you sent {} messages since i joined the server'.format(a),
                                  color=self.bot.violet_color)
            embed.set_author(name=member, icon_url=member.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            a = await self.bot.db.fetchval(
                """
                SELECT message
                FROM chat.messagecount
                 WHERE user_id = $1 AND guild_id= $2
                """,
                interaction.user.id, interaction.user.guild.id
            )
            if a is None:
                a = 0
            embed = discord.Embed(title='you sent {} messages since i joined the server'.format(a),
                                  color=self.bot.green_colour)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    """@msg2.error
    async def message2_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(error, ephemeral=True)
        elif isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("member name is not in the list", ephemeral=True)
        else:
            await interaction.response.send_message("something went wrong", ephemeral=True)"""

    @app_commands.command(name="invites", description="display the total invi")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(user="Member")
    async def invitesslash(self, interaction: discord.Interaction, user: discord.Member = None):
        if user == None:
            totalInvites = 0
            for i in await interaction.guild.invites():
                if i.inviter == interaction.user:
                    totalInvites += i.uses
            embed = discord.Embed(
                description=f"You've invited ``{totalInvites}`` member{'' if totalInvites == 1 else 's'} to the server!",
                colour=discord.Colour.red(), )
            embed.set_footer(text=f"{self.bot.user} : Infromation requested by {interaction.user}",
                             icon_url=self.bot.user.avatar.url)
            embed.set_author(icon_url=interaction.user.avatar.url, name=interaction.user)

            await interaction.response.send_message(embed=embed)

        else:
            totalInvites = 0
            for i in await user.guild.invites():

                if i.inviter == user:
                    totalInvites += i.uses
            embed2 = discord.Embed(
                description=f"{user} invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!")
            embed2.set_footer(text=f"{self.bot.user} : Information requested by {interaction.user}",
                              icon_url=self.bot.user.avatar.url)
            embed2.set_author(icon_url=user.avatar.url, name=user)
            await interaction.response.send_message(embed=embed2)

    @invitesslash.error
    async def inviteslashe_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(error, ephemeral=True)
        else:
            await interaction.response.send_message("something went wrong", ephemeral=True)
            raise error


async def setup(bot: SussyBot) -> None:
    await bot.add_cog(
        messagess(bot))
