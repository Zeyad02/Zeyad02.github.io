import discord
from discord.ext import commands
import motor.motor_asyncio
import pprint

prefix = ">"
bot = commands.Bot(command_prefix = prefix)

cogs = ['cogs.ad_loop_message', 'cogs.boost_ad_command', 'cogs.Ad_Messages_database_display_command']

myclient = motor.motor_asyncio.AsyncIOMotorClient("localhost", 27017)
bot.db = myclient['SquanchyBot']

@bot.event
async def on_ready():
    print(f'Ready')

@bot.command()
async def emergencystop(ctx, number): # Stops either admin commands or the entire bot's commands in case there is an emergency.
    if number == 1:
        pass

        # TODO: Only SquanchyBot Admins can use this command.
        # TODO: Stop only SquanchyBot admin (database) commands.

    elif number == 2:
        pass

        # TODO: Only Zeyad and Wael can use this.
        # TODO: Stop everything. Even ads.

    else:
        await ctx.send("Incorrectly used. This command is used as follows: '(command_prefix_here)emergencystop (number)' || Number can be either '1' or '2'. '1' is for stopping SquanchyBot Admin commands. '2' is for stopping the entire bot, **INCLUDING CURRENTLY RUNNING ADS**.")

@bot.event
async def on_guild_join(guild): # Gets the guild.id of the guild when the bot first joins the guild and stores it in the Guilds collection in the database.
    dict = {
        'guild_id' : guild.id
    }
    x = bot.db.Guilds.insert_one(dict)

# Add: Remove guild.id from database when the bot leaves the server.

@bot.command()
async def purge(ctx, amount: int):
    deleted = await ctx.channel.purge(limit = amount)
    await ctx.send(f"Deleted {len(deleted)} messages")

    # TODO: Make it so that only people with admin perms can use this.

for cog in cogs:
    bot.load_extension(cog)
    print(cog)
print("cogs set up!")

bot.run("ODU0MTE4MTYxMzkyODYxMjI0.YMfRhg.i0gWrHFrVgmOmTBhFlg9crPzG0Y")
