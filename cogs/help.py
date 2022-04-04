import asyncio

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

        await ctx.message.add_reaction("❔")
        await ctx.send(embed=em)

#===================================mod==help==command============================================================================
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
                                                                   "**``$unban <user> ``**"
                                                                   "\n"
                                                                   "unban a banned user in the guild"
                                                                   "\n"
                                                                   "\n"
                                                                   "**``$mute <user> <reason optional>``**"
                                                                   "\n"
                                                                   "mute a random user from the guild"
                                                                   "\n")
        await ctx.send(embed=em)


#==========================================================================================================================


    @help.command()
    async def general(self,ctx):
        embed = discord.Embed(title="general command plugins",description="**``$whois <user optional>``**"
                                                                          "\n"
                                                                          "get user infromation"
                                                                          "\n"
                                                                          "\n"
                                                                          "**``$avatar <user optional>``**"
                                                                          "\n"
                                                                          "get a user avatar "
                                                                          "\n"
                                                                          "\n"
                                                                          "**``$ping ``**"
                                                                          "\n"
                                                                          "get client ping "
                                                                          "\n"
                                                                          "\n"
                                                                          "**``$list``**"
                                                                          "\n"
                                                                          "get list of all commands"
                                                                          "\n"
                                                                          "\n"
                                                                          "**``$status``**"
                                                                          "\n"
                                                                          "get bot basic info"
                                                                          "\n"
                                                                          "\n"
                                                                          "**``$dm``**"
                                                                          "\n"
                                                                          "dm a member by the bot"
                                                                          )
        await ctx.send(embed=embed)

    @help.command()
    async def fun(self, ctx):

        embed = discord.Embed(title="fun command plugins", description="**``$trigger <user optional>``**"
                                                                           "\n"
                                                                           "trigger a user"
                                                                           "\n"
                                                                           "\n"
                                                                           "**``$gay <user optional>``**"
                                                                           "\n"
                                                                           "show your gay pride"
                                                                           "\n"
                                                                           "\n"
                                                                           "**``$wasted <user optional>``**"
                                                                           "\n"
                                                                           "make a user wasted "
                                                                           "\n"
                                                                           "\n"
                                                                           "**``$jail <user optional>``**"
                                                                           "\n"
                                                                           "put a user in the jail"
                                                                           "\n"
                                                                           "\n"
                                                                           "**``$comrade <user optional>``**"
                                                                           "\n"
                                                                           "make a user comrade"
                                                                           "\n"
                                                                           "\n"



                                                                           )
        embed2= discord.Embed(title="page 2",description="**``$glass <user optional>``**"
                                                                       "\n"
                                                                       "put a user under the glass"
                                                                       "\n"
                                                                       "\n"
                                                                       "**``$joke``**"
                                                                       "\n"
                                                                       "make a joke "
                                                                       "\n"
                                                                       "\n"
                                                                       "**``$minecraft <minecraft username>``**"
                                                                       "\n"
                                                                       "get a mincraft user uuid "
                                                                       "\n"
                                                                       "\n"
                                                                       "**``$colour <hex code>``**"
                                                                       "\n"
                                                                       "get a colour by hex code"
                                                                       "\n"
                                                                       "\n"
                                                                       "**``$image <search optional>``**"
                                                                       "\n"
                                                                       "get a image from unsplash "
                                                                       )
        embed3 =discord.Embed(title="page 3",description="**``$gif <search optional>``**"
                                                                       "\n"
                                                                       "get a random gif from Tenor"
                                                                       "\n"
                                                                       "\n"
                                                                       "**``$animals``**"
                                                                       "\n"
                                                                       "get a random animal image"
                                                                       "\n"
                                                                       "\n"
                                                                       "**``$cat``**"
                                                                       "\n"
                                                                       "get a random cat image "
                                                                       "\n"
                                                                       "\n"
                                                                       "**``$dog``** "
                                                                       "\n"
                                                                       "get a random dog image"
                                                                       "\n"
                                                                       "\n"
                                                                       "**``$animalfacts``**"
                                                                       "\n"
                                                                       "get a random animal fact with image"
                                                                       "\n")
        embed4 = discord.Embed(title="page 4",description="**``$memes``**"
                                                                       "\n"
                                                                       "get a random memes from reddit r/memes"
                                                                       "\n"
                                                                       "\n"
                                                                       "**``$meirl``**"
                                                                       "\n"
                                                                       "get a random memes from r/me_irl")
        contents = [embed, embed2,embed3,embed4]
        pages = 4
        cur_page = 1
        message = await ctx.send(embed=contents[cur_page - 1])
        # getting the message object for editing and reacting

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed=contents[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=contents[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break


    @commands.command()
    async def hello(self,ctx):
        msg = await ctx.send('Send me that 👍 reaction, mate')
        self._previous_message = msg
        await msg.add_reaction("👍")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check,)
        except asyncio.TimeoutError:
            await ctx.send('👎')
        else:
            await self._previous_message.edit(content="Edited the message",)
        '''message = await ctx.send("I'll edit this message when you type `$next`")
        self._previous_message = message
        await message.add_reaction("❔")
        if discord.user == ctx.message.author and str(self.reaction.emoji) == '✅':
            await self._previous_message.edit(content="Edited the message",)'''

    @commands.command()
    async def pages(self,ctx):
        embed1 = discord.Embed(title=" page 1 yes")
        embed2 = discord.Embed(title="page 2 no")
        embed3 = discord.Embed(title="page 3")
        contents = [embed1,embed2,embed3]
        pages = 3
        cur_page = 1
        message = await ctx.send(embed = contents[cur_page - 1])
        # getting the message object for editing and reacting

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed=contents[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=contents[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break





def setup(client):
    client.add_cog(help(client))