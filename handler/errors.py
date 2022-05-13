from discord.ext.commands.errors import CheckFailure
from discord.ext import commands




class NotPermitted(CheckFailure):
    '''Not Permitted'''
    pass


class AudioError(CheckFailure):
    '''Audio Error'''
    pass
