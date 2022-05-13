import logging
import os
import discord
import aiohttp
import random
from requests import get
from discord.ext import commands
from discord import app_commands
from discord.ui import Button , View
from discord.ext.commands import cooldown , BucketType
from discord.app_commands import Choice
from bot import SussyBot

class randomapi(commands.Cog):
    def __init__(self, bot: SussyBot) -> None:
        self.bot = bot

    """all random apis here"""

    #give a random animal fact with image
    @commands.command()
    async def animalfacts(self, ctx):
        async with aiohttp.ClientSession() as session:
            link = ["https://some-random-api.ml/animal/dog", "https://some-random-api.ml/animal/cat",
                    "https://some-random-api.ml/animal/fox",
                    "https://some-random-api.ml/animal/birb", "https://some-random-api.ml/animal/koala",
                    "https://some-random-api.ml/animal/kangaroo", "https://some-random-api.ml/animal/raccoon",
                    "https://some-random-api.ml/animal/panda", "https://some-random-api.ml/animal/red_panda", ]
            list = random.choice(link)
            async with session.get(list) as response:
                data = await response.json()
                embed2 = discord.Embed(title="", description=data["fact"],
                                       colour=discord.Colour.random())
                embed2.set_image(url=data["image"])
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed2)
                await ctx.message.clear_reaction("✅")



    #give a random animal image
    @app_commands.command(name="animals", description="get a random animal photo")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    async def animalslash(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            link = ["https://some-random-api.ml/img/dog", "https://some-random-api.ml/img/cat",
                        "https://some-random-api.ml/img/fox",
                        "https://some-random-api.ml/img/birb", "https://some-random-api.ml/img/koala",
                        "https://some-random-api.ml/img/panda", "https://some-random-api.ml/img/red_panda", ]
            list = random.choice(link)
            async with session.get(list) as response:
                data = await response.json()
                embed3 = discord.Embed(title="", description="", colour=discord.Colour.random())
                embed3.set_image(url=data["link"])

                #hello

                button2 = Button(label="cancle",style=discord.ButtonStyle.red,)
                async def button2_callback(interaction):

                    await interaction.response.edit_message(view=view.clear_items())


                button = Button(label="Next image", style=discord.ButtonStyle.primary)
                view = View()

                async def button_callback(interaction):
                    async with aiohttp.ClientSession() as session:
                        link2 = ["https://some-random-api.ml/img/dog", "https://some-random-api.ml/img/cat",
                                "https://some-random-api.ml/img/fox",
                                "https://some-random-api.ml/img/birb", "https://some-random-api.ml/img/koala",
                                "https://some-random-api.ml/img/panda", "https://some-random-api.ml/img/red_panda", ]
                        list2 = random.choice(link)
                        async with session.get(list2) as response:
                            data = await response.json()
                            embed4 = discord.Embed(title="", description="", colour=discord.Colour.random())
                            embed4.set_image(url=data["link"])
                    await interaction.response.edit_message(embed=embed4, view=view)

                button.callback = button_callback
                button2.callback = button2_callback
                view.add_item(button)
                view.add_item(button2)


                await interaction.response.send_message(embed=embed3, view=view)


    #animals slash error handler
    @animalslash.error
    async def animalslash_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error ,  app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"{error}",ephemeral=True)
        else:
            await interaction.response.send_message("**something went wrong do ``$help`` for help**",ephemeral=True)


    #animal prefix command
    @commands.command()
    @commands.cooldown(1 , 5 , BucketType.user)
    async def animals(self, ctx):
        async with aiohttp.ClientSession() as session:
            link = ["https://some-random-api.ml/img/dog", "https://some-random-api.ml/img/cat",
                    "https://some-random-api.ml/img/fox",
                    "https://some-random-api.ml/img/birb", "https://some-random-api.ml/img/koala",
                    "https://some-random-api.ml/img/panda", "https://some-random-api.ml/img/red_panda", ]
            list = random.choice(link)
            async with session.get(list) as response:
                data = await response.json()
                embed3 = discord.Embed(title="", description="", colour=discord.Colour.random())
                embed3.set_image(url=data["link"])
                async with session.get(list) as response:
                    data = await response.json()
                    embed3 = discord.Embed(title="", description="", colour=discord.Colour.random())
                    embed3.set_image(url=data["link"])

                    # hello

                    button2 = Button(label="cancle", style=discord.ButtonStyle.red, )

                    async def button2_callback(interaction):
                        await interaction.response.edit_message(view=view.clear_items())

                    button = Button(label="Next image", style=discord.ButtonStyle.primary)
                    view = View()

                    async def button_callback(interaction):
                        async with aiohttp.ClientSession() as session:
                            link = ["https://some-random-api.ml/img/dog", "https://some-random-api.ml/img/cat",
                                    "https://some-random-api.ml/img/fox",
                                    "https://some-random-api.ml/img/birb", "https://some-random-api.ml/img/koala",
                                    "https://some-random-api.ml/img/panda",
                                    "https://some-random-api.ml/img/red_panda", ]
                            list = random.choice(link)
                            async with session.get(list) as response:
                                data = await response.json()
                                embed3 = discord.Embed(title="", description="", colour=discord.Colour.random())
                                embed3.set_image(url=data["link"])
                                async with session.get(list) as response:
                                    data = await response.json()
                                    embed3 = discord.Embed(title="", description="", colour=discord.Colour.random())
                                    embed3.set_image(url=data["link"])
                        await interaction.response.edit_message(embed=embed3, view=view)

                    button.callback = button_callback
                    button2.callback = button2_callback
                    view.add_item(button)
                    view.add_item(button2)
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed3 ,  view = view)
                await ctx.message.clear_reaction("✅")







    #give a random dog image slash command
    @app_commands.command(name="dog", description="get a random dog photo")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    async def dogslash(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            link = "https://some-random-api.ml/img/dog"
            async with session.get(link) as response:
                data = await response.json()
                embed3 = discord.Embed(title="", description="", colour=discord.Colour.random())
                embed3.set_image(url=data["link"])

                button2 = Button(label="cancle", style=discord.ButtonStyle.red, )

                async def button2_callback(interaction):
                    await interaction.response.edit_message(view=view.clear_items())

                button = Button(label="Next image", style=discord.ButtonStyle.primary)
                view = View()

                async def button_callback(interaction):
                    async with aiohttp.ClientSession() as session:
                        link = "https://some-random-api.ml/img/dog"
                        async with session.get(link) as response:
                            data = await response.json()
                            embed4 = discord.Embed(title="", description="", colour=discord.Colour.random())
                            embed4.set_image(url=data["link"])
                    await interaction.response.edit_message(embed=embed4, view=view)

                button.callback = button_callback
                button2.callback = button2_callback
                view.add_item(button)
                view.add_item(button2)
                await interaction.response.send_message(embed=embed3 , view = view)


    @dogslash.error
    async def dogslash_error(self , interaction: discord.Interaction , error : app_commands.AppCommandError):
        if isinstance(error , app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"{error}",ephemeral=True)
        else:
            await interaction.response.send_message("APi is down try again after few moments",ephemeral=True)



    @commands.command()
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as session:
            link = "https://some-random-api.ml/img/dog"
            async with session.get(link) as response:
                data = await response.json()
                embed3 = discord.Embed(title="", description="", colour=discord.Colour.random())
                embed3.set_image(url=data["link"])
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed3)
                await ctx.message.clear_reaction("✅")






#give a random cat image
    @app_commands.command(name="cat", description="do you love cats :cat:?")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    async def catslash(self, interaction : discord.Interaction):
        async with aiohttp.ClientSession() as session:
            link = "https://some-random-api.ml/img/cat"
            async with session.get(link) as response:
                data = await response.json()
                embed3 = discord.Embed(title="", description="", colour=discord.Colour.random())
                embed3.set_image(url=data["link"])
                button2 = Button(label="cancle", style=discord.ButtonStyle.red, )

                async def button2_callback(interaction):
                    await interaction.response.edit_message(view=view.clear_items())

                button = Button(label="Next image", style=discord.ButtonStyle.primary)
                view = View()

                async def button_callback(interaction):
                    async with aiohttp.ClientSession() as session:
                        link = "https://some-random-api.ml/img/cat"
                        async with session.get(link) as response:
                            data = await response.json()
                            embed4 = discord.Embed(title="", description="", colour=discord.Colour.random())
                            embed4.set_image(url=data["link"])
                    await interaction.response.edit_message(embed=embed4, view=view)

                button.callback = button_callback
                button2.callback = button2_callback
                view.add_item(button)
                view.add_item(button2)

                await interaction.response.send_message(embed=embed3, view = view)


    @catslash.error
    async def catslash_error(self, interaction : discord.Interaction , error : app_commands.AppCommandError):
        if isinstance(error , app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"{error}",ephemeral=True)
        elif isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("seomthing went wrong or api is down| pls try again letter or report by doing $bugs <reason>",ephemeral=True)
        else:
            await interaction.response.send_message("something went wrong do ``$help`` or report the bug by doing ``$bug``",ephemeral=True)



    @commands.command()
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            link = "https://some-random-api.ml/img/cat"
            async with session.get(link) as response:
                data = await response.json()
                embed3 = discord.Embed(title="", description="", colour=discord.Colour.random())
                embed3.set_image(url=data["link"])
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed3)
                await ctx.message.clear_reaction("✅")




#random api ml fun command ========================================================================
        """messageCount[author] = 1
        with open('messages.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
            json.dump(messageCount, f, indent=4)"""
#joke command
    @commands.command()
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as session:
            link = "https://some-random-api.ml/joke"
            async with session.get(link) as response:
                data = await response.json()
                joke = data["joke"]
                embed3 = discord.Embed(title="", description=f"**{joke}**", colour=discord.Colour.random())
                await ctx.send("amongus ")
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed3)
                await ctx.message.clear_reaction("✅")

    @app_commands.command(name="joke",description="lol laugh at this user")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    async def joke_slash(self, intreaction : discord.Interaction):
        async with aiohttp.ClientSession() as session:
            link = "https://some-random-api.ml/joke"
            async with session.get(link) as response:
                data = await response.json()
                joke = data["joke"]
                embed3 = discord.Embed(title="", description=f"**{joke}**", colour=discord.Colour.random())
                button2 = Button(label="cancle", style=discord.ButtonStyle.red, )

                async def button2_callback(interaction):
                    await interaction.response.edit_message(view=view.clear_items())

                button = Button(label="Next joke", style=discord.ButtonStyle.primary)
                view = View()

                async def button_callback(interaction):
                    async with aiohttp.ClientSession() as session:
                        link = "https://some-random-api.ml/joke"
                        async with session.get(link) as response:
                            data = await response.json()
                            joke = data["joke"]
                            embed4 = discord.Embed(title="", description=f"**{joke}**", colour=discord.Colour.random())
                    await interaction.response.edit_message(embed=embed4, view=view)

                button.callback = button_callback
                button2.callback = button2_callback
                view.add_item(button)
                view.add_item(button2)

                await intreaction.response.send_message(embed = embed3 ,  view = view)


    @joke_slash.error
    async def joke_slash_error(self, interaction : discord.Interaction , error: app_commands.AppCommandError):
        if isinstance(error , app_commands.CommandOnCooldown):
            await interaction.response.send_message(error,ephemeral=True)
        else:
            await interaction.response.send_message("something went wrong",ephemeral=True)


    @app_commands.command(name="youtube",description="get a youtube video thumbnail")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(url="url of the video",type = "the size of thumbnail")
    @app_commands.choices(type = [
        Choice(name="max",value="maxresdefault.jpg"),
        Choice(name="small",value="default.jpg"),
        Choice(name="medium",value="mqdefault.jpg"),

    ])

    async def ytgrab(self,interaction: discord.Interaction,url: str,type:str):
        search_url = str(url.rsplit("=",1)[1])
        orl = f"https://img.youtube.com/vi/{search_url}/{type}"
        await interaction.response.send_message(orl)


    @ytgrab.error
    async def ytgrab_error(self,interaction : discord.Interaction, error : app_commands.AppCommandError):
        if isinstance(error , app_commands.CommandOnCooldown):
            await interaction.response.send_message(error,ephemeral=True)
        else:
            await interaction.response.send_message("invaild url or something went wrong",ephemeral=True)


    @app_commands.command(name="minecraft",description="get mincraft username uuid ")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(username="minecraft profile username")
    async def minecraft_slash(self, interaction :discord.Interaction,username:str):
        search_url = f"https://some-random-api.ml/mc?username={username}"

        async with aiohttp.ClientSession() as cs:
            async with cs.get(search_url) as r:
                res = await r.json()
                ign = res["username"]
                names = res["name_history"][0]["name"]
                uuid = res['uuid']
                embed4 = discord.Embed(title=f"{ign}", description="")
                embed4.add_field(name="uuid", value=f"{uuid}")
                embed4.add_field(name="first usernames", value=f"{names}")


                await interaction.response.send_message(embed=embed4)

    @minecraft_slash.error
    async def minecraft_slash_error(self, interaction : discord.Interaction , error : app_commands.AppCommandError):
        if isinstance(error , app_commands.CommandOnCooldown):
            await interaction.response.send_message(error,ephemeral=True)
        else:
            await interaction.response.send_message("something went wrong try again",ephemeral=True)


    #minecraft command
    @commands.command(pass_context=True)
    async def minecraft(self, ctx, *, username=None):
        search_url = None
        if username != None:
            search_url = f"https://some-random-api.ml/mc?username={username}"
        else:
            await ctx.send("**fucking give me a vaild name**",delete_after=5)
            return
        async with aiohttp.ClientSession() as cs:
            async with cs.get(search_url) as r:
                res = await r.json()
                ign = res["username"]
                names = res["name_history"][0]["name"]
                uuid = res['uuid']
                embed4 = discord.Embed(title=f"{ign}", description="")
                embed4.add_field(name="uuid",value=f"{uuid}")
                embed4.add_field(name="first usernames",value=f"{names}")

                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed4)
                await ctx.message.clear_reaction("✅")






#trigger command
    @app_commands.command(name="trigger", description="trigger a user")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(member= "username")
    async def triggerslash(self, interaction: discord.Interaction, member: discord.Member=None):
        if member != None:
            search_url = f"https://some-random-api.ml/canvas/triggered?avatar={member.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")

            if resp.status_code == 200:
                open(r'data/trigger.gif', 'wb').write(resp.content)
                d = open(r"data/trigger.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'
                logging.warning(file_to_send)


                await interaction.response.send_message(file=discord.File(r"../data\\trigger.gif"))


            elif resp.status_code != 200:
                await interaction.response.send_message("api is down", ephemeral=True)
        else:
            search_url = f"https://some-random-api.ml/canvas/triggered?avatar={interaction.user.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")

            if resp.status_code == 200:
                open(r'data/trigger.gif', 'wb').write(resp.content)
                d = open(r"data/trigger.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'
                logging.warning(file_to_send)


                await interaction.response.send_message(file=discord.File(r"data/trigger.gif"))


            elif resp.status_code != 200:
                await interaction.response.send_message("api is down" , ephemeral=True)
    @triggerslash.error
    async def triggerslash_error(self, ineraction : discord.Interaction , error: app_commands.AppCommandError):
        if isinstance(error , app_commands.CommandOnCooldown):
            await ineraction.response.send_message(error,ephemeral=True)
        else:
            await ineraction.response.send_message("something went wrong",ephemeral=True)

    @commands.command(description="get a user triggerd")
    async def trigger(self, ctx, member: discord.Member = None):

        if member != None:
            logging.warning(member.avatar.url)
            search_url = f"https://some-random-api.ml/canvas/triggered?avatar={member.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")

            if resp.status_code == 200:
                open(r'data/trigger.gif', 'wb').write(resp.content)
                d = open(r"data/trigger.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'
                logging.warning(file_to_send)

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File(r"data/trigger.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                ctx.send("api is down")
        else:
            search_url = f"https://some-random-api.ml/canvas/triggered?avatar={ctx.message.author.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")

            if resp.status_code == 200:
                open(r'data/trigger.gif', 'wb').write(resp.content)
                d = open(r"data/trigger.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'
                logging.warning(file_to_send)

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File(r"data/trigger.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                ctx.send("api id down")




#jai api
    @app_commands.command(name="jail", description="put a user in the jail")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(member="username")
    async def jail_slash(self, interaction: discord.Interaction , member: discord.Member = None):
        if member != None:
            search_url = f"https://some-random-api.ml/canvas/jail?avatar={member.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")

            if resp.status_code == 200:
                open(r'data/jail.gif', 'wb').write(resp.content)
                d = open(r"data/jail.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'
                logging.warning(file_to_send)


                await interaction.response.send_message(file=discord.File(r"data/jail.gif"))


            elif resp.status_code != 200:
                await interaction.response.send_message("api is down",ephemeral=True)
        else:
            search_url = f"https://some-random-api.ml/canvas/jail?avatar={interaction.user.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")

            if resp.status_code == 200:
                open(r'data/jail.gif', 'wb').write(resp.content)
                d = open(r"../data\\jail.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'
                logging.warning(file_to_send)



                await interaction.response.send_message(file=discord.File(r"data/jail.gif"))


            elif resp.status_code != 200:
                await interaction.response.send_message("api is down",ephemeral=True)

    @jail_slash.error
    async def jail_slash_error(self, interaction : discord.Interaction , error : app_commands.AppCommandError):
        if isinstance(error , app_commands.CommandOnCooldown):
            await interaction.response.send_message(error,ephemeral=True)
        else:
            await interaction.response.send_message("something went wrong",ephemeral=True)



    @commands.command(description="get a user in the jail")
    async def jail(self, ctx, member: discord.Member = None):

        if member != None:
            search_url = f"https://some-random-api.ml/canvas/jail?avatar={member.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")

            if resp.status_code == 200:
                open(r'data/jail.gif', 'wb').write(resp.content)
                d = open(r"data/jail.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'
                logging.warning(file_to_send)

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File(r"data/jail.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                ctx.send("api is down")
        else:
            search_url = f"https://some-random-api.ml/canvas/jail?avatar={ctx.message.author.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")

            if resp.status_code == 200:
                open(r'data/jail.gif', 'wb').write(resp.content)
                d = open(r"data/jail.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'
                logging.warning(file_to_send)

                await ctx.message.add_reaction("✅")

                await ctx.send(file=discord.File(r"data/jail.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                ctx.send("api is down")

    @app_commands.command(name="gay", description="show your gay pride")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(member="username")
    async def gay_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        if member != None:
            search_url = f"https://some-random-api.ml/canvas/gay?avatar={member.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")

            if resp.status_code == 200:
                open(r'data/gay.gif', 'wb').write(resp.content)
                d = open(r"data/gay.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await interaction.response.send_message(file=discord.File(r"data/gay.gif"))

            elif resp.status_code != 200:
                await interaction.response.send_message("api is down",ephemeral=True)
        else:
            search_url = f"https://some-random-api.ml/canvas/gay?avatar={interaction.user.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")

            if resp.status_code == 200:
                open(r'data/gay.gif', 'wb').write(resp.content)
                d = open(r"data/gay.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await interaction.response.send_message(file=discord.File(r"data/gay.gif"))
            elif resp.status_code != 200:
                interaction.response.send_message("api is down",ephemeral=True)

    @gay_slash.error
    async def gay_slash_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(error,ephemeral=True)
        else:
            await interaction.response.send_message("something went wrong",ephemeral=True)

    #gay command
    @commands.command(description="show your gay pride")
    async def gay(self, ctx, member: discord.Member = None):
        if member != None:
            search_url = f"https://some-random-api.ml/canvas/gay?avatar={member.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")

            if resp.status_code == 200:
                open(r'data/gay.gif', 'wb').write(resp.content)
                d = open(r"data/gay.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File(r"data/gay.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                await ctx.send("api is down")
        else:
            search_url = f"https://some-random-api.ml/canvas/gay?avatar={ctx.message.author.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")

            if resp.status_code == 200:
                open(r'data/gay.gif', 'wb').write(resp.content)
                d = open(r"data/gay.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File(r"data/gay.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                await ctx.send("api is down")




#glass command put someone in glass
    @app_commands.command(name="glass", description="put a user in glass")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(member="username")
    async def glass_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        if member != None:
            search_url = f"https://some-random-api.ml/canvas/glass?avatar={member.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")
            if resp.status_code == 200:
                open(r'data/glass.gif', 'wb').write(resp.content)
                d = open(r"data/glass.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await interaction.response.send_message(file=discord.File(r"data/glass.gif"))

            elif resp.status_code != 200:
                await interaction.response.send_message("api is down",ephemeral=True)
        else:
            search_url = f"https://some-random-api.ml/canvas/glass?avatar={interaction.user.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")
            if resp.status_code == 200:
                open(r'data/glass.gif', 'wb').write(resp.content)
                d = open(r"data/glass.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await interaction.response.send_message(file=discord.File(r"data/glass.gif"))
            elif resp.status_code != 200:
                await interaction.response.send_messgae("api is down",ephemeral=True)

    """@glass_slash.error
    async def glass_slash_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(error,ephemeral=True)
        else:
            await interaction.response.send_message("something went wrong",ephemeral=True)"""



    @commands.command(description="get a user in glass")
    async def glass(self, ctx, member: discord.Member = None):
        if member != None:
            search_url = f"https://some-random-api.ml/canvas/glass?avatar={member.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")
            if resp.status_code == 200:
                open(r'data/glass.gif', 'wb').write(resp.content)
                d = open(r"data/glass.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File(r"data/glass.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                ctx.send("api is down")
        else:
            search_url = f"https://some-random-api.ml/canvas/glass?avatar={ctx.message.author.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")
            if resp.status_code == 200:
                open(r'data/glass.gif', 'wb').write(resp.content)
                d = open(r"data/glass.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File(r"data/glass.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                ctx.send("api is down")

#make someone wasted
    @app_commands.command(name="wasted", description="make a user wasted")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(member="username")
    async def wasted_slash(self,interaction: discord.Interaction, member: discord.Member = None):
        if member != None:
            search_url = f"https://some-random-api.ml/canvas/wasted?avatar={member.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")
            if resp.status_code == 200:
                open(r'data/wasted.gif', 'wb').write(resp.content)
                d = open(r"../data\\wasted.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'


                await interaction.response.send_message(file=discord.File(r"data/wasted.gif"))
            elif resp.status_code != 200:
                await interaction.response.send_message("api is down",ephemeral=True)

        else:
            search_url = f"https://some-random-api.ml/canvas/wasted?avatar={interaction.user.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")
            if resp.status_code == 200:
                open(r'data/wasted.gif', 'wb').write(resp.content)
                d = open(r"data/wasted.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await interaction.response.send_message(file=discord.File(r"data/wasted.gif"))

            elif resp.status_code != 200:
                await interaction.response.send_message("api is down", ephemeral=True)

    @wasted_slash.error
    async def wasted_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(error, ephemeral=True)
        else:
            await interaction.response.send_message("something went wrong", ephemeral=True)

    @commands.command(description="get a user wasted")
    async def wasted(self, ctx, member: discord.Member = None):
        if member != None:
            search_url = f"https://some-random-api.ml/canvas/wasted?avatar={member.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")
            if resp.status_code == 200:
                open(r'data/wasted.gif', 'wb').write(resp.content)
                d = open(r"data/wasted.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File(r"data/wasted.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                ctx.send("api is down")

        else:
            search_url = f"https://some-random-api.ml/canvas/wasted?avatar={ctx.message.author.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")
            if resp.status_code == 200:
                open(r'data/wasted.gif', 'wb').write(resp.content)
                d = open(r"data/wasted.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File(r"data/wasted.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                await ctx.send("api is down")



#make somone comrade
    @app_commands.command(name="comrade", description="make a user comrade")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(member="username")
    async def comrade_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        if member != None:
            search_url = f"https://some-random-api.ml/canvas/comrade?avatar={member.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")
            if resp.status_code == 200:
                open(r'data/comrade.gif', 'wb').write(resp.content)
                d = open(r"data/comrade.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'


                await interaction.response.send_message(file=discord.File(r"data/comrade.gif"))


            elif resp.status_code != 200:
                await interaction.response.send_message("api is down",ephemeral=True)
        else:
            search_url = f"https://some-random-api.ml/canvas/comrade?avatar={interaction.user.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")
            if resp.status_code == 200:
                open(r'data/comrade.gif', 'wb').write(resp.content)
                d = open(r"data/comrade.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'


                await interaction.response.send_message(file=discord.File(r"data/comrade.gif"))



            elif resp.status_code != 200:
                await interaction.response.send_message("api is down",ephemeral=True)

    @comrade_slash.error
    async def comrade_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(error, ephemeral=True)
        else:
            await interaction.response.send_message("something went wrong", ephemeral=True)

    @commands.command(description="get a user comrade")
    async def comrade(self, ctx, member: discord.Member = None):
        if member is None:
            search_url = f"https://some-random-api.ml/canvas/comrade?avatar={ctx.message.author.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")
            print()
            if resp.status_code == 200:
                open(r'data/comrade.gif', 'wb').write(resp.content)
                d = open(r"data/comrade.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File(r"data/comrade.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                ctx.send("api is down")
        else:
            search_url = f"https://some-random-api.ml/canvas/comrade?avatar={member.avatar.url}"
            slice_object = slice(-10)
            resp = get(f"{search_url[slice_object]}")
            if resp.status_code == 200:
                open(r'data/comrade.gif', 'wb').write(resp.content)
                d = open(r"data/comrade.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File(r"data/comrade.gif"))
                await ctx.message.clear_reaction("✅")


            elif resp.status_code != 200:
                ctx.send("api is down")


#get a color by hex code
    @app_commands.command(name="colour",description="get a colour by hex code")
    @app_commands.checks.cooldown(1 , 5 , key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(hex= "hex code only 6 latters")
    async def colourslash(self, interaction : discord.Interaction ,hex: str = None):
        if len(hex) > 6 or hex == None :
            await interaction.response.send_message("hex code only contain 6 latters with numbers")
        else:
            search_url = f"https://some-random-api.ml/canvas/colorviewer?hex={hex}"
            em = discord.Embed(title=hex, description="")
            em.set_image(url=search_url)
            await interaction.response.send_message(embed = em)

    @colourslash.error
    async def colourslash_error(self, ineraction : discord.Interaction , error : app_commands.AppCommandError):
        if isinstance(error , app_commands.CommandOnCooldown):
            await ineraction.response.send_message(f"{error}", ephemeral=True)
        else:
            await ineraction.response.send_message("API is down try again in some moments",ephemeral=True)


    @commands.command(description="get a user comrade")
    async def colour(self, ctx, hex=None):
        search_url = None
        if hex != None:
            search_url = f"https://some-random-api.ml/canvas/colorviewer?hex={hex}"
            em = discord.Embed(title=hex, description="")
            em.set_image(url=search_url)
            await ctx.send(embed=em)
        else:
            await ctx.send("**fucking give me a colour code**")
            return

    @app_commands.command(name="wikipedia", description="search about anything on wikipedia ")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(search="Search")
    async def wikislash(self, interaction: discord.Interaction, search: str):
        try:
            search_url = None
            if search != None:
                search = search.replace(' ', '_')
                logging.warning(search)

                search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={search}&limit=1"
                logging.warning(search_url)
            else:
                await interaction.response.send_message("``your mom``",ephemeral=True)

            async with aiohttp.ClientSession() as cs:
                async with cs.get(search_url) as r:
                    res = await r.json()
                    logging.warning(res[3][0])
                    await interaction.response.send_message(res[3][0])

        except IndexError:
            await interaction.response.send_message(f"``there is no page called {search}``",ephemeral=True)


    @wikislash.error
    async def wikislash_error(self , interaction : discord.Interaction , error : app_commands.AppCommandError):
        if isinstance(error , app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"{error}")
        else:
            await interaction.response.send_message("something went wrong",ephemeral=True)

    @commands.command(description="get a user comrade")
    async def wiki(self, ctx, *,search=None):
        try:
            search_url = None
            if search != None:
                search = search.replace(' ', '_')
                logging.warning(search)

                search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={search}&limit=1"
                logging.warning(search_url)
            else:
                await ctx.send("``your mom``")

            async with aiohttp.ClientSession() as cs:
                async with cs.get(search_url) as r:
                    res = await r.json()
                    logging.warning(res[3][0])
                    await ctx.send(res[3][0])

        except IndexError:
            await ctx.send(f"``there is no page called {search}``")





    @app_commands.command(name="convertcase",description="convert your case of word and sentence")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(message = "the message that you want to convert the case ")
    @app_commands.choices(type = [
        Choice(name="title case",value="Title"),
        Choice(name="upper case",value="upper"),
        Choice(name="lower case",value="lower"),
        Choice(name="capitalize case",value="capitalize"),
        Choice(name="swap case", value="swap"),
        Choice(name="alternate case", value="alt")
    ])
    async def convertcase(self,interaction : discord.Interaction ,type:str,message: str):
        button = Button(label="delete", style=discord.ButtonStyle.danger)
        view = View()

        async def button_callback(interaction):
            await interaction.message.delete()

        button.callback = button_callback
        view.add_item(button)

        if str(type) == "Title":
            embed = discord.Embed(description=f"**{message.title()}**",colour= discord.Colour.blue())

            await interaction.response.send_message(embed = embed, view = view)
            return
        elif str(type) == "upper":
            message = discord.Embed(description=f"**{message.upper()}**",colour= discord.Colour.blue())

            await interaction.response.send_message(embed = message, view=view)
            return
        elif str(type) == "lower":
            message =discord.Embed(description=f"**{message.lower()}**",colour= discord.Colour.blue())

            await interaction.response.send_message(embed =message,view=view)
            return
        elif str(type) == "capitalize":
            message= discord.Embed(description=f"**{message.capitalize()}**",colour= discord.Colour.blue())

            await interaction.response.send_message(embed = message,view=view)
            return
        elif str(type) == "swap":
            message = discord.Embed(description=f"**{message.swapcase()}**",colour= discord.Colour.blue())

            await interaction.response.send_message(embed = message, view=view)
            return
        elif str(type) == "alt":
            finalswap = ""
            count = len(message)
            i = 0

            while (i < count):
                if i % 2 == 0:
                    # print(str.lower(apple[i]),end="")
                    finalswap += str.lower(message[i])

                else:
                    finalswap += str.upper(message[i])
                i += 1
            embed = discord.Embed(description=f"**{finalswap}**",colour= discord.Colour.blue())

            await interaction.response.send_message(embed = embed,view=view)
            return
        else:
            embed = discord.Embed(title="something went wrong")
            await interaction.response.send_message(embed,ephemeral=True)






























async def setup(bot: SussyBot) -> None:
    await bot.add_cog(
        randomapi(bot))