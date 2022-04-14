import asyncio

import discord
import datetime
import warnings
from discord.ext import commands, tasks
from discord import app_commands
from discord.app_commands import Choice
from discord.ui import Select , View




class calc_command(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


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

    @app_commands.command(name="calc",description="are you bad at math use this")
    @app_commands.choices(function = [
        Choice(name="subtraction",value="-"),
        Choice(name="addition",value="+"),
        Choice(name="division",value="/"),
        Choice(name="multiplication",value="*"),
    ])
    async def calc_slash(self, interaction : discord.Interaction ,function:str ,number1:int,number2:int):
        try:
           if function == "+":
              number1 = int(number1)
              number2 = int(number2)
              a = number1+number2
              await interaction.response.send_message(f"result : ``{a}``")
              return
           elif function == "-":
              number1 = int(number1)
              number2 = int(number2)
              b = number1 - number2
              await interaction.response.send_message(f"result : ``{b}``")
              return

           elif function == "/":
              number1 = int(number1)
              number2 = int(number2)
              c = number1 / number2
              await interaction.response.send_message(f"result : ``{c}``")
              return

           elif function == "*":
              number1 = int(number1)
              number2 = int(number2)
              d = number1 * number2
              await interaction.response.send_message(f"result : ``{d}``")
              return
        except ZeroDivisionError:


            await interaction.response.send_message(f"{number1} / {number2} = ur mom", ephemeral=True)


    @commands.command()
    async def testtest1(self, ctx):
        select = Select(
            placeholder="choose a test",
            options=[
                discord.SelectOption(
                    label="choose",
                    emoji="1️⃣",
                    value="apple",
                    description="choose the asdasdasdasdasd"
                ),
                discord.SelectOption(
                    label="choose",
                    emoji="2️⃣",
                    description="yes it is"
                )
            ]

        )
        async def my_callback(interaction):
            if select.values[0] == "apple":
                await interaction.response.send_message("hello")

        select.callback = my_callback
        view = View()
        view.add_item(select)
        await ctx.send("what",view =view)










async def setup(bot: commands.Bot ) -> None:
    await bot.add_cog(
        calc_command(bot))