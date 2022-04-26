import discord
from discord import app_commands
from discord.ext import commands
import random
import json
import motor.motor_asyncio

import logging

class economy(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    async def open_account(self,user):
        users = await self.get_bank_data()
        logging.warning(user.id)
        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["Wallet"] = 0
            users[str(user.id)]["Bank"] = 0
            users[str(user.id)]["Net"] = 0
            users[str(user.id)]["Item"] = []
        with open("economy/bank.json", 'w') as f:
            json.dump(users, f)
        return True

    async def open_inv(self,user,items):
        users = await self.get_inv_data()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)][items] = 1


            """users[str(user.id)][items] += 1"""

        with open("economy/inv.json", 'w') as f:
            json.dump(users, f)

        return True

    async def get_bank_data(self):
        with open("economy/bank.json", 'r') as f:
            users = json.load(f)
        return users

    async def get_inv_data(self):
        with open("economy/inv.json") as f:
            inv = json.load(f)
        return inv

    @commands.command()
    async def balance(self, ctx):
        await self.open_account(ctx.author)

        user = ctx.author

        users = await self.get_bank_data()

        wallet_amt = users[str(user.id)]["Wallet"]
        bank_amt = users[str(user.id)]["Bank"]
        Net = users[str(user.id)]["Net"]

        em = discord.Embed(title=f"{ctx.author.name}'s balance.", color=discord.Color.teal())
        em.add_field(name="Wallet Balance", value=wallet_amt)
        em.add_field(name="Bank Balance", value=bank_amt)
        em.add_field(name="networth", value=Net)
        await ctx.send(embed=em)




    #beg command
    @commands.command()
    async def beg(self, ctx):
        hola = ["candy", "coffee", "watter bottel",] #add ietms to inv
        items = random.choice(hola)

        await self.open_account(ctx.author)

        await self.open_inv(ctx.author,items)

        inv = await self.get_inv_data()

        user = ctx.author

        if items not in inv[str(user.id)]:
            inv[str(user.id)][items] = 0
            with open("economy/inv.json", 'w') as f:
                json.dump(inv, f)
        else:
            inv[str(user.id)][items] += 1
            with open("economy/inv.json", 'w') as f:
                json.dump(inv, f)

        users = await self.get_bank_data()
        token = random.randrange(100)

        hello = [int(token), "imagine begging what a noob"]

        abs = random.choice(items)
        earnings = random.choice(hello)
        if earnings == hello[1]:
            await ctx.send(earnings)
        elif earnings == hello[0]:

            users[str(user.id)]["Wallet"] += earnings
            users[str(user.id)]["Net"] += earnings




            with open("economy/bank.json", 'w') as f:
                json.dump(users, f)

            await ctx.send(f"Someone gave your {earnings} coins")

    @commands.command()
    async def dep(self, ctx, amount :int =None):
        await self.open_account(ctx.author)

        user = ctx.author
        users = await self.get_bank_data()
        if amount is None:
            depcoin = users[str(user.id)]["Wallet"]
            users[str(user.id)]["Bank"] = depcoin
            users[str(user.id)]["Wallet"] = users[str(user.id)]["Wallet"] - users[str(user.id)]["Bank"]
            with open("economy/bank.json", 'w') as f:
                json.dump(users, f)
            await ctx.send(f"{depcoin} sus coins deposite to your bank")
        else:
            if amount > int(users[str(user.id)]["Wallet"]):
                await ctx.send("your mom")
            elif amount <= int(users[str(user.id)]["Wallet"]) and amount >= 0:
                depcoin = amount
                users[str(user.id)]["Bank"] = depcoin
                users[str(user.id)]["Wallet"] = users[str(user.id)]["Wallet"] - depcoin
                with open("economy/bank.json", 'w') as f:
                    json.dump(users, f)
                await ctx.send(f"{depcoin} sus coins deposite to your bank")
            else:
                await ctx.send("your mom")




    @commands.command()
    async def give_money(self, ctx,member: discord.Member = None,amount=int):
        await self.open_account(member)

        logging.warning(ctx.author)
        logging.warning(member)
        user = member
        users = await self.get_bank_data()

        users[str(user.id)]["Bank"] = amount
        logging.warning(users[str(user.id)]["Bank"])
        logging.warning(users[str(user.id)])
        """with open("economy/bank.json", 'w') as f:
            json.dump(users, f)"""
        await ctx.send(f"{amount} sus coins deposite to your bank")


    @commands.command()
    async def shop(self,ctx):
        items = ["smartphone","laptop"]
        embed = discord.Embed(title="itmes")
        embed.add_field(name=items[0],value='400000$')
        embed.add_field(name=items[1],value='100000000$')
        await ctx.send(embed=embed)





    @commands.command()
    async def buy(self,ctx,nameitem:str = None,itemprice=400000):
        if nameitem is None:
            await ctx.send(f"there is not a item in the shop called {nameitem}")
        else:
            await self.open_account(ctx.author)
            await self.open_inv(ctx.author, nameitem)
            inv = await self.get_inv_data()
            user = ctx.author
            if nameitem not in inv[str(user.id)]:

                inv[str(user.id)][nameitem] = 1
                with open("economy/inv.json", 'w') as f:
                    json.dump(inv, f)
            else:
                inv[str(user.id)][nameitem] += 1
                with open("economy/inv.json", 'w') as f:
                    json.dump(inv, f)
            users = await self.get_bank_data()
            users[str(user.id)]["Wallet"] = users[str(user.id)]["Wallet"] - itemprice
            with open("economy/bank.json", 'w') as f:
                json.dump(users, f)
            await ctx.send(f"you have {nameitem}")

    @commands.command()
    async def beger(self,ctx):
        db = self.bot.mongoConnect["sussybot"]
        collection = db["verify"]
        erning = random.randint(0,100)
async def setup(bot: commands.Bot ) -> None:
    await bot.add_cog(
        economy(bot))