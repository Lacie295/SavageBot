# created by Sami Bosch on Wednesday, 27 November 2019

# This file contains all functions necessary to reply to messages
import re
from discord.ext import commands
import random

import db_handler

raids = {}


def init(client):
    class Pokemon(commands.Cog):
        @commands.command(pass_context=True)
        async def set_fc(self, context):
            m = context.message
            regex = r"^(SW-)?[0-9]{4}(-[0-9]{4}){2}$"
            if m.content.find(" ") > 0:
                fc = m.content.split(" ")[1]
                if re.match(regex, fc):
                    u_id = m.author.id
                    db_handler.set_fc(u_id, fc if fc.startswith("SW-") else "SW-" + fc)
                    await context.send("FC updated!")
                else:
                    await context.send("Please give the FC in the form SW-xxxx-xxxx-xxxx or xxxx-xxxx-xxxx.")
            else:
                await context.send("Please give an FC.")

        @commands.command(pass_context=True)
        async def get_fc(self, context):
            m = context.message
            if m.mentions:
                u_id = m.mentions[0].id
                await context.send(db_handler.get_fc(u_id))
            else:
                await context.send("Please provide an user.")

        @commands.command(pass_context=True)
        async def trade(self, context):
            m = context.message
            if m.mentions:
                user = m.mentions[0]
                author = m.author
                u_fc = db_handler.get_fc(user.id)
                a_fc = db_handler.get_fc(author.id)

                code = str(random.randint(0, 9999))

                await user.send("FC: " + a_fc + "\nCode: " + code)
                await author.send("FC: " + u_fc + "\nCode: " + code)
            else:
                await context.send("Please provide an user.")

        @commands.command(pass_context=True)
        async def host(self, context):
            author = context.message.author
            a_id = author.id
            if a_id not in raids:
                code = str(random.randint(0, 9999))
                raids[a_id] = (code, [])
                await context.send("Raid created!")
                await author.send("Raid code: " + code)
            else:
                await context.send("You're already hosting a raid!")

        @commands.command(pass_context=True)
        async def close(self, context):
            author = context.message.author
            a_id = author.id
            if a_id in raids:
                raids.pop(a_id)
                await context.send("Raid closed!")
            else:
                await context.send("You aren't hosting a raid!")

        @commands.command(pass_context=True)
        async def join(self, context):
            m = context.message
            author = m.author
            a_id = author.id
            if m.mentions:
                host = m.mentions[0]
                h_id = host.id
                if h_id in raids:
                    raid = raids[h_id]
                    if a_id not in raid[1] or a_id == h_id:
                        if len(raid[1]) < 4:
                            raid[1].append(a_id)
                            await author.send("FC: " + db_handler.get_fc(h_id) + "\nRaid code: " + raid[0])
                            await context.send("Joined raid!")
                        else:
                            await context.send("Raid already full!")
                    else:
                        await context.send("You are already in the raid!")
                else:
                    await context.send(host.name + " is currently not hosting a raid.")
            else:
                await context.send("Please provide a raid.")

        @commands.command(pass_context=True)
        async def leave(self, context):
            m = context.message
            author = m.author
            a_id = author.id
            if m.mentions:
                host = m.mentions[0]
                h_id = host.id
                if h_id != a_id:
                    if h_id in raids:
                        raid = raids[h_id]
                        if a_id in raid[1]:
                            raid[1].remove(a_id)
                            await context.send("Left raid!")
                        else:
                            await context.send("You are not participating in that raid!")
                    else:
                        await context.send(host.name + " is currently not hosting a raid.")
                else:
                    await context.send("You can't leave your own raid! Use !close instead.")
            else:
                await context.send("Please provide a raid.")

        @commands.command(pass_context=True)
        async def kick(self, context):
            m = context.message
            author = m.author
            a_id = author.id
            if m.mentions:
                user = m.mentions[0]
                u_id = user.id
                if a_id in raids:
                    raid = raids[a_id]
                    if u_id in raid[1]:
                        raid[1].remove(u_id)
                        await context.send("Kicked " + user.name + " out of the raid!")
                    else:
                        await context.send(user.name + " is not participating in that raid!")
                else:
                    await context.send("You are currently not hosting a raid.")
            else:
                await context.send("Please provide an user.")

        @commands.command(pass_context=True)
        async def list(self, context):
            m = context.message
            author = m.author
            a_id = author.id
            if a_id in raids:
                raid = raids[a_id][1]
                s = author.name
                for u_id in raid:
                    user = client.get_user(u_id)
                    s += "\n" + user.name
                await context.send("Currently in the raid:\n" + s)
            else:
                await context.send("You are currently not hosting a raid.")

    client.add_cog(Pokemon())
