import discord
from discord.ext import commands,tasks
import os
import time
from dotenv import load_dotenv
import json
from zora_discord import startBot

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='^')

load_dotenv()

@bot.command(name='wallet', help='Check Wallet for mints and sales')
async def wallet(ctx, *, arg):
    print('test')
    userid = ctx.message.author.id
    link = startBot(arg)
    await ctx.send(f'<@{userid}>\n **{link}**')

if __name__ == "__main__" :
    bot.run(os.environ["DISCORD_TOKEN"])
