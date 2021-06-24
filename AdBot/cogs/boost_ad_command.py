import discord
import asyncio
from discord.ext import commands
import motor.motor_asyncio
import pprint

class boost_ad_command(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def boostad(self, ctx, adtoboost): # Creates another copy of the specified ad in the database, hence, increasing the amount it gets sent.
        pass

        # TODO: Only Wael and Zeyad can use.

    @commands.command()
    async def removeboostad(self, ctx, adtoremove):
        pass

        # TODO: Add a removeboostad command.

def setup(bot):
    bot.add_cog(boost_ad_command(bot))
