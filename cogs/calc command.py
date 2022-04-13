import asyncio

import discord
import datetime
import warnings
from discord.ext import commands, tasks



class calc(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def calc(self,ctx,number1 , pre , number2):
        emoji = self.client.get_emoji("<:buffering:739613552058564639>")
        try:
           if pre == "+":
              number1 = int(number1)
              number2 = int(number2)
              a = number1+number2
              await ctx.send(a)
              return
           elif pre == "-":
              number1 = int(number1)
              number2 = int(number2)
              b = number1 - number2
              await ctx.send(b)
              return

           elif pre == "/":
              number1 = int(number1)
              number2 = int(number2)
              c = number1 / number2
              await ctx.send(c)
              return

           elif pre == "*":
              number1 = int(number1)
              number2 = int(number2)
              d = number1 * number2
              await ctx.send(d)
              return
           else:
              await ctx.send("somthing went wrong")
        except ZeroDivisionError:

            await ctx.message.add_reaction("🚫")

            await ctx.send(f"{number1} / {number2} = ur mom",delete_after= 5)
            await  ctx.message.clear_reaction("🚫")
        except:

            await ctx.send("ur mom")
















async def setup(bot):
    await bot.add_cog(calc(bot))