import discord
import asyncio
from discord.ext import commands
import motor.motor_asyncio
import pprint

class Ad_Messages_database_display_command(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def ad_database(self, ctx, adtoboost):
        await ctx.send(f"```{self.bot.db.Ad_Message.find()}```")

        # TODO: Only Wael and Zeyad can use.

def setup(bot):
    bot.add_cog(Ad_Messages_database_display_command(bot))
