import logging
from bot import SussyBot
import discord
import datetime, time
from datetime import datetime
from datetime import timedelta
from discord.ext import commands
import psutil
from discord.ext.commands import cooldown, BucketType, MemberConverter
from discord import app_commands, role
from discord.ui import Button, View, TextInput
from discord import ui
from discord.utils import get



class normal(commands.Cog):
    def __init__(self, bot: SussyBot) -> None:
        self.bot = bot
        global startTime

        startTime = time.time()


    """#whois slash_error
    @whoisslash.error
    async def whoisslash_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"{error}", ephemeral=True)
        else:
            await interaction.response.send_message("something went wrong do $help or report for bugs by doing $bugs <bugs>", ephemeral=True)
"""

    # whois prfefix command
    @commands.hybrid_command(name="whois", description="Get a user basic information")
    @app_commands.describe(member="User")
    @cooldown(1, 5, BucketType.channel)
    async def whois(self, ctx, member: discord.Member = None):
        if member != None:
            roles = []
            for role in member.roles:
                roles.append(role)
            embed10 = discord.Embed(title=member.display_name, description=member.mention, url=member.avatar.url,
                                    colour=discord.Colour.red())
            embed10.add_field(name="ID", value=member.id, inline=False)
            embed10.add_field(name="status", value=member.status, inline=False)
            embed10.add_field(name="__**join server at**__ ",
                              value=member.joined_at.strftime('%a, %d %B %Y, %I:%M %p UTC'))
            embed10.add_field(name="__**created at**__ ",
                              value=member.created_at.strftime('%a, %d %B %Y, %I:%M %p UTC'))
            embed10.add_field(name='Bot?', value=member.bot)
            if len(roles) == 1:
                embed10.add_field(name=f'Roles ({len(roles) - 1})', value='**no roles**')
            else:
                embed10.add_field(name=f'Roles ({len(roles) - 1})',
                                  value=' '.join([role.mention for role in roles if role.name != '@everyone']))

            embed10.set_thumbnail(url=member.avatar.url)
            await ctx.send(embed=embed10)
        else:
            roles = []
            for role in ctx.user.roles:
                roles.append(role)
            embed10 = discord.Embed(title=ctx.user.name, description=ctx.user.mention,
                                    url=ctx.user.avatar.url,
                                    colour=discord.Colour.red())
            embed10.add_field(name="ID", value=ctx.user.id, inline=False)
            embed10.add_field(name="status", value=ctx.user.status, inline=False)
            embed10.add_field(name="__**join server at**__ ",
                              value=ctx.user.joined_at.strftime('%a, %d %B %Y, %I:%M %p UTC'))
            embed10.add_field(name="__**created at**__ ",
                              value=ctx.user.created_at.strftime('%a, %d %B %Y, %I:%M %p UTC'))
            embed10.add_field(name='Bot?', value=ctx.user.bot)
            if len(roles) == 1:
                embed10.add_field(name=f'Roles ({len(roles) - 1})', value='**NIL**')
            else:
                embed10.add_field(name=f'Roles ({len(roles) - 1})',
                                  value=' '.join([role.mention for role in roles if role.name != '@everyone']))
            embed10.set_thumbnail(url=ctx.user.avatar.url)
            embed10.add_field(name="permissions", value=ctx.user.guild_permissions)
            await ctx.response.send_message(embed=embed10)

    # whois command error
    @whois.error
    async def whois_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title="invalid username!")
            await ctx.send(embed=embed)
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=error)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="something went wrong :face_with_raised_eyebrow: ")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="member-count", description="show how many member this guild have")
    @commands.cooldown(1, 5, BucketType.user)
    async def membercount(self, ctx):
        time = datetime.utcnow().strftime(r"%I:%M %p")
        emed = discord.Embed(title=f"Members : ``{ctx.message.guild.member_count}``",colour=discord.Colour.gold())
        emed.set_footer(text=f"today at {time}")
        await ctx.send(embed=emed)

    # ping prefix command
    @commands.hybrid_command(name="ping",description="ping pong!", aliases=['mem'])
    @cooldown(1, 5, BucketType.user)
    async def ping(self, ctx):
        embed11 = discord.Embed(title="pong! 🏓 latency is "f"{round(self.bot.latency * 1000)}ms", description="",
                                url="", colour=discord.Colour.gold())
        button = Button(label="ping", style=discord.ButtonStyle.green, emoji="🏓")
        view = View()
        async def button_callback(interaction):
            await interaction.response.edit_message(embed=embed11, view=view)
        button.callback = button_callback
        view.add_item(button)
        await ctx.message.add_reaction("🏓")
        await ctx.send(embed=embed11, view=view)

    # avatar prefix command
    @commands.hybrid_command(name="avatar",description="Get a user avatar", aliases=['av'])
    @app_commands.describe(member="User")
    @cooldown(1, 5, BucketType.user)
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            embed10 = discord.Embed(title=ctx.message.author.display_name, description="",
                                    url=ctx.message.author.avatar.url,
                                    colour=discord.Colour.blue())
            embed10.set_image(url=ctx.message.author.avatar.url)
            await ctx.send(embed=embed10)
            return
        elif member is not None:
            embed9 = discord.Embed(title=member.display_name, description="", url=member.avatar.url,
                                   colour=discord.Colour.blue())
            embed9.set_image(url=member.avatar.url)
            await ctx.message.add_reactio

    @commands.hybrid_command(name="guild-avatar",description="Get a user avatar", aliases=['ga'])
    @commands.cooldown(1, 5, BucketType.user)
    async def guild_avatar(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}", url=ctx.guild.icon.url,colour=discord.Colour.gold())
        embed.set_image(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    # stats prefix command
    @commands.hybrid_command(name="stats",description="Get bot system information")
    @cooldown(1, 3, BucketType.user)
    async def stats(self, ctx):
        bedem = discord.Embed(title='System Resource Usage', description='See CPU and memory usage of the system.')
        bedem.add_field(name='CPU Usage', value=f'{psutil.cpu_percent()}%', inline=False)
        bedem.add_field(name='Memory Usage', value=f'{psutil.virtual_memory().percent}%', inline=False)
        bedem.add_field(name='Available Memory',
                        value=f'{psutil.virtual_memory().available * 100 / psutil.virtual_memory().total}%',
                        inline=False)
        await ctx.send(embed=bedem)

    # status prefix command
    @commands.command()
    @cooldown(1, 3, BucketType.user)
    async def status2(self, ctx):
        a = round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
        z = 100 - a
        uptime = (timedelta(seconds=int(round(time.time() - startTime))))

        embed = discord.Embed(title="Sussy-bot Status :", description="")
        embed.add_field(name=":<:2123:965984586322567218> Shard[0]",
                        value=f'<:space:965978649872441364> **version: ``Alpha``**\n<:space:965978649872441364>**ping : ``{round(self.bot.latency * 1000)}ms``** \n <:space:965978649872441364> **memory : ``{z}% used``** \n <:space:965978649872441364>**servers : ``{len(self.bot.guilds)}``** \n<:space:965978649872441364>**uptime : ``{uptime}``**')
        """embed.add_field(name="Memory ", value=f'{z}% used', )
        embed.add_field(name="Servers", value=f"{len(self.bot.guilds)}", )
        embed.add_field(name="Uptime", value=uptime, )
        "embed.set_thumbnail(url=self.client.user.avatar_url)"
        embed.set_author(name="sussy-bot", icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)"""
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="status",description="get bot status")
    @cooldown(1, 3, BucketType.user)
    async def status(self, ctx):
        a = round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
        z = 100 - a
        uptime = (timedelta(seconds=int(round(time.time() - startTime))))

        embed = discord.Embed(title="Sussy-bot Status :", description="")
        embed.add_field(name="Shard[0]", value=f'{round(self.bot.latency * 1000)}ms')
        embed.add_field(name="Memory ", value=f'{z}% used', )
        embed.add_field(name="Servers", value=f"{len(self.bot.guilds)}", )
        embed.add_field(name="Uptime", value=uptime, )
        "embed.set_thumbnail(url=self.client.user.avatar_url)"
        embed.set_author(name="sussy-bot", icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

    @status.error
    async def status_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"{error}")
        else:
            await ctx.send(
                "something went wrong do $help or report for bugs by doingn $bugs <bugs>")

    # top secret command
    @commands.command()
    @commands.is_owner()
    @cooldown(1, 59, BucketType.user)
    async def send_dm(self, ctx, member: discord.Member, *, content):
        channel = await member.create_dm()
        await channel.send(content)
        await ctx.send("done")

    # send a bug
    @commands.command()
    @cooldown(1, 59, BucketType.user)
    async def bugs(self, ctx, *, message):
        if len(message) >= 100:
            return
        else:
            with open("write.txt", "a") as f:
                f.write(f"\n{ctx.guild.name} : {ctx.message.author.display_name} : {message}")
            embed = discord.Embed(title="done")
            await ctx.send(embed=embed)

    """@commands.command()
    async def serverinfo(self, ctx):
        embed = discord.Embed()
        embed.set_author(icon_url=ctx.guild.icon.url , name=ctx.guild.name)
        embed.set_thumbnail(url=)"""

    """@commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.bot:
            print('function load')
            with open('messages.json', 'r') as f:
                users = json.load(f)
                print('file load')
            await self.update_data(users, ctx.author, ctx.guild)
            await self.add_experience(users, ctx.author, 4, ctx.guild)
            await self.level_up(users, ctx.author, ctx.channel, ctx.guild)

            with open('messages.json', 'w') as f:
                json.dump(users, f)

    async def update_data(self, users, user, server):
        if not str(server.id) in users:
            users[str(server.id)] = {}
            if not str(user.id) in users[str(server.id)]:
                users[str(server.id)][str(user.id)] = {}
                users[str(server.id)][str(user.id)]['experience'] = 0
                users[str(server.id)][str(user.id)]['level'] = 1
        elif not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1

    async def add_experience(self, users, user, exp, server):
        users[str(user.guild.id)][str(user.id)]['experience'] += exp

    async def level_up(self,users, user, channel, server):
        experience = users[str(user.guild.id)][str(user.id)]['experience']
        lvl_start = users[str(user.guild.id)][str(user.id)]['level']
        lvl_end = int(experience ** (1 / 4))
        if str(user.guild.id) != '939208771929014372':
            if lvl_start < lvl_end:
                await channel.send('{} has leveled up to Level {}'.format(user.mention, lvl_end))
                users[str(user.guild.id)][str(user.id)]['level'] = lvl_end

    @commands.command(aliases=['rank', 'lvl'])
    async def level(self, ctx, member: discord.Member = None):

        if not member:
            user = ctx.message.author
            with open('messages.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(ctx.guild.id)][str(user.id)]['level']
            exp = users[str(ctx.guild.id)][str(user.id)]['experience']

            embed = discord.Embed(title='Level {}'.format(lvl), description=f"{exp} XP ", color=discord.Color.green())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            with open('messages.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(ctx.guild.id)][str(member.id)]['level']
            exp = users[str(ctx.guild.id)][str(member.id)]['experience']
            embed = discord.Embed(title='Level {}'.format(lvl), description=f"{exp} XP", color=discord.Color.green())
            embed.set_author(name=member, icon_url=member.avatar.url)

            await ctx.send(embed=embed)"""

    """def get_messages(self,ctx):  ##first we define get_prefix
        with open('normal.json', 'r') as f:  ##we open and read the prefixes.json, assuming it's in the same file
            messageCount = json.load(f)  # load the json as prefixes
        return messageCount[str(ctx.guild.id)]
    @commands.Cog.listener()

    async def on_message(self, ctx):
        author = str(ctx.author.id)
        with open('normal.json', 'r') as f:  # read the prefix.json file
            messageCount = json.load(f)

        # if author in messageCount:
        #     with open('normal.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
        #         message_data = [{"888058231094665266": 6, "389604896606781440": 5}]
        #         json.dump(message_data, f, indent=4)
        await self.update_userdata(author, messageCount, ctx)
        logging.warning(ctx.guild)

    async def update_userdata(self, author, messageCount, ctx):
        counter = 0
        guild = ctx.guild.id

        for servers in messageCount:
            if guild == servers['guild']:
                author_msg = 0
                if author in servers['data']:
                    servers['data'][author] += 1
                    with open('normal.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
                        json.dump(servers, f, indent=4)
                        print(servers['data'])
                else:
                    servers['data'][author] = 1
                    with open('normal.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
                        json.dump(servers, f, indent=4)
                        print(servers)
            else:
                with open('normal.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
                    json.dump(servers['data'], f, indent=4)
                    print(servers['data'])"""

    # if author in messageCount:
    #     messageCount[0] += 1

    # else:
    #     messageCount[author] = 1
    #     logging.warning('No')

    # if author in messageCount:
    #     messageCount[author] += 1
    #     with open('normal.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
    #         final_data = {**json_data, **message_data}
    #         logging.warning(final_data)
    #         json.dump(final_data, f, indent=4)
    # else:
    #     messageCount[author] = 1
    #     with open('normal.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
    #         final_data = {**json_data, **message_data}
    #         logging.warning(final_data)
    #         json.dump(final_data, f, indent=4)

    # morseslash command

    @app_commands.command(name="morse", description="wanna write in dots ")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(message="message you wan to convert to")
    async def morseslash(self, interaction: discord.Interaction, message: str):
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

        await interaction.response.send_message(cipher)

    @morseslash.error
    async def morseslash_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"{error}", ephemeral=True)
        else:
            await interaction.response.send_message(
                "something went wrong do $help or report for bugs by doingn $bugs <bugs>", ephemeral=True)

    # morse commmand
    @commands.command()
    @cooldown(1, 10, BucketType.user)
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

    # text slash command
    @app_commands.command(name="text", description="wanna write in text ")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    @app_commands.describe(message="message you want to change it to")
    async def textslash(self, interaction: discord.Interaction, message: str):
        if len(message) >= 20:
            await interaction.response.send_message("text too long")
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

        await interaction.response.send_message(cipher)

    @textslash.error
    async def textslash_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"{error}", ephemeral=True)

        else:
            await interaction.response.send_message(
                "message must be number and latters not symbolsn", ephemeral=True)

    # text prfix command

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

        # add role command

        """if role.position > ctx.author.top_role.position:  # if the role is above users top role it sends error
            return await ctx.send('**:x: | That role is above your top role!**')
        if role in user.roles:
            await user.remove_roles(role)  # removes the role if user already has
            await ctx.send(f"Removed {role} from {user.mention}")
        else:
            await user.add_roles(role)  # adds role if not already has it
            await ctx.send(f"Added {role} to {user.mention}")"""

    @app_commands.command(name="clicktest", description="this is test")
    @app_commands.checks.cooldown(1, 5, key=lambda j: (j.guild_id, j.user.id))
    async def click(self, interaction: discord.Interaction):
        button = Button(label="click me!", style=discord.ButtonStyle.green, emoji="<:troll_sad:938264721268809789>")
        view = View()

        async def button_callback(interaction):
            await interaction.response.edit_message(content=f"{round(self.bot.latency * 1000)}ms", view=view)

        button.callback = button_callback
        view.add_item(button)
        await interaction.response.send_message(f"{round(self.bot.latency * 1000)}ms", view=view)

    @commands.command()
    @commands.is_owner()
    async def prepare(self, ctx: commands.Context):
        """Starts a persistent view."""
        # In order for a persistent view to be listened to, it needs to be sent to an actual message.
        # Call this method once just to store it somewhere.
        # In a more complicated program you might fetch the message_id from a database for use later.
        # However, this is outside the scope of this simple example.
        await ctx.send("What's your favourite colour?")

    """@commands.command()
    @commands.has_permissions(administrator=True)  # permissions
    async def verify_set(self, ctx ,channel: discord.TextChannel, *, role):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT rule FROM role WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO role(guild_id, rule) VALUES(?,?)")
            val = (ctx.guild.id, role)
        elif result is not None:
            sql = ("UPDATE role SET rule = ? WHERE guild_id = ?")
            val = (role, ctx.guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        embed11 = discord.Embed(title="click verify to verify yourself")

        view = PersistentView()

        await channel.send(embed=embed11, view=view)
        await ctx.send("verification setup complete")"""





    @commands.command()
    async def send_ch(self, ctx, channel: discord.TextChannel, *, message: str):
        await channel.send(message)
        await ctx.send("done")


async def setup(bot: SussyBot) -> None:
    await bot.add_cog(
        normal(bot))
