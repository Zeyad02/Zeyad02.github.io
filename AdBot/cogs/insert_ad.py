import discord
import asyncio
from discord.ext import commands
import motor.motor_asyncio
import pprint
import pendulum

class payment_system(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command() #// v.02
    async def insert_ad(self, ctx, package_id): # Allows SquanchyBot owners to add an ad to the Ad_Messages collection in the SquanchyBot Database.

        Ad_Messages_col = self.bot.db.Ad_Messages.find()

        Ad_Messages_col.insert_one()



        # TODO: Only allow admins of SquanchyBot to use this command.
        # TODO: Get the Ad_Messages collection.
        # TODO: Insert the ad to the collection in its own document.
            # - TODO: ad_name: Name of ad here.
            # - TODO: ad_message: Ad message here.
            # - TODO: ad_buyer: {"ad_buyer_name": member.name, "ad_buyer_id": member.id}

            # - TODO: ad_package: [package_id] # set this to a list of all the packages that the person wants. Loop with for.


    @commands.command()
    async def grantpremium(self, ctx, reciever : discord.Member, grant_role, expiration_date : int = pendulum.now().add(days = 30)): # Grants either premium plus or regular preium to a specified user.
        print(pendulum.now().add(days = 30))

        if grant_role == int():
            role_object = await bot.get_role(grant_role)
            role_to_assign = role_object.name
        else:
            role_to_assign = grant_role

        roles = ["premium", "premium+", "premium-plus"]

        if role_to_assign.lower() in roles:

            all_guild_roles = await ctx.guild.roles()
            final_role = all_guild_roles[role_to_assign.lower()]
            await reciever.add_roles(final_role.id)
            await ctx.send(f"Assigned the {role_to_assign.capitalize} package and role to {reciever.mention}.")

            #
            # if role_to_assign.lower() == roles[0]:
            #     await reciever.add_roles(857067051629805588)
            #     await ctx.send(f"Assigned the Premium package and role to {reciever.mention}.")
            #     # TODO: Add the "Premium" role to reciever parameter (member object).
            #
            # elif role_to_assign.lower() == roles[1] or role_to_assign.lower() == roles[2]
            #     await reciever.add_roles(857067093694218281)
            #     await ctx.send(f"Assigned the Premium+ package and role to {reciever.mention}.")
            #     # TODO: Add the "Premium-Plus" role to reciever parameter (member object).

        else:
            await ctx.send("You gave the wrong role name. The roles which can be granted are only: 'premium' and 'premium+' .")

        # TODO: Only allow admins of SquanchyBot to use this command.
        # TODO: Get the Subscriptions collection.
        # TODO: Insert the info to the collection, alongside the grantlicense-command info.
        # TODO: Add the "Premium" or "Premium Plus" roles.

    @commands.command()
    async def grantlicense(self, ctx, reciever: discord.Member, expiration_date : int): # Grants a license to distribute product to a specified member.
        pass

        # TODO: Only allow admins of SquanchyBot to use this command.
        # TODO: Get the Subscriptions collection.
        # TODO: Insert the info to the collection, alongside the grantlicense-command info.
        # TODO: Add the "Distribution License" role.



def setup(bot):
    bot.add_cog(payment_system(bot))
