import logging

import os
import discord
import aiohttp
import random
from requests import get
from discord.ext import commands



class fun(commands.Cog):

    def __init__(self, client):
        self.client = client


#reddit=====================================================================


    @commands.command(pass_context=True)
    async def memes(self, ctx):
        embed = discord.Embed(title="yo boi", description="")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def meirl(self, ctx):
        embed4 = discord.Embed(title="", description="")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/me_irl/new.json?sort=hot') as r:
                res = await r.json()
                embed4.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed4)


    @commands.command(pass_context=True)
    async def space(self, ctx):
        embed10 = discord.Embed(title="", description="")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/astrophotography/new.json?sort=hot') as r:
                res = await r.json()
                embed10.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed10)



#reddit=====================================================================











#------------------------------------------api random animal------------------------------------------------------
    @commands.command()
    async def animalfacts(self, ctx):
        async with aiohttp.ClientSession() as session:
            link = ["https://some-random-api.ml/animal/dog","https://some-random-api.ml/animal/cat",
                                                         "https://some-random-api.ml/animal/fox",
                    "https://some-random-api.ml/animal/birb","https://some-random-api.ml/animal/koala",
                    "https://some-random-api.ml/animal/kangaroo","https://some-random-api.ml/animal/raccoon",
                    "https://some-random-api.ml/animal/panda","https://some-random-api.ml/animal/red_panda",]
            list = random.choice(link)
            async with session.get(list) as response:
                data = await response.json()
                embed2 = discord.Embed(title="", description=data["fact"],
                                      colour=discord.Colour.random())
                embed2.set_image(url=data["image"])
                await ctx.send(embed=embed2)

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
                embed3 = discord.Embed(title="",description="",colour=discord.Colour.random())
                embed3.set_image(url=data["link"])
                await ctx.send(embed=embed3)

    @commands.command()
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as session:
            link = "https://some-random-api.ml/img/dog"
            async with session.get(link) as response:
                data = await response.json()
                embed3 = discord.Embed(title="", description="", colour=discord.Colour.random())
                embed3.set_image(url=data["link"])
                await ctx.send(embed=embed3)

    @commands.command()
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            link = "https://some-random-api.ml/img/cat"
            async with session.get(link) as response:
                data = await response.json()
                embed3 = discord.Embed(title="", description="", colour=discord.Colour.random())
                embed3.set_image(url=data["link"])
                await ctx.send(embed=embed3)

#===============================================================================







#-------------------------------------unsplash api-----------------------------------------------------------------
    @commands.command(pass_context=True)
    async def image(self, ctx, *, message=None):
        unsplashID = os.environ['UNSPLASH_KEY']
        embed4 = discord.Embed(title="", description="")
        search_url = None
        final_image = None
        if message != None:
            search_url = f'https://api.unsplash.com/search/photos?client_id={unsplashID}&query={message}&per_page=25'
        else:
            search_url = f'https://api.unsplash.com/photos/random?client_id={unsplashID}&count=2'

        async with aiohttp.ClientSession() as cs:
            async with cs.get(search_url) as r:
                res = await r.json()
                if message != None:
                    final_image = res['results'][random.randint(0, 25)]['urls']['small']
                else:
                    final_image = res[0]['urls']['small']

                embed4.set_image(url=final_image)
                await ctx.message.add_reaction("✅")
                await ctx.send(embed=embed4)


#===============================================================================================================











#---------------------------------------Tenor api-----------------------------------------------------------

    @commands.command(pass_context=True)
    async def gif(self, ctx, *, message=None):
        apikey = os.environ["GIF_KEY"]
        search_url = None
        if message != None:
            search_url = f"https://g.tenor.com/v1/search?q={message}&key={apikey}&limit=25"
        else:
            search_url = f"https://g.tenor.com/v1/random?q=%s&key={apikey}&limit=25"



        async with aiohttp.ClientSession() as cs:
            async with cs.get(search_url) as r:
                res = await r.json()

                if message == None:
                    #logging.warning(res['results'])
                    final_image = res["results"][random.randint(0, 25)]["media"][0]["tinygif"]["url"]
                else:
                    final_image = res["results"][random.randint(0, 25)]["media"][0]["tinygif"]["url"]

                await ctx.message.add_reaction("✅")
                await ctx.send(final_image)


#=================================================================================================================











#-------------------------------------random api------------------------------------------------------
    @commands.command()
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as session:
            link = "https://some-random-api.ml/joke"
            async with session.get(link) as response:
                data = await response.json()
                joke = data["joke"]
                embed3 = discord.Embed(title="", description=f"**{joke}**", colour=discord.Colour.red())
                await ctx.send(embed=embed3)

    @commands.command(pass_context=True)
    async def minecraft(self, ctx, *, username=None):

        search_url = None
        if username != None:
            search_url = f"https://some-random-api.ml/mc?username={username}"
        else:
            await ctx.send("fucking give me a name")
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


#trigger command--------------------------------------------------------------------------------------

    @commands.command(description="get a user triggerd")
    async def trigger(self, ctx, member: discord.Member = None):


        if member is None:
            await ctx.send("Invalid user!")
        else:
            search_url = f"https://some-random-api.ml/canvas/triggered?avatar={member.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")

            if resp.status_code == 200:
                open('trigger.gif', 'wb').write(resp.content)
                d = open("trigger.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'
                logging.warning(file_to_send)


                await ctx.send(file=discord.File("trigger.gif"))

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)

 #jail command=====================================================================
    @commands.command(description="get a user in the jail")
    async def jail(self, ctx, member: discord.Member = None):

        if member is None:
            await ctx.send("Invalid user!")
        else:
            search_url = f"https://some-random-api.ml/canvas/jail?avatar={member.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")


            if resp.status_code == 200:
                open('jail.gif', 'wb').write(resp.content)
                d = open("jail.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'
                logging.warning(file_to_send)


                await ctx.send(file=discord.File("jail.gif"))

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)

#gay=====================================================================
    @commands.command(description="show your gay pride")
    async def gay(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Invalid user!")
        else:
            search_url = f"https://some-random-api.ml/canvas/gay?avatar={member.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")

            if resp.status_code == 200:
                open('gay.gif', 'wb').write(resp.content)
                d = open("gay.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'


                await ctx.send(file=discord.File("gay.gif"))

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)


#glass=====================================================================
    @commands.command(description="get a user in glass")
    async def glass(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Invalid user!")
        else:
            search_url = f"https://some-random-api.ml/canvas/glass?avatar={member.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")
            if resp.status_code == 200:
                open('glass.gif', 'wb').write(resp.content)
                d = open("glass.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'


                await ctx.send(file=discord.File("glass.gif"))

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)


#get a user wasted=====================================================================
    @commands.command(description="get a user wasted")
    async def wasted(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Invalid user!")
        else:
            search_url = f"https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")
            if resp.status_code == 200:
                open('wasted.gif', 'wb').write(resp.content)
                d = open("wasted.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'

                await ctx.send(file=discord.File("wasted.gif"))

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)


#comrade=====================================================================
    @commands.command(description="get a user comrade")
    async def comrade(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Invalid user!")
        else:
            search_url = f"https://some-random-api.ml/canvas/comrade?avatar={member.avatar_url}"
            slice_object = slice(-14)
            resp = get(f"{search_url[slice_object]}png")
            if resp.status_code == 200:
                open('comrade.gif', 'wb').write(resp.content)
                d = open("comrade.gif", "r+")
                file_to_send = f'{os.getcwd()}/{d.name}'


                await ctx.send(file=discord.File("comrade.gif"))

            elif resp.status_code != 200:
                jsonresp = resp.json()

                print(resp.status_code)
                print(jsonresp)




#--------------------------------------------------------------------------------------------------



def setup(client):
    client.add_cog(fun(client))