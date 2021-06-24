import discord
import asyncio
from discord.ext import commands, tasks
import motor.motor_asyncio
import random
from random import choice as randchoice
from random import shuffle
import traceback, sys
import pprint

channel_dict = {} # Dictionary for the time interval of each channel. Set at the get_interval_message_data() function and gets its data from MongoDB "Guilds" collection. {channel_id: time_interval}

# For random.choice() send ad message. ## message_dict = {} # Dictionary for the messages in the MongoDB Document. Should be 3 as of the time of writing this.
# For random.choice() send ad message. ## message_saved = {} # Dictionary for the last message sent in a channel by the bot. {channel_id: message.content}

class ad_loop_message(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel_tasks = {}

# Allow people to change the channels where the main ad is sent and to change the main ad loop duration time.

    @commands.Cog.listener()
    async def on_ready(self): ### on_ready event for the bot.
        await self.bot.loop.create_task(self.get_interval_message_data())
        ad_messages_2 = self.bot.db.Ad_Messages.find()

        ## async for each_message in ad_messages_2:                                  ### For random.choice() send ad message.
        ##     message_dict[each_message["ad_name"]] = each_message["ad_message"]    ###
        ## print(message_dict)                                                       ###

        self.bot.loop.create_task(self.db_loop_and_task_create())

    @commands.command()
    ## @commands.cooldown(1, 60, commands.BucketType.guild)
    # Fix cooldown for this command. Maybe re-add the cooldown exception.
    async def setup(self, ctx):
        db_document = self.bot.db.Guilds.find({"guild_id" : ctx.guild.id}).limit(1)
        async for i in db_document:
            if i["main_ad_on_or_off"] == False:
                await ctx.message.channel.send("Ping the names (ex. '#general, #announcements, #partners' or, if you want only one channel, ping just that channel, such as: '#giveaways') of the channels that you want the main message ad to run in. Seperate each channel with a comma.")
                def check(m):
                    return m.channel_mentions and m.channel.id == ctx.message.channel.id
                dict = {
                    "main_ad_channels" : {

                    }
                }
                response_1 = await self.bot.wait_for('message', timeout = 30, check = check)
                for x in response_1.channel_mentions:
                    dict["main_ad_channels"]["channel_" + x.name] = x.id
                insert_update = self.bot.db.Guilds.update_one({"guild_id": ctx.guild.id}, { "$set" : dict})

                await ctx.message.channel.send("Channels have been set!")



                print("done 1")



                await ctx.message.channel.send("Set the duration you want each message ad to be sent in minutes. Minimum is 5 minutes, and maximum is 1440 minutes. No decimals or fractions, it must be a whole number. (ex. '5', or '60', or '1440')")

                def check(m_2):
                    return m_2.content.isdigit() and m_2.channel == ctx.message.channel and int(m_2.content) in range(5,1441)

                response_2 = await self.bot.wait_for('message', check = check)
                insert_update_2 = self.bot.db.Guilds.update_one({"guild_id": ctx.guild.id}, { "$set" : {"main_ad_loop_duration_time" : int(response_2.content)}})

                await ctx.channel.send("Setup is complete! Use the `>startad` command to start running ads!")

            else:
                await ctx.channel.send("The bot is currently running ads. In order to change the setup functionality (channels and time intervals) please use the (command_prefix)stopad (ex. >stopad) command first.")

    # Give owner options about which ad they want to run on the server.
    # Add timeout and then try: and except: the timeout after 60 seconds to check for when people forget to write anything.
    # Add an X emoji that people can select to stop the process.

    # Display error message. Display error message if 'time' parameter is not an integer.
    # Send message saying that the time has been set to x MINUTES. Specify that it is minutes.
    # Make minutes limited to a minimum of 5 minutes and a maximum of the product of 60x24 or just 60 minutes.


    @commands.command()
    async def startad(self, ctx): ### Adds the True value to the guild's document and begins sending the ads.
        insert_one = self.bot.db.Guilds.update_one({"guild_id" : ctx.guild.id}, {"$set" : {"main_ad_on_or_off" : True}})
        await ctx.send("Ads started.")

    @commands.command()
    async def stopad(self, ctx):
        insert_one = self.bot.db.Guilds.update_one({"guild_id" : ctx.guild.id}, {"$set" : {"main_ad_on_or_off" : False}})
        self.channel_tasks.pop(ctx.channel.id)
        await ctx.send("Ads stopped.")

    async def get_interval_message_data(self): ### This takes the information about the time duration and channels where the main ad will be displayed, which are set by the server owner, from the database. Then, this loop task sends the message in the specific channels ever x given minutes.
        await self.bot.wait_until_ready()
        all_documents = self.bot.db.Guilds.find()
        async for each_document in all_documents:
            interval = each_document["main_ad_loop_duration_time"]
            for each_channel in each_document["main_ad_channels"].values():
                got_channel = self.bot.get_channel(each_channel)
                channel_dict[got_channel.id] = {"channel_id": int(each_channel), "interval": int(interval)}

    async def sender(self, timetosleep, channeltosend):                         ### Sends the ad message in the specified channel, at the specified wait-time interval, and prevents the sending of the same ad twice or more in a row.
        while not self.bot.is_closed():
            channel_to_send_ad_message = self.bot.get_channel(channeltosend)
            all_ad_messages_documents = self.bot.db.Ad_Messages.find()
            shuffle_list = []
            async for each_ad_message_document in all_ad_messages_documents:
                shuffle_list.append(each_ad_message_document["ad_message"])

            random.shuffle(shuffle_list)
            for each_ad_message in shuffle_list:
                await channel_to_send_ad_message.send(each_ad_message)
                await asyncio.sleep(timetosleep)


        # counter = 0                                                           ### A variable that is used to make sure that the sender() function does not save the bot's last message from before it was ran. Main use begins when it is above the integer 0, aka at integer 1.
        # while not self.bot.is_closed():                                       ### Continues loop until the bot is closed.
        #     channeltosend_2 = self.bot.get_channel(channeltosend)             ### Gets the channel object to send the ad in.
        #     if counter != 0:                                                  ### Checks if the counter var is not equal to integer 0.
        #         async for message in channeltosend_2.history():               ### Loops through the entire message history of the channel that the ad message is to be sent in. IMPORTANT: this loops through all messages, not just the bot's messages.
        #             if message.author.id == self.bot.user.id:                 ### Checks if the last looped message was sent by the bot.
        #                 message_saved[channeltosend] = message.content        ### Inserts the last message that the bot sent in a specific channel. {channel_id: message.content}
        #                 break                                                 ### return so you won't have to keep iterating. Once the first message by the bot in the history function is found it stops the for loop.
        #     else:                                                             ### Passes. This is here to not insert the message.content of the last message the bot sent before it was ran.
        #         pass
        #     await asyncio.sleep(timetosleep)                                  ### Sets the waiting period between the current message and the last message based on the given time interval. Sets custom time interval for each channel.
        #
        #     Maybe move this ^^^^^ (asyncio.sleep(timetosleep)) up in the beginning of the function so that the bot waits before sending the very first message, instead of sending a message instantly after the bot is ran.
        #
        #     random_message = randchoice(list(message_dict.values()))          ### Chooses the initial random ad message.
        #     if random_message in message_saved.values():                      ### Does this if the randomly chosen ad message was used in the previously sent message in the earlier specified channel by the bot.
        #         while random_message in message_saved.values():               ### Loops until a new random ad message is chosen. New as opposed to the initial random ad message.
        #             random_message = randchoice(list(message_dict.values()))  ### Chooses another random ad message if/when the initial random ad message is the same message previously sent by the bot in the earlier specified channel.
        #         await channeltosend_2.send(random_message)                    ### Sends the new random ad message once the while loop is finished and a new random ad message is chosen.
        #         if counter == 0:                                              ### Checks if the counter variable is equal to zero. This is used to make sure that the bot does not use the last message sent by the bot *before* the bot was ran as a reference preventing repeated random messages in the earlier specified channel.
        #             counter = counter + 1                                     ### Adds to counter if it has not been added to already.
        #     else:                                                             ### Does this if the randomly chosen ad message was not used in the previously sent message in the earlier specified channel by the bot.
        #         await channeltosend_2.send(random_message)                    ### Sends the random message.
        #         if counter == 0:                                              ### Checks if the counter variable is equal to zero. This is used to make sure that the bot does not use the last message sent by the bot *before* the bot was ran as a reference preventing repeated random messages in the earlier specified channel.
        #             counter = counter + 1                                     ### Adds to counter if it has not been added to already.

            # Don't send the same ad more than twice in a row unless there is only one ad in the database.
            # Make time interval into minutes and not seconds.
            # Only usable by people with admin perms.


            # Add the phone features.
            # Make sure there are no errors.
            # Make it pretty.
            # Picture ads.


    async def db_loop_and_task_create(self):
        while not self.bot.is_closed():
            for each_channel_2 in channel_dict:
                c = channel_dict[each_channel_2]["channel_id"]
                db_document = await self.bot.db.Guilds.find({"guild_id" : self.bot.get_channel(each_channel_2).guild.id}).to_list(length = 1)
                for i in db_document:
                    if i["main_ad_on_or_off"] == True:
                        if channel_dict[each_channel_2]["channel_id"] in self.channel_tasks:
                            if c in self.channel_tasks and not self.channel_tasks[c].cancelled():
                                continue
                        time_interval = channel_dict[each_channel_2]["interval"]
                        channel_to_send = channel_dict[each_channel_2]["channel_id"]
                        task_sender = self.bot.loop.create_task(self.sender(time_interval, channel_to_send))
                        self.channel_tasks[channel_dict[each_channel_2]["channel_id"]] = task_sender
                    else:
                        if c in self.channel_tasks and not self.channel_tasks[c].cancelled():
                            self.channel_tasks[c].cancel()


def setup(bot):
    bot.add_cog(ad_loop_message(bot))
