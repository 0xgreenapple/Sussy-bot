import discord
import os
import random
import json
import datetime, time
import asyncio
from discord import Intents
from discord.ext import commands, tasks
from itertools import cycle




intents = Intents.default()
intents.members = True


def get_prefix(client, message): ##first we define get_prefix
    with open('prefixes.json', 'r') as f: ##we open and read the prefixes.json, assuming it's in the same file
        prefixes = json.load(f) #load the json as prefixes
    return prefixes[str(message.guild.id)]




client = commands.Bot(command_prefix=(get_prefix),case_insensitive=True, intents=intents)
client.remove_command("help")

status = cycle(['amongus','SUS','bruh','ur mom','0101000101','game of life'])
@client.event
async def on_guild_join(guild): #when the bot joins the guild
    with open('prefixes.json', 'r') as f: #read the prefix.json file
        prefixes = json.load(f) #load the json file

    prefixes[str(guild.id)] = '$'#default prefix

    with open('prefixes.json', 'w') as f: #write in the prefix.json "message.guild.id": "bl!"
        json.dump(prefixes, f, indent=4) #the indent is to make everything look a bit neater

@client.event
async def on_guild_remove(guild): #when the bot is removed from the guild
    with open('prefixes.json', 'r') as f: #read the file
        prefixes = json.load(f)

    prefixes.pop(str(guild.id)) #find the guild.id that bot was removed from

    with open('prefixes.json', 'w') as f: #deletes the guild.id as well as its prefix
        json.dump(prefixes, f, indent=4)

#=====================================================================================================
@client.command()
@commands.is_owner()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')
  print(f'{extension} successfully loaded')
  await ctx.send('Cogs reloaded')

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')
  print(f'{extension} successfully unloaded')
  await ctx.send('Cogs unloaded')

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')
  client.load_extension(f'cogs.{extension}')
  await ctx.send(f'{extension} successfully re-loaded')
  await ctx.send('Cog reloaded')


#======================================================================================








#======================================================================================

try:
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f"cogs.{filename[:-3]}")
except Exception as e:
    print("Cogs error: Cannot load cogs")
    print("\033[5;37;40m\033[1;33;40mWARNING\033[1;33;40m\033[0;37;40m", end=' ')
    print("Functionality limited!\n")
    print(f"exception thrown:\n{e}")
#======================================================================================

@client.command(pass_context=True)
@commands.has_permissions(administrator=True) #ensure that only administrators can use this command
async def changeprefix(ctx, prefix): #command: bl!changeprefix ...
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f: #writes the new prefix into the .json
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: {prefix}') #confirms the prefix it's been changed to
#next step completely optional: changes bot nickname to also have prefix in the nickname
    name=f'{prefix}BotBot'





#======================================================================================
@client.event
async def on_ready():
    change_status.start()
    print(f"{client.user.display_name} is online")
    '''await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching,name = 'SUS'))'''

@tasks.loop(seconds=3600)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

#member count and reactions on messages




@client.event
async def on_message(message):
    a = [
                        "among us",
                        "go outside touch some grass",
                        "ur mom",
                        "imposter was ejected",
                        "you are sus",
                        "SUS",
                        "Wtf you want to me",
                        "red was the imposter",
                        "f you kid",
                        "what the fuck you looking nice today",
                        "hmm tell me who is baka",
                        "ummmm u suck"
                    ]
    message_in = message.content

    channel = client.get_channel('952460342313758760')
    print(f"{message.guild.name} : {message.channel} : {message.author}: {message.author.name}: {message.content}")
    sussyserver_guild = client.get_guild(917471209329946695)

    if message.author.bot:
        return
    elif message_in.lower().find('sus') != -1:
        await message.channel.send("amongus",delete_after= 10)

    elif (client.user in message.mentions) and message_in.lower().find('prefix') != -1:
        embed = discord.Embed(title=f"YO :wave:  my prefix is {get_prefix(client,message)}",)

        await message.channel.send(embed=embed)
    elif client.user in message.mentions:
        if message_in.lower().find('amongus') != -1 or message_in.lower().find(
                'cool') != -1 or message_in.lower().find('good') != -1 or message_in.lower().find('nice') != -1:
            await message.channel.send(f'amongus')
        elif message_in.lower().find('bad') != -1 or message_in.lower().find(
                'horrible') != -1 or message_in.lower().find('suck') != -1 or message_in.lower().find(
                'terrible') != -1 or message_in.lower().find('waste') != -1 or message_in.lower().find(
                'fk') != -1 or message_in.lower().find('fuck') != -1:
            await message.channel.send(f'ur mom',delete_after=11)
        elif message_in.lower().find('how are you') != -1:
            await message.channel.send(f'I can smell sus, {message.author.display_name}')
        elif message_in.lower().find('ur mom') != -1:
            await message.channel.send(f'ur mom in my basement, {message.author.display_name}')
        elif message_in.lower().find('ur dad') != -1:
            await message.channel.send(f'shut up YOU, {message.author.display_name}')
        elif message_in.lower().find('fuck you') != -1:
            await message.channel.send(f'f you too, {message.author.display_name}')
        elif message_in.lower().find('what do you do for living') != -1:
            await message.channel.send(f'i eat bananas , {message.author.display_name}')
        else:
            await message.channel.send(f'{random.choice(a)}, **{message.author.display_name}**!')



    await client.process_commands(message)





'''end '''






token = os.environ['TOKEN']
client.run(token)
