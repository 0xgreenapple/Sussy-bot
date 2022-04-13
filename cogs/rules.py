import discord
import datetime
from discord.ext import commands
import json


class info(commands.Cog):

    def __init__(self, client):
        self.client = client


    def get_message(self, client, ctx):  ##first we define get_prefix
        with open('message.json', 'r') as f:  ##we open and read the prefixes.json, assuming it's in the same file
            msg = json.load(f)  # load the json as prefixes
        return msg[str(ctx.guild.id)]

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_rule(self,ctx,*, rule):
        with open('message.json', 'r') as f:  # read the prefix.json file
            msg = json.load(f)
        msg[str(ctx.guild.id)] = rule
        with open('message.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
            json.dump(msg, f, indent=4)
        await ctx.send("rule done")

    @commands.command()
    async def rules(self,ctx):
        await ctx.send(self.get_message(self.client , ctx))


    def is_it_me(self, ctx):
        return ctx.guild.id == 917471209329946695
    @commands.command(description = "get rules",)
    async def dsd(self,ctx):

        whole_rules = discord.Embed(title="rules",description="list of rules\n"
                                                              "infromation based on discord tos https://discord.com/terms",colour=discord.Colour.red())

        #rules1
        whole_rules.add_field(name="__**Respect one another**__",
                              value=" Don't be an inconvenience to others!* *Be resp\
                              ectful. Respect the server, the members, the staff, and\
                               anyone else here. We want to create a friendly and\
                                encouraging environment community. Also Absolutely No\
                                 Homophobic, Trans-phobic, Racism, flirting, fetishistic\
                                  or any other similar behaviour /hate speech allowed. We \
                                  want everyone to feel welcome  heart",)
        #rules 2

        whole_rules.add_field(name="__**No piracy, plagiarism, scams, spamming, advertising other servers, malicious files or discord crashers.**__",
                              value="Keep it fun and friendly!no spam or self-promotion(server \
                              invites, advertisements, etc) without permission from a staff.\
                               This includes DMing server members. No begging. Don’t send a \
                               lot of small messages right after each other. do not disrupt\
                                chat by spamming. use appropriate channels for your Post", inline=False)

        #rules 3
        whole_rules.add_field(name="__**No NSFW content & keep your language tame**__",
                              value="Don't send/show any offensive, political, religious,\
                               hateful, illegal, or 18+ content in any way.No NSFW or\
                                obscene content. this includes text, images, or link \
                                features nudity, sex, hard violence, or other graphically\
                                 disturbing content. Political and religious discussions\
                                  are also prohibited. Swearing is allowed as long as it's\
                                   not used as an insult.",inline=False)
        #rules 4

        whole_rules.add_field(name="__**Use the appropriate channels for your posts.**__",
                              value="Read the channel descriptions if you need more info.\
                              Keep discussions in their relevant channels", inline=False)
        #rules 5

        whole_rules.add_field(name="__**English only**__",
                              value="English is to be used as your main language in text channels.\
                                 let's stick with it so we can all understand each other and easier\
                                 moderation for staff teams",inline=False)

        #whole_rules.set_footer(text="infromation based on discord tos https://discord.com/terms",icon_url="https://support.discord.com/hc/article_attachments/360052376732/discord_security_shield.png")
        if ctx.guild.id != 917471209329946695:  # This is the wanted guild id
            return
        else:
            await ctx.send(embed=whole_rules)






async def setup(bot):
    await bot.add_cog(info(bot))
