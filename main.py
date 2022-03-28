import discord
import os

from discord.ext import commands, tasks
from itertools import cycle


client = commands.Bot(command_prefix='$')

status = cycle(['amongus','SUS','0_0','ur mom'])


@client.command()
async def load(ctx, extension):
    print("loaded")
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    print("unloaded")
    client.upload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
@client.event
async def on_ready():
    change_status.start()
    print(f"{client.user.display_name} is online")
    '''await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching,name = 'SUS'))'''

@tasks.loop(seconds=1200)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

#member count and reactions on messages
@client.event
async def on_message(message):
    badwords = ["fuck", "shit", "sex"]
    if str(badwords) in message.content.lower():
        await message.delete()



@client.event
async def on_message(message):

    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    sussyserver_guild = client.get_guild(917471209329946695)


    if "lmao" in message.content.lower():
        await message.delete()
        await message.channel.send("https://media.discordapp.net/attachments/829651225212354570/953880595354746940/ezgif.com-gif-maker_3.gif")
    emoji = "<:pepecry_laugh:939420378273566760>"
    emoji2 = "✅"
    if "$list" in message.content.lower():
            await message.add_reaction(emoji2)
    elif "$membercount"  == message.content.lower():
        await message.channel.send(f"```py\n{sussyserver_guild.member_count}```")
    await client.process_commands(message)
'''end '''

token = os.environ['TOKEN']
client.run(token)
