import discord
import asyncio
from discord.ext import commands
import motor.motor_asyncio
import pprint

class payment_system(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Track clicks, such as opens. When someone clicks the link to the ad, it takes you to a redirect link where we can collect
    # data on the user. Collect email, IP, hardware IPs (for hardware bans if needed). Sell data / use it for making money:
    # Email List. -/

    # Make a discordservers website or some other website that acts as the redirect website. The website will get a lot of
    # traction from the redirecting. -/

    # Put something in the database for each guild saying that someone from that server clicked the link.

    # Only pay server owners based on the first time a new person clicks that link. Check Discord ID, or user's IP, to check
    # if it is the first time they have clicked the ad or if it is not the first time.

    # MAKE IT SO THAT ONLY DISCORD ACCOUNTS THAT ARE OLDER THAN 6 MONTHS CAN EARN THE SERVER OWNER MONEY.

    ########################################################################################################################


    "guild_id_here": {
        "ad_id_here": {
            "redirect_link": "redirect_link_here"
            "referal_counter": 0
        },

        "ad_id_here": {
            "redirect_link": "redirect_link_here"
            "referal_counter": 0
        }
    }

    # Need collection in db for each guild and in the collection have a custom redirect link for each ad. Remove custom redirect for ad once it expires. Add redirect link for ad when someone buys it. Have a referal counter in each redirect link for each ad in each guild.


    @commands.command()
    async def collectearnings(): # Allowes server owners to collect their earnings.
        pass

        # TODO: Only accessible to server owners. Has to be server owner to use the command. Maybe add a feature where the server owner can specify which other member can collect earnings as well.

    @commands.command()
    async def collectearnings_license():
        pass

        # TODO: Must have the "Distribution License" role in order to use this command.

def setup(bot):
    bot.add_cog(payment_system(bot))
