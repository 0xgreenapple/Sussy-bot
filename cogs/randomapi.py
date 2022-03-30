import logging
import os
import discord
import aiohttp
import random
from requests import get
from discord.ext import commands



class image(commands.Cog):

    def __init__(self, client):
        self.client = client



                                  #apis from random api ml.com


#random api ml animals command ========================================================================


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
    @commands.command()
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
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed3)
                await ctx.message.clear_reaction("✅")





#give a random dog image
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







#joke command
    @commands.command()
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as session:
            link = "https://some-random-api.ml/joke"
            async with session.get(link) as response:
                data = await response.json()
                joke = data["joke"]
                embed3 = discord.Embed(title="", description=f"**{joke}**", colour=discord.Colour.random())
                await ctx.send("amongus ",delay=10)
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed3)
                await ctx.message.clear_reaction("✅")



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
    @commands.command(description="get a user triggerd")
    async def trigger(self, ctx, member: discord.Member = None):

        if member != None:
            search_url = f"https://some-random-api.ml/canvas/triggered?avatar={member.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")

            if resp.status_code == 200:
                open('trigger.gif', 'wb').write(resp.content)
                d = open("trigger.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'
                logging.warning(file_to_send)

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File("trigger.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)
        else:
            search_url = f"https://some-random-api.ml/canvas/triggered?avatar={ctx.message.author.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")

            if resp.status_code == 200:
                open('trigger.gif', 'wb').write(resp.content)
                d = open("trigger.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'
                logging.warning(file_to_send)

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File("trigger.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)




#jai api

    @commands.command(description="get a user in the jail")
    async def jail(self, ctx, member: discord.Member = None):

        if member != None:
            search_url = f"https://some-random-api.ml/canvas/jail?avatar={member.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")

            if resp.status_code == 200:
                open('jail.gif', 'wb').write(resp.content)
                d = open("jail.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'
                logging.warning(file_to_send)

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File("jail.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)
        else:
            search_url = f"https://some-random-api.ml/canvas/jail?avatar={ctx.message.author.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")

            if resp.status_code == 200:
                open('jail.gif', 'wb').write(resp.content)
                d = open("jail.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'
                logging.warning(file_to_send)

                await ctx.message.add_reaction("✅")

                await ctx.send(file=discord.File("jail.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)



#gay command
    @commands.command(description="show your gay pride")
    async def gay(self, ctx, member: discord.Member = None):
        if member != None:
            search_url = f"https://some-random-api.ml/canvas/gay?avatar={member.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")

            if resp.status_code == 200:
                open('gay.gif', 'wb').write(resp.content)
                d = open("gay.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File("gay.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)
        else:
            search_url = f"https://some-random-api.ml/canvas/gay?avatar={ctx.message.author.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")

            if resp.status_code == 200:
                open('gay.gif', 'wb').write(resp.content)
                d = open("gay.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File("gay.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)
            await ctx.send("**noice**")



#glass command put someone in glass

    @commands.command(description="get a user in glass")
    async def glass(self, ctx, member: discord.Member = None):
        if member != None:
            search_url = f"https://some-random-api.ml/canvas/glass?avatar={member.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")
            if resp.status_code == 200:
                open('glass.gif', 'wb').write(resp.content)
                d = open("glass.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File("glass.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)
        else:
            search_url = f"https://some-random-api.ml/canvas/glass?avatar={ctx.message.author.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")
            if resp.status_code == 200:
                open('glass.gif', 'wb').write(resp.content)
                d = open("glass.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File("glass.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)

#make someone wasted

    @commands.command(description="get a user wasted")
    async def wasted(self, ctx, member: discord.Member = None):
        if member != None:
            search_url = f"https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")
            if resp.status_code == 200:
                open('wasted.gif', 'wb').write(resp.content)
                d = open("wasted.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File("wasted.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)
            await ctx.send("Invalid user!")

        else:
            search_url = f"https://some-random-api.ml/canvas/wasted?avatar={ctx.message.author.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")
            if resp.status_code == 200:
                open('wasted.gif', 'wb').write(resp.content)
                d = open("wasted.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File("wasted.gif"))
                await ctx.message.clear_reaction("✅")

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)



#make somone comrade

    @commands.command(description="get a user comrade")
    async def comrade(self, ctx, member: discord.Member = None):
        if member is None:
            search_url = f"https://some-random-api.ml/canvas/comrade?avatar={ctx.message.author.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")
            if resp.status_code == 200:
                open('comrade.gif', 'wb').write(resp.content)
                d = open("comrade.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File("comrade.gif"))
                await ctx.message.clear_reaction("✅")
                logging.warning("hello world")

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)
        else:
            search_url = f"https://some-random-api.ml/canvas/comrade?avatar={member.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")
            if resp.status_code == 200:
                open('comrade.gif', 'wb').write(resp.content)
                d = open("comrade.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.message.add_reaction("✅")
                await ctx.send(file=discord.File("comrade.gif"))
                await ctx.message.clear_reaction("✅")
                logging.warning("hello world")

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)


#get a color by hex code

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





























def setup(client):
    client.add_cog(image(client))