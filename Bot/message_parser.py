# created by Sami Bosch on Wednesday, 27 November 2019

# This file contains all functions necessary to reply to messages
import discord
from discord.ext import commands


def init(client):
    class Pokemon(commands.Cog):
        @commands.command(pass_context=True)
        async def add_fc(self, context):
            m = context.message

    client.add_cog(Pokemon())
