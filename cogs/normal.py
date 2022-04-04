import discord
import datetime, time
from discord.ext import commands
import psutil
from discord.ext.commands import cooldown, BucketType, MemberConverter


class general(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime

        startTime = time.time()

    @commands.command(description="get a user basic info",aliases=['wi'])
    @cooldown(1, 5, BucketType.channel)
    async def whois(self, ctx, member: discord.Member=None ):
        if member != None :
            embed10 = discord.Embed(title=member.display_name, description=member.mention, url=member.avatar_url,
                                    colour=discord.Colour.red())
            embed10.add_field(name="ID", value=member.id, inline=False)
            embed10.add_field(name="status", value=member.status, inline=False)
            embed10.add_field(name="__**join server at**__ ", value=member.joined_at.strftime('%a, %d %B %Y, %I:%M %p UTC'))
            embed10.add_field(name="__**created at**__ ", value=member.created_at.strftime('%a, %d %B %Y, %I:%M %p UTC'))
            embed10.add_field(name='Bot?', value=member.bot)
            embed10.set_thumbnail(url=member.avatar_url)
            await ctx.message.add_reaction("✅")
            await ctx.send(embed=embed10)
        else:
             embed10 = discord.Embed(title=ctx.message.author.name, description=ctx.message.author.mention, url=ctx.message.author.avatar_url,
                                 colour=discord.Colour.red())
             embed10.add_field(name="ID", value=ctx.message.author.id, inline=False)
             embed10.add_field(name="status", value=ctx.message.author.status, inline=False)
             embed10.add_field(name="__**join server at**__ ", value=ctx.message.author.joined_at.strftime('%a, %d %B %Y, %I:%M %p UTC'))
             embed10.add_field(name="__**created at**__ ", value=ctx.message.author.created_at.strftime('%a, %d %B %Y, %I:%M %p UTC'))
             embed10.set_thumbnail(url=ctx.message.author.avatar_url)
             await ctx.message.add_reaction("✅")
             await ctx.send(embed=embed10)




    #whois command error
    @whois.error
    async def whois_error(self, ctx, error):
        if isinstance(error , commands.MemberNotFound):
            embed = discord.Embed(title="invaid username | ur mom :)")
            await ctx.send(embed = embed)

        if isinstance(error , commands.CommandOnCooldown):
            embed = discord.Embed(title=error)
            await ctx.send(embed  = embed)
        else:
            embed = discord.Embed(title="something went wrong")
            await ctx.send(embed=embed)




    #user info beta
    @commands.command(aliases=['ui'])

    @cooldown(1, 5, BucketType.channel)
    async def userinfo(self, ctx, member):

        if member[0] == '<' and member[1] == '@':
            converter = MemberConverter()
            member = await converter.convert(ctx, member)
        elif member.isnumeric():
            member = int(member)

        members = await ctx.guild.fetch_members().flatten()
        multiple_member_array = []

        if isinstance(member, discord.Member):
            for members_list in members:
                if member.name.lower() in members_list.name.lower():
                    multiple_member_array.append(members_list)
                else:
                    pass

        elif isinstance(member, int):
            for member_list in members:
                if member_list.id == member:
                    multiple_member_array.append(member_list)
                else:
                    pass

        else:
            for members_list in members:
                if member.lower() in members_list.name.lower():
                    multiple_member_array.append(members_list)
                else:
                    pass

        if len(multiple_member_array) == 1:

            roles = []
            for role in multiple_member_array[0].roles:
                roles.append(role)

            embed = discord.Embed(
                colour=discord.Colour.random(),
            )
            embed.set_author(name=f'User Info - {multiple_member_array[0]}')
            embed.set_thumbnail(url=multiple_member_array[0].avatar_url)
            embed.set_footer(text=f'infromation requested by {ctx.message.author.display_name}',icon_url=ctx.message.author.avatar_url)

            embed.add_field(name='ID:', value=multiple_member_array[0].id)
            embed.add_field(name='Member Name:', value=multiple_member_array[0])
            embed.add_field(name='Member Nickname:', value=multiple_member_array[0].display_name)

            embed.add_field(name='Created at: ',
                            value=multiple_member_array[0].created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
            embed.add_field(name='Joined at:',
                            value=multiple_member_array[0].joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))


            await ctx.send(embed=embed)


        elif len(multiple_member_array) > 1:

            multiple_member_array_duplicate_array = []
            for multiple_member_array_duplicate in multiple_member_array:
                if len(multiple_member_array_duplicate_array) < 10:
                    multiple_member_array_duplicate_array.append(multiple_member_array_duplicate.name)
                else:
                    break

            embed = discord.Embed(
                title=f'Search for {member}\nFound multiple results (Max 10)',
                description=f'\n'.join(multiple_member_array_duplicate_array),
                colour=0x808080
            )
            await ctx.send(embed=embed)

        else:
            await ctx.send(f'The member `{member}` does not exist!')




    # Userinfo: Error handling

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                '```\n$userinfo {member_name}\n          ^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.send('I am Forbidden from doing this command, please check if `server members intent` is enabled')
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback')
            raise error



    @commands.command(description="do ping to get bot infromation",aliases=['mem'])
    @cooldown(1, 5, BucketType.user)
    async def ping(self,ctx):
        embed11 = discord.Embed(title="pong! 🏓 latency is "f"{round(self.client.latency * 1000)}ms",description="",url="", colour=discord.Colour.red())
        await ctx.message.add_reaction("🏓")
        await ctx.send(embed=embed11)

        #await ctx.send_message("pong! latency is "f"{round(self.client.latency * 1000)} ms")

    '''@nextcord.slash_command()
    async def info(self, interactions : interactions):
        await ctx.send("owner = green apple#6495")
        await ctx.send("command prefix is " + f"('{self.client.command_prefixs}')")'''

    '''@nextcord.slash_command()
    async def commandlist(self, interactions : interactions):
        await ctx.send("$info| bot info")
        await ctx.send("$kick| kick a member")
        await ctx.send("$ban| ban a member ")
        await ctx.send("$ping| bot latency")
        await ctx.send("$avatar| for user avatar")'''

    @commands.command(description="get a user avatar",aliases=['av'])
    @cooldown(1, 5, BucketType.channel)
    async def avatar(self, ctx, member: discord.Member = None):

        if member is None:
            embed10 = discord.Embed(title=ctx.message.author.display_name, description="", url=ctx.message.author.avatar_url,
                                   colour=discord.Colour.blue())
            embed10.set_image(url=ctx.message.author.avatar_url)
            await ctx.message.add_reaction("✅")
            await ctx.send(embed=embed10)
            return
        elif member is not None:
            embed9 = discord.Embed(title=member.display_name, description="", url=member.avatar_url, colour=discord.Colour.blue())
            embed9.set_image(url=member.avatar_url)
            await ctx.message.add_reactio
        else:
            embed = discord.Embed(title="**oh i m dying**")

    @avatar.error
    async def avatar_error(self,ctx,error):
        if isinstance(error , commands.MissingRequiredArgument):
            embed = discord.Embed(colour=0x0000ff)
            embed.set_image(url=f'{ctx.author.avatar_url}')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            embed = discord.Embed(title="oh! somthing went wrong do $help")
            await ctx.send(embed = embed)



    @commands.command(description= "get list of all commands")
    async def list(self,ctx):
        embed = discord.Embed(title=" commands list :", url="", description="this is the list of all command in the bot"
                                                                           "\n"
                                                                           "__**general commands**__ "
                                                                           "\n"
                                                                           "━━━━━━━━━━━━━━━━━━━━━━━━"
                                                                           , color=0xFF5733)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/917479518040645712/951103745817731132/sussy_server_3.gif")
        embed.add_field(name="__**help**__", value="do ($help) to view command list")
        embed.add_field(name="__**avatar**__", value="do ($avatar <user>) to view user avatars")
        embed.add_field(name="__**ping**__", value="do ($ping) to view user client ping")
        embed.add_field(name="__**info**__ ", value="do ($info) to view bot infromation")

        embed2 = discord.Embed(title="", url="", description="this is the list of all mod commands in the bot"
                                                                           "\n"
                                                                           "__**general mod commands**__ "
                                                                           "\n"
                                                                           "━━━━━━━━━━━━━━━━━━━━━━━━"
                              , color=0xFF5733)
        embed.set_thumbnail(
            url="")
        embed2.add_field(name="__**kick**__", value="do ($kick <user> <reason>) to kick a user")
        embed2.add_field(name="__**ban**__", value="do ($ban <user> <reason>) to ban a user")
        embed2.add_field(name="__**unban**__", value="do ($unban <user> ) to unban a user")
        embed2.add_field(name="__**clear**__ ", value="do ($clear <amount>) to clear the specific amount of messages in the channel")
        await ctx.send(embed=embed)
        await ctx.send(embed=embed2)







    @commands.command()
    async def uptime(self,ctx):

        # what this is doing is creating a variable called 'uptime' and assigning it
        # a string value based off calling a time.time() snapshot now, and subtracting
        # the global from earlier
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - startTime))))
        await ctx.send(uptime)

    @commands.command()
    @cooldown(1, 3, BucketType.user)
    async def stats(self,ctx):
        bedem = discord.Embed(title='System Resource Usage', description='See CPU and memory usage of the system.')
        bedem.add_field(name='CPU Usage', value=f'{psutil.cpu_percent()}%', inline=False)
        bedem.add_field(name='Memory Usage', value=f'{psutil.virtual_memory().percent}%', inline=False)
        bedem.add_field(name='Available Memory',
                        value=f'{psutil.virtual_memory().available * 100 / psutil.virtual_memory().total}%',
                        inline=False)

        await ctx.send(embed=bedem)

    @commands.command()
    @cooldown(1, 3, BucketType.user)
    async def status(self,ctx):

        a = round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
        z = 100 - a
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - startTime))))
        embed = discord.Embed(title="sussy-bot status | version alpha",description="")
        embed.add_field(name="ping",value=f'{round(self.client.latency * 1000)}ms')
        embed.add_field(name="Memory ",value=f'{z}% used',)
        embed.add_field(name="Servers",value=f"{len(self.client.guilds)}",)
        embed.add_field(name="Uptime",value=uptime,)
        "embed.set_thumbnail(url=self.client.user.avatar_url)"
        embed.set_author(name="sussy-bot",icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)



    @commands.command()
    @cooldown(1, 59, BucketType.user)
    async def send_dm(self, ctx, member: discord.Member, *, content):
        channel = await member.create_dm()
        await channel.send(content)


    @commands.command()
    @cooldown(1, 59, BucketType.user)
    async def bugs(self,ctx, *,message):
        if len(message) >= 100:
            return
        else:
            with open("write.txt", "a") as f:
                f.write(f"\n{ctx.guild.name} : {ctx.message.author.display_name} : {message}")
            embed = discord.Embed(title="done")
            await ctx.send(embed = embed)

    @commands.command()
    @cooldown(1 ,10 , BucketType.user)
    async def morse(self, ctx, *, message):

        MORSE_DICT = {'A': '.-', 'B': '-...',
                      'C': '-.-.', 'D': '-..', 'E': '.',
                      'F': '..-.', 'G': '--.', 'H': '....',
                      'I': '..', 'J': '.---', 'K': '-.-',
                      'L': '.-..', 'M': '--', 'N': '-.',
                      'O': '---', 'P': '.--.', 'Q': '--.-',
                      'R': '.-.', 'S': '...', 'T': '-',
                      'U': '..-', 'V': '...-', 'W': '.--',
                      'X': '-..-', 'Y': '-.--', 'Z': '--..',
                      '1': '.----', '2': '..---', '3': '...--',
                      '4': '....-', '5': '.....', '6': '-....',
                      '7': '--...', '8': '---..', '9': '----.',
                      '0': '-----', ', ': '--..--', '.': '.-.-.-',
                      '?': '..--..', '/': '-..-.', '-': '-....-',
                      '(': '-.--.', ')': '-.--.-'}

        cipher = ''

        for letter in message.upper():
            if letter != ' ':
                cipher += MORSE_DICT[letter] + ' '
            else:
                cipher += ' '

        await ctx.send(f'Here is your cyphered text:\n```\n{cipher}\n```')

    @commands.command()
    async def text(self, ctx, *, message):
        if len(message) >= 20:
            await ctx.send("text too long")
            return

        else:
            MORSE_DICT = {'A': '🇦', 'B': '🇧',
                      'C': '🇨', 'D': '🇩', 'E': '🇪',
                      'F': '🇫', 'G': '🇬', 'H': '🇭',
                      'I': '🇮', 'J': '🇯', 'K': '🇰',
                      'L': '🇱', 'M': '🇲', 'N': '🇳',
                      'O': '🇴', 'P': '🇵', 'Q': '🇶',
                      'R': '🇷', 'S': '🇸', 'T': '🇹',
                      'U': '🇺', 'V': '🇻', 'W': '🇼',
                      'X': '🇽', 'Y': '🇾', 'Z': '🇿',
                      '1': '1️⃣', '2': '2️⃣', '3': '3️⃣',
                      '4': '4️⃣', '5': '5️⃣', '6': '6️⃣',
                      '7': '7️⃣', '8': '8️⃣', '9': '9️⃣',
                      '0': '0️⃣'}

            cipher = ''

            for letter in message.upper():
                if letter != ' ':
                    cipher += MORSE_DICT[letter] + ' '
                else:
                     cipher += ' '

        await ctx.send(cipher)
def setup(client):
    client.add_cog(general(client))